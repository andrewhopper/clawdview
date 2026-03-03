export function renderHTML(container, content) {
  const iframe = document.createElement('iframe');
  iframe.className = 'preview-iframe';
  iframe.srcdoc = content;
  container.innerHTML = '';
  container.appendChild(iframe);
}
