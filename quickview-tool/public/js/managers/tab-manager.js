export class TabManager {
  constructor() {
    this.tabs = document.querySelectorAll('.tab');
    this.panels = document.querySelectorAll('.panel');
    this.setup();
    this.setupKeyboardShortcuts();
  }

  setup() {
    this.tabs.forEach(tab => {
      tab.addEventListener('click', () => {
        const targetPanel = tab.dataset.tab;
        this.tabs.forEach(t => t.classList.remove('active'));
        this.panels.forEach(p => p.classList.remove('active'));
        tab.classList.add('active');
        document.getElementById(`${targetPanel}-panel`).classList.add('active');
      });
    });
  }

  setupKeyboardShortcuts() {
    document.addEventListener('keydown', (e) => {
      if ((e.metaKey || e.ctrlKey) && e.shiftKey && (e.key === 'ArrowLeft' || e.key === 'ArrowRight')) {
        e.preventDefault();
        const tabsArray = Array.from(this.tabs);
        const activeIndex = tabsArray.findIndex(t => t.classList.contains('active'));
        let nextIndex;

        if (e.key === 'ArrowRight') {
          nextIndex = (activeIndex + 1) % tabsArray.length;
        } else {
          nextIndex = (activeIndex - 1 + tabsArray.length) % tabsArray.length;
        }

        tabsArray[nextIndex].click();
      }
    });
  }

  switchTo(tabName) {
    const tab = document.querySelector(`[data-tab="${tabName}"]`);
    if (tab) tab.click();
  }
}
