export class TabManager {
  constructor() {
    this.tabs = document.querySelectorAll('.tab');
    this.panels = document.querySelectorAll('.panel');
    this.setup();
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

  switchTo(tabName) {
    const tab = document.querySelector(`[data-tab="${tabName}"]`);
    if (tab) tab.click();
  }
}
