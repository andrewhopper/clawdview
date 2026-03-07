const { spawn } = require('child_process');

class TunnelService {
  constructor(options = {}) {
    this.provider = options.provider; // 'ngrok' or 'tailscale'
    this.port = options.port || 3333;
    this.url = null;
    this._cleanup = null;
  }

  async start() {
    if (this.provider === 'ngrok') {
      return this._startNgrok();
    } else if (this.provider === 'tailscale') {
      return this._startTailscale();
    }
    throw new Error(`Unknown tunnel provider: ${this.provider}`);
  }

  async _startNgrok() {
    let ngrok;
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

    return this.url;
  }

  async _startTailscale() {
    return new Promise((resolve, reject) => {
      // Use `tailscale funnel` to expose the port
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

      proc.on('close', (code) => {
        if (code !== 0) {
          console.error('Tailscale funnel failed:', stderr || stdout);
          console.error('');
          console.error('Make sure Tailscale is installed and you are logged in:');
          console.error('  tailscale up');
          console.error('');
          console.error('Funnel must also be enabled in your Tailscale ACLs.');
          console.error('See: https://tailscale.com/kb/1223/funnel');
          reject(new Error('Tailscale funnel failed'));
          return;
        }

        // Parse the URL from tailscale funnel output
        const urlMatch = (stdout + stderr).match(/https:\/\/[^\s]+/);
        if (urlMatch) {
          this.url = urlMatch[0];
        } else {
          // Derive from tailscale status if not in output
          this._getTailscaleUrl().then((url) => {
            this.url = url;
            resolve(this.url);
          }).catch(() => {
            this.url = `https://<your-machine>.tailnet-name.ts.net:${this.port}`;
            resolve(this.url);
          });
          return;
        }

        this._cleanup = async () => {
          spawn('tailscale', ['funnel', '--bg', 'off'], {
            stdio: 'ignore',
          });
        };

        resolve(this.url);
      });

      // Timeout after 15 seconds
      setTimeout(() => {
        proc.kill();
        reject(new Error('Tailscale funnel timed out'));
      }, 15000);
    });
  }

  async _getTailscaleUrl() {
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
            resolve(`https://${dnsName}`);
          } else {
            reject(new Error('No DNS name found'));
          }
        } catch {
          reject(new Error('Failed to parse tailscale status'));
        }
      });
    });
  }

  async stop() {
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

module.exports = TunnelService;
