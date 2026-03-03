export class SocketManager {
  constructor(onFileTree, onFileChange) {
    this.socket = window.io();
    this.onFileTree = onFileTree;
    this.onFileChange = onFileChange;
    this.setup();
  }

  setup() {
    this.socket.on('connect', () => {
      document.getElementById('status').className = 'status connected';
    });

    this.socket.on('disconnect', () => {
      document.getElementById('status').className = 'status disconnected';
    });

    this.socket.on('fileTree', (tree) => this.onFileTree(tree));
    this.socket.on('fileChange', (data) => this.onFileChange(data));
  }

  requestRefresh() {
    this.socket.emit('refreshFiles');
  }
}
