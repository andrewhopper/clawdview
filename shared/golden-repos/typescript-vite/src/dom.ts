/**
 * DOM utility functions.
 */

/**
 * Query selector with type safety.
 */
export function $(selector: string): HTMLElement | null {
  return document.querySelector(selector);
}

/**
 * Query selector all with type safety.
 */
export function $$(selector: string): HTMLElement[] {
  return Array.from(document.querySelectorAll(selector));
}

/**
 * Create an HTML element with attributes and children.
 */
export function createElement<K extends keyof HTMLElementTagNameMap>(
  tag: K,
  attrs?: Record<string, string>,
  children?: (string | Node)[]
): HTMLElementTagNameMap[K] {
  const element = document.createElement(tag);

  if (attrs) {
    for (const [key, value] of Object.entries(attrs)) {
      element.setAttribute(key, value);
    }
  }

  if (children) {
    for (const child of children) {
      if (typeof child === 'string') {
        element.appendChild(document.createTextNode(child));
      } else {
        element.appendChild(child);
      }
    }
  }

  return element;
}

/**
 * Add event listener with automatic cleanup.
 */
export function on<K extends keyof HTMLElementEventMap>(
  element: HTMLElement,
  event: K,
  handler: (e: HTMLElementEventMap[K]) => void,
  options?: AddEventListenerOptions
): () => void {
  element.addEventListener(event, handler as EventListener, options);
  return () => element.removeEventListener(event, handler as EventListener, options);
}

/**
 * Toggle a class on an element.
 */
export function toggleClass(element: HTMLElement, className: string, force?: boolean): boolean {
  return element.classList.toggle(className, force);
}

/**
 * Set multiple styles on an element.
 */
export function setStyles(element: HTMLElement, styles: Partial<CSSStyleDeclaration>): void {
  Object.assign(element.style, styles);
}
