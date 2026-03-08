export class FileTreeManager {
  constructor(containerId, onFileSelect, preferencesManager) {
    this.container = document.getElementById(containerId);
    this.onFileSelect = onFileSelect;
    this.preferencesManager = preferencesManager || null;
    this.lastTree = null;
  }

  render(fileTree) {
    this.lastTree = fileTree;
    this.container.innerHTML = '';

    const filtered = this.filterTree(fileTree);
    if (filtered && filtered.length > 0) {
      this.renderItems(filtered, this.container);
    } else {
      this.container.innerHTML = '<div class="no-files">No files found</div>';
    }
  }

  filterTree(items) {
    if (!items || !this.preferencesManager) return items;

    return items
      .map(item => {
        if (item.type === 'directory') {
          const children = this.filterTree(item.children);
          if (children && children.length > 0) {
            return { ...item, children };
          }
          return null;
        }
        if (this.preferencesManager.isFileTypeWatched(item.extension)) {
          return item;
        }
        return null;
      })
      .filter(Boolean);
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
