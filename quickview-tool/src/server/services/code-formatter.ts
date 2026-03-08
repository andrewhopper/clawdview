export class CodeFormatter {
  formatJavaScript(content: string): string {
    return content
      .replace(/([^=!<>])=([^=])/g, '$1 = $2')
      .replace(/([^=!<>])==([^=])/g, '$1 == $2')
      .replace(/([^=!<>])===([^=])/g, '$1 === $2')
      .replace(/\{([^\s])/g, '{ $1')
      .replace(/([^\s])\}/g, '$1 }')
      .split('\n')
      .map((line) => line.trim())
      .map((line, i, arr) => {
        let indent = 0;
        for (let j = 0; j < i; j++) {
          const prevLine = arr[j];
          if (prevLine.includes('{')) indent += 2;
          if (prevLine.includes('}')) indent -= 2;
        }
        if (line.includes('}')) indent -= 2;
        return ' '.repeat(Math.max(0, indent)) + line;
      })
      .join('\n');
  }

  formatJSON(content: string): string {
    try {
      return JSON.stringify(JSON.parse(content), null, 2);
    } catch {
      throw new Error('Invalid JSON content');
    }
  }

  formatHTML(content: string): string {
    return content
      .replace(/></g, '>\n<')
      .split('\n')
      .map((line) => line.trim())
      .filter((line) => line.length > 0)
      .map((line, i, arr) => {
        let indent = 0;
        for (let j = 0; j < i; j++) {
          const prevLine = arr[j];
          if (prevLine.match(/<[^/][^>]*[^/]>/)) indent += 2;
          if (prevLine.match(/<\/[^>]*>/)) indent -= 2;
        }
        if (line.match(/<\/[^>]*>/)) indent -= 2;
        return ' '.repeat(Math.max(0, indent)) + line;
      })
      .join('\n');
  }

  formatCSS(content: string): string {
    return content
      .replace(/\{/g, ' {\n  ')
      .replace(/\}/g, '\n}\n')
      .replace(/:\s*([^;]+);/g, ': $1;')
      .replace(/;\s*([^}])/g, ';\n  $1')
      .replace(/\n\s*\n/g, '\n')
      .trim();
  }

  format(content: string, extension: string): string {
    switch (extension) {
      case '.js':
      case '.jsx':
        return this.formatJavaScript(content);
      case '.json':
        return this.formatJSON(content);
      case '.html':
        return this.formatHTML(content);
      case '.css':
        return this.formatCSS(content);
      default:
        throw new Error('File type not supported for formatting');
    }
  }
}
