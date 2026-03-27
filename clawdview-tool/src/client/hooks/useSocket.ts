import { useEffect, useRef, useState, useCallback } from 'react';
import { io, Socket } from 'socket.io-client';
import type { FileTreeItem, FileChangeEvent, WatchedDirInfo } from '../types';

export function useSocket(
  onFileTree: (tree: FileTreeItem[]) => void,
  onFileChange: (data: FileChangeEvent) => void,
  onWatchedDirs: (dirs: WatchedDirInfo[]) => void,
) {
  const [connected, setConnected] = useState(false);
  const socketRef = useRef<Socket | null>(null);
  const onFileTreeRef = useRef(onFileTree);
  const onFileChangeRef = useRef(onFileChange);
  const onWatchedDirsRef = useRef(onWatchedDirs);

  onFileTreeRef.current = onFileTree;
  onFileChangeRef.current = onFileChange;
  onWatchedDirsRef.current = onWatchedDirs;

  useEffect(() => {
    const socket = io();
    socketRef.current = socket;

    socket.on('connect', () => setConnected(true));
    socket.on('disconnect', () => setConnected(false));
    socket.on('fileTree', (tree: FileTreeItem[]) => onFileTreeRef.current(tree));
    socket.on('fileChange', (data: FileChangeEvent) => onFileChangeRef.current(data));
    socket.on('watchedDirs', (dirs: WatchedDirInfo[]) => onWatchedDirsRef.current(dirs));

    return () => {
      socket.disconnect();
    };
  }, []);

  const requestRefresh = useCallback(() => {
    socketRef.current?.emit('refreshFiles');
  }, []);

  const addDir = useCallback((dir: string) => {
    socketRef.current?.emit('addDir', dir);
  }, []);

  const removeDir = useCallback((dir: string) => {
    socketRef.current?.emit('removeDir', dir);
  }, []);

  return { connected, requestRefresh, addDir, removeDir };
}
