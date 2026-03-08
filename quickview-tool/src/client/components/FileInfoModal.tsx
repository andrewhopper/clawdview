import { useState, useEffect } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from './ui/dialog';
import { ScrollArea } from './ui/scroll-area';
import { Separator } from './ui/separator';
import { formatFileSize } from '@/lib/utils';
import type { FileInfoResponse, CurrentFile } from '../types';

interface FileInfoModalProps {
  file: CurrentFile | null;
  isOpen: boolean;
  onClose: () => void;
}

export function FileInfoModal({ file, isOpen, onClose }: FileInfoModalProps) {
  const [info, setInfo] = useState<FileInfoResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!isOpen || !file) return;

    const controller = new AbortController();
    setLoading(true);
    setError(null);

    fetch(`/api/file-info/${file.path}`, { signal: controller.signal })
      .then((res) => {
        if (!res.ok) throw new Error('Failed to load file info');
        return res.json();
      })
      .then((data) => setInfo(data))
      .catch((err) => {
        if (err.name !== 'AbortError') setError(err.message);
      })
      .finally(() => setLoading(false));

    return () => controller.abort();
  }, [isOpen, file]);

  return (
    <Dialog open={isOpen} onOpenChange={(open) => { if (!open) onClose(); }}>
      <DialogContent className="max-w-md max-h-[80vh] flex flex-col">
        <DialogHeader>
          <DialogTitle>{file?.name || 'File Info'}</DialogTitle>
          <DialogDescription>Detailed information about this file.</DialogDescription>
        </DialogHeader>

        <ScrollArea className="flex-1 -mx-6 px-6">
          <div className="space-y-1 text-sm pb-4">
            {loading && (
              <div className="text-center py-3 text-muted-foreground">Loading...</div>
            )}
            {error && (
              <div className="text-destructive">{error}</div>
            )}
            {info && (
              <>
                <InfoSection title="File" rows={[
                  ['Filename', info.filename],
                  ['Path', info.path],
                  ['Extension', info.extension || 'None'],
                  ['Inode', String(info.inode)],
                  ['Size', formatFileSize(info.size)],
                  ...(info.lines != null ? [['Lines', info.lines.toLocaleString()] as [string, string]] : []),
                  ['Modified', new Date(info.modifiedAt).toLocaleString()],
                  ['Created', new Date(info.createdAt).toLocaleString()],
                  ['Permissions', info.permissions],
                  ...(info.encoding ? [['Encoding', info.encoding] as [string, string]] : []),
                ]} />

                {info.git && (
                  <>
                    <Separator className="my-3" />
                    <InfoSection title="Git" rows={[
                      ['Status', info.git.status],
                      ...(info.git.branch ? [['Branch', info.git.branch] as [string, string]] : []),
                      ...(info.git.lastCommit ? [
                        ['Last Commit', info.git.lastCommit.hash.substring(0, 8)] as [string, string],
                        ['Author', info.git.lastCommit.author] as [string, string],
                        ['Date', new Date(info.git.lastCommit.date).toLocaleString()] as [string, string],
                        ['Message', info.git.lastCommit.subject] as [string, string],
                      ] : []),
                    ]} />
                  </>
                )}

                {info.uuids && info.uuids.length > 0 && (
                  <>
                    <Separator className="my-3" />
                    <InfoSection
                      title="UUIDs Found"
                      rows={info.uuids.map((uuid, i) => [
                        `UUID ${info.uuids!.length > 1 ? i + 1 : ''}`.trim(),
                        uuid,
                      ])}
                    />
                  </>
                )}

                {info.exif && (
                  <>
                    <Separator className="my-3" />
                    <InfoSection title="EXIF Data" rows={
                      Object.entries(info.exif)
                        .filter(([, v]) => v != null)
                        .map(([key, value]) => {
                          const labels: Record<string, string> = {
                            width: 'Width', height: 'Height',
                            cameraMake: 'Camera Make', cameraModel: 'Camera Model',
                            dateTaken: 'Date Taken', exposureTime: 'Exposure',
                            fNumber: 'Aperture', iso: 'ISO',
                            focalLength: 'Focal Length',
                            gpsLatitude: 'GPS Lat', gpsLongitude: 'GPS Lon',
                            software: 'Software', copyright: 'Copyright',
                            description: 'Description',
                          };
                          let display = String(value);
                          if (key === 'dateTaken') display = new Date(value as string).toLocaleString();
                          if (key === 'width' || key === 'height') display = `${value}px`;
                          return [labels[key] || key, display] as [string, string];
                        })
                    } />
                  </>
                )}
              </>
            )}
          </div>
        </ScrollArea>
      </DialogContent>
    </Dialog>
  );
}

function InfoSection({ title, rows }: { title: string; rows: [string, string][] }) {
  return (
    <div>
      <div className="text-xs font-semibold uppercase tracking-wider text-muted-foreground py-2">
        {title}
      </div>
      {rows.map(([label, value], i) => (
        <div key={`${label}-${i}`} className="flex justify-between items-baseline py-1.5 border-b border-border/50 last:border-b-0">
          <span className="text-sm text-muted-foreground shrink-0">{label}</span>
          <span className="text-sm text-foreground font-mono text-right break-all ml-4">{value}</span>
        </div>
      ))}
    </div>
  );
}
