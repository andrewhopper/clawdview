export interface FileTreeItem {
  name: string;
  type: 'file' | 'directory';
  path: string;
  extension?: string;
  size?: number;
  mtime?: number;
  children?: FileTreeItem[];
}

export interface FileData {
  content: string;
  extension: string;
  filename: string;
  path: string;
}

export interface CurrentFile {
  name: string;
  path: string;
  extension: string;
}

export interface Preferences {
  autoOpenOnChange: boolean;
  maxOpenTabs: number;
  watchedFileTypes: string[];
}

export interface FileChangeEvent {
  event: string;
  path: string;
  relativePath: string;
  content: string | null;
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

export interface FileInfoResponse {
  filename: string;
  path: string;
  extension: string;
  size: number;
  inode: number;
  createdAt: string;
  modifiedAt: string;
  permissions: string;
  lines?: number;
  encoding?: string;
  uuids?: string[];
  git?: GitInfo;
  exif?: ExifData;
}

export type ViewMode = 'tree' | 'recent' | 'type';
export type TabName = 'preview' | 'code' | 'output';
