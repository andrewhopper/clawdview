export interface FileTreeItem {
  name: string;
  type: 'file' | 'directory';
  path: string;
  extension?: string;
  size?: number;
  mtime?: number;
  children?: FileTreeItem[];
}

export interface GitInfo {
  status: string;
  branch?: string;
  lastCommit?: {
    hash: string;
    author: string;
    date: string;
    subject: string;
  };
}

export interface ExifData {
  width?: number;
  height?: number;
  cameraMake?: string;
  cameraModel?: string;
  dateTaken?: string;
  exposureTime?: string;
  fNumber?: string;
  iso?: number;
  focalLength?: string;
  gpsLatitude?: number;
  gpsLongitude?: number;
  software?: string;
  copyright?: string;
  description?: string;
}
