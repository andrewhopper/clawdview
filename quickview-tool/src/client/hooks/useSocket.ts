import { useEffect, useRef, useState, useCallback } from 'react';
import { io, Socket } from 'socket.io-client';
import type { FileTreeItem, FileChangeEvent } from '../types';

export function useSocket(
  onFileTree: (tree: FileTreeItem[]) => void,
  onFileChange: (data: FileChangeEvent) => void,
) {
  const [connected, setConnected] = useState(false);
  const socketRef = useRef<Socket | null>(null);
  const onFileTreeRef = useRef(onFileTree);
  const onFileChangeRef = useRef(onFileChange);

  onFileTreeRef.current = onFileTree;
  onFileChangeRef.current = onFileChange;

  useEffect(() => {
    const socket = io();
    socketRef.current = socket;

    socket.on('connect', () => setConnected(true));
    socket.on('disconnect', () => setConnected(false));
    socket.on('fileTree', (tree: FileTreeItem[]) => onFileTreeRef.current(tree));
    socket.on('fileChange', (data: FileChangeEvent) => onFileChangeRef.current(data));

    return () => {
      socket.disconnect();
    };
  }, []);

  const requestRefresh = useCallback(() => {
    socketRef.current?.emit('refreshFiles');
  }, []);

  return { connected, requestRefresh };
}
