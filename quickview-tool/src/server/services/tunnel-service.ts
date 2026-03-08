import { spawn } from 'child_process';

interface ProviderInfo {
  label: string;
  description: string;
  setup: string;
}

const PROVIDERS: Record<string, ProviderInfo> = {
  localtunnel: {
    label: 'localtunnel',
    description: 'Free, no account required',
    setup: 'npm install localtunnel',
  },
  ngrok: {
    label: 'ngrok',
    description: 'Requires account + authtoken',
    setup: 'npm install @ngrok/ngrok && export NGROK_AUTHTOKEN=your_token',
  },
  tailscale: {
    label: 'Tailscale Funnel',
    description: 'Requires Tailscale CLI + Funnel enabled',
    setup: 'tailscale up && enable Funnel in ACL policy',
  },
};

interface TunnelServiceOptions {
  provider: string;
  port?: number;
}

export class TunnelService {
  private provider: string;
  private port: number;
  url: string | null;
  private _cleanup: (() => Promise<void>) | null;

  constructor(options: TunnelServiceOptions) {
    this.provider = options.provider;
    this.port = options.port || 3333;
    this.url = null;
    this._cleanup = null;
  }

  static get supportedProviders(): string[] {
    return Object.keys(PROVIDERS);
  }

  static getProviderInfo(name: string): ProviderInfo | undefined {
    return PROVIDERS[name];
  }

  async start(): Promise<string> {
    const startFn: Record<string, () => Promise<string>> = {
      localtunnel: () => this._startLocaltunnel(),
      ngrok: () => this._startNgrok(),
      tailscale: () => this._startTailscale(),
    };

    const fn = startFn[this.provider];
    if (!fn) {
      throw new Error(
        `Unknown tunnel provider: "${this.provider}". ` +
          `Supported: ${TunnelService.supportedProviders.join(', ')}`,
      );
    }

    this._printSecurityWarning();
    return fn();
  }

  private _printSecurityWarning(): void {
    console.warn('');
    console.warn('WARNING: Tunnel mode exposes this server to the internet.');
    console.warn('Anyone with the URL can browse files and execute Python scripts.');
    console.warn('Only use this in trusted environments with non-sensitive files.');
    console.warn('');
  }

  private async _startLocaltunnel(): Promise<string> {
    let localtunnel: any;
    try {
      localtunnel = require('localtunnel');
    } catch {
      console.error('localtunnel package not installed. Install it with:');
      console.error('  npm install localtunnel');
      throw new Error('localtunnel package not found');
    }

    const tunnel = await localtunnel({ port: this.port });
    this.url = tunnel.url;
    this._cleanup = async () => {
      tunnel.close();
    };

    tunnel.on('close', () => {
      this.url = null;
    });

    return this.url!;
  }

  private async _startNgrok(): Promise<string> {
    let ngrok: any;
    try {
      ngrok = require('@ngrok/ngrok');
    } catch {
      console.error('ngrok package not installed. Install it with:');
      console.error('  npm install @ngrok/ngrok');
      console.error('');
      console.error('You also need an ngrok authtoken. Get one at https://dashboard.ngrok.com');
      console.error('Then set it: export NGROK_AUTHTOKEN=your_token');
      throw new Error('ngrok package not found');
    }

    const listener = await ngrok.forward({
      addr: this.port,
      authtoken_from_env: true,
    });

    this.url = listener.url();
    this._cleanup = async () => {
      await ngrok.disconnect();
    };

    return this.url!;
  }

  private async _startTailscale(): Promise<string> {
    return new Promise((resolve, reject) => {
      const proc = spawn('tailscale', ['funnel', '--bg', String(this.port)], {
        stdio: ['ignore', 'pipe', 'pipe'],
      });

      let stdout = '';
      let stderr = '';

      proc.stdout.on('data', (data) => {
        stdout += data.toString();
      });
      proc.stderr.on('data', (data) => {
        stderr += data.toString();
      });

      const timeout = setTimeout(() => {
        proc.kill();
        reject(new Error('Tailscale funnel timed out after 15s'));
      }, 15000);

      proc.on('close', (code) => {
        clearTimeout(timeout);

        if (code !== 0) {
          console.error('Tailscale funnel failed:', stderr || stdout);
          console.error('');
          console.error('Make sure Tailscale is installed and logged in (tailscale up).');
          console.error('Funnel must be enabled in your ACL policy.');
          console.error('See: https://tailscale.com/kb/1223/funnel');
          reject(new Error('Tailscale funnel failed'));
          return;
        }

        const urlMatch = (stdout + stderr).match(/https:\/\/[^\s]+/);
        if (urlMatch) {
          this.url = urlMatch[0];
          this._cleanup = async () => {
            spawn('tailscale', ['funnel', '--bg', 'off'], { stdio: 'ignore' });
          };
          resolve(this.url);
        } else {
          this._getTailscaleDnsName()
            .then((dnsName) => {
              this.url = `https://${dnsName}`;
              this._cleanup = async () => {
                spawn('tailscale', ['funnel', '--bg', 'off'], { stdio: 'ignore' });
              };
              resolve(this.url!);
            })
            .catch(() => {
              reject(new Error('Tailscale funnel started but could not determine URL'));
            });
        }
      });
    });
  }

  private async _getTailscaleDnsName(): Promise<string> {
    return new Promise((resolve, reject) => {
      const proc = spawn('tailscale', ['status', '--json'], {
        stdio: ['ignore', 'pipe', 'pipe'],
      });

      let stdout = '';
      proc.stdout.on('data', (data) => {
        stdout += data.toString();
      });

      proc.on('close', (code) => {
        if (code !== 0) {
          reject(new Error('Could not get tailscale status'));
          return;
        }
        try {
          const status = JSON.parse(stdout);
          const dnsName = status.Self?.DNSName?.replace(/\.$/, '');
          if (dnsName) {
            resolve(dnsName);
          } else {
            reject(new Error('No DNS name found'));
          }
        } catch {
          reject(new Error('Failed to parse tailscale status'));
        }
      });
    });
  }

  async stop(): Promise<void> {
    if (this._cleanup) {
      try {
        await this._cleanup();
      } catch {
        // Best effort cleanup
      }
      this._cleanup = null;
    }
    this.url = null;
  }
}
