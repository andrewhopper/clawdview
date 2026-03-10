/**
 * Base embeddings interface.
 */
export abstract class BaseEmbeddings {
  /** The embedding dimension. */
  abstract readonly dimension: number;

  /** Embed a single text string. */
  abstract embedText(text: string): Promise<number[]>;

  /** Embed multiple text strings. */
  abstract embedTexts(texts: string[]): Promise<number[][]>;

  /** Embed a search query. Override if query embedding differs. */
  async embedQuery(query: string): Promise<number[]> {
    return this.embedText(query);
  }
}
