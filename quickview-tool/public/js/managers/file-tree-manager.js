export class FileTreeManager {
  constructor(containerId, onFileSelect) {
    this.container = document.getElementById(containerId);
    this.onFileSelect = onFileSelect;
    this.files = [];
    this.currentIndex = -1;
  }

  render(fileTree) {
    this.container.innerHTML = '';
    this.files = [];
    if (fileTree && fileTree.length > 0) {
      this.collectFiles(fileTree);
      this.renderItems(fileTree, this.container);
      // Restore selection if the current file is still in the list
      if (this.currentIndex >= this.files.length) {
        this.currentIndex = this.files.length - 1;
      }
    } else {
      this.container.innerHTML = '<div class="no-files">No files found</div>';
      this.currentIndex = -1;
    }
  }

  collectFiles(items) {
    items.forEach(item => {
      if (item.type === 'file') {
        this.files.push(item);
      }
      if (item.children && item.children.length > 0) {
        this.collectFiles(item.children);
      }
    });
  }

  renderItems(items, container, level = 0) {
    items.forEach(item => {
      const element = document.createElement('div');
      element.className = `file-item ${item.type} ${this.getFileClass(item.extension)}`;
      element.style.paddingLeft = `${12 + (level * 16)}px`;
      element.textContent = item.name;

      if (item.type === 'file') {
        const fileIndex = this.files.indexOf(item);
        element.dataset.fileIndex = fileIndex;
        element.addEventListener('click', () => {
          this.selectByIndex(fileIndex);
        });
      }

      container.appendChild(element);

      if (item.children && item.children.length > 0) {
        this.renderItems(item.children, container, level + 1);
      }
    });
  }

  selectByIndex(index) {
    if (index < 0 || index >= this.files.length) return;
    this.currentIndex = index;
    document.querySelectorAll('.file-item.selected').forEach(el => el.classList.remove('selected'));
    const el = this.container.querySelector(`[data-file-index="${index}"]`);
    if (el) {
      el.classList.add('selected');
      el.scrollIntoView({ block: 'nearest' });
    }
    this.onFileSelect(this.files[index]);
  }

  selectNext() {
    if (this.files.length === 0) return;
    const next = this.currentIndex < this.files.length - 1 ? this.currentIndex + 1 : 0;
    this.selectByIndex(next);
  }

  selectPrevious() {
    if (this.files.length === 0) return;
    const prev = this.currentIndex > 0 ? this.currentIndex - 1 : this.files.length - 1;
    this.selectByIndex(prev);
  }

  getFileCount() {
    return this.files.length;
  }

  getCurrentIndex() {
    return this.currentIndex;
  }

  getFileClass(extension) {
    if (!extension) return 'file';
    const ext = extension.toLowerCase().replace('.', '');
    const classMap = {
      html: 'html', js: 'js', jsx: 'js', py: 'py',
      json: 'json', md: 'md', svg: 'svg', css: 'css'
    };
    return classMap[ext] || 'file';
  }
}
