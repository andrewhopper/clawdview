import type { GitInfo, ExifData } from '../shared/types';
export type { FileTreeItem, GitInfo, ExifData } from '../shared/types';

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
