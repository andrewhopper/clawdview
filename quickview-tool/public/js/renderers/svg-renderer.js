export function renderSVG(container, content) {
  container.innerHTML = `
    <div style="padding: 20px; text-align: center;" class="bg-background">
      ${content}
    </div>
  `;
}
