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
      .reduce<string[]>((result, line) => {
        const indent = result.length > 0
          ? (result[result.length - 1].search(/\S/) || 0) +
            (result[result.length - 1].includes('{') ? 2 : 0) +
            (line.includes('}') ? -2 : 0)
          : (line.includes('}') ? 0 : 0);
        result.push(' '.repeat(Math.max(0, indent)) + line);
        return result;
      }, [])
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
    const lines = content
      .replace(/></g, '>\n<')
      .split('\n')
      .map((line) => line.trim())
      .filter((line) => line.length > 0);

    let indent = 0;
    return lines
      .map((line) => {
        if (line.match(/<\/[^>]*>/)) indent -= 2;
        const result = ' '.repeat(Math.max(0, indent)) + line;
        if (line.match(/<[^/][^>]*[^/]>/) && !line.match(/<\/[^>]*>/)) indent += 2;
        return result;
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
