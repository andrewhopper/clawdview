declare module 'exif-parser' {
  interface ExifResult {
    tags: Record<string, any>;
    imageSize?: {
      width: number;
      height: number;
    };
  }

  interface ExifParser {
    enableSimpleValues(enable: boolean): void;
    parse(): ExifResult;
  }

  function create(buffer: Buffer): ExifParser;

  export = { create };
}
