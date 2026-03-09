import { useState, useCallback } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from './ui/dialog';
import { Button } from './ui/button';
import { Input } from './ui/input';
import type { CurrentFile } from '../types';

const EXPIRY_OPTIONS = [
  { value: 900, label: '15 minutes' },
  { value: 3600, label: '1 hour' },
  { value: 86400, label: '24 hours' },
  { value: 604800, label: '7 days' },
];

function formatExpiry(seconds: number): string {
  if (seconds < 3600) return `${Math.round(seconds / 60)} minutes`;
  if (seconds < 86400) return `${Math.round(seconds / 3600)} hour(s)`;
  return `${Math.round(seconds / 86400)} day(s)`;
}

interface ShareModalProps {
  file: CurrentFile | null;
  isOpen: boolean;
  onClose: () => void;
}

export function ShareModal({ file, isOpen, onClose }: ShareModalProps) {
  const [expiresIn, setExpiresIn] = useState(3600);
  const [url, setUrl] = useState<string | null>(null);
  const [info, setInfo] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [copied, setCopied] = useState(false);

  const reset = useCallback(() => {
    setUrl(null);
    setInfo('');
    setError(null);
    setCopied(false);
  }, []);

  const handleOpenChange = useCallback((open: boolean) => {
    if (!open) {
      onClose();
      reset();
    }
  }, [onClose, reset]);

  const handleShare = useCallback(async () => {
    if (!file) return;
    setLoading(true);
    setError(null);

    try {
      const response = await fetch('/api/share/presign', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ filePath: file.path, expiresIn }),
      });
      const data = await response.json();

      if (!response.ok) throw new Error(data.error || 'Failed to create share link');

      setUrl(data.url);
      setInfo(`Pre-signed URL expires in ${formatExpiry(data.expiresIn)}`);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [file, expiresIn]);

  const handleCopy = useCallback(async () => {
    if (!url) return;
    try {
      await navigator.clipboard.writeText(url);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      // fallback: select the input
    }
  }, [url]);

  return (
    <Dialog open={isOpen} onOpenChange={handleOpenChange}>
      <DialogContent className="max-w-md">
        <DialogHeader>
          <DialogTitle>Share via S3</DialogTitle>
          <DialogDescription>
            {file ? `Share ${file.name} with a pre-signed URL.` : 'Select a file to share.'}
          </DialogDescription>
        </DialogHeader>

        <div className="space-y-4">
          <div>
            <label className="text-xs font-medium uppercase tracking-wider text-muted-foreground mb-1.5 block">
              URL expiry
            </label>
            <select
              value={expiresIn}
              onChange={(e) => { setExpiresIn(Number(e.target.value)); reset(); }}
              className="w-full bg-secondary text-secondary-foreground border border-border rounded-md px-3 py-2 text-sm"
            >
              {EXPIRY_OPTIONS.map((opt) => (
                <option key={opt.value} value={opt.value}>{opt.label}</option>
              ))}
            </select>
          </div>

          <Button onClick={handleShare} disabled={loading} className="w-full">
            {loading ? 'Uploading...' : 'Get Pre-signed URL'}
          </Button>

          {url && (
            <div className="space-y-2">
              <label className="text-xs font-medium uppercase tracking-wider text-muted-foreground block">
                Share URL
              </label>
              <div className="flex gap-2">
                <Input value={url} readOnly className="font-mono text-xs" />
                <Button variant="secondary" size="sm" onClick={handleCopy}>
                  {copied ? 'Copied!' : 'Copy'}
                </Button>
              </div>
              <p className="text-xs text-muted-foreground">{info}</p>
            </div>
          )}

          {error && (
            <div className="text-sm text-destructive bg-destructive/10 border border-destructive/30 rounded-md px-3 py-2">
              {error}
            </div>
          )}
        </div>
      </DialogContent>
    </Dialog>
  );
}
