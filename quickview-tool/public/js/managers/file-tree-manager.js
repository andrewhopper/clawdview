export class FileTreeManager {
  constructor(containerId, onFileSelect) {
    this.container = document.getElementById(containerId);
    this.onFileSelect = onFileSelect;
  }

  render(fileTree) {
    this.container.innerHTML = '';
    if (fileTree && fileTree.length > 0) {
      this.renderItems(fileTree, this.container);
    } else {
      this.container.innerHTML = '<div class="no-files">No files found</div>';
    }
  }

  renderItems(items, container, level = 0) {
    items.forEach(item => {
      const element = document.createElement('div');
      element.className = `file-item ${item.type} ${this.getFileClass(item.extension)}`;
      element.style.paddingLeft = `${12 + (level * 16)}px`;
      element.textContent = item.name;

      if (item.type === 'file') {
        element.addEventListener('click', () => {
          document.querySelectorAll('.file-item.selected').forEach(el => el.classList.remove('selected'));
          element.classList.add('selected');
          this.onFileSelect(item);
        });
      }

      container.appendChild(element);

      if (item.children && item.children.length > 0) {
        this.renderItems(item.children, container, level + 1);
      }
    });
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
