/**
 * TTS Domain Model - TypeScript Types
 * Auto-generated from ontology.ttl
 * Version: 1.0.0
 */

// ----------------
// ENUMS
// ----------------

export enum ProviderType {
  ElevenLabs = 'elevenlabs',
  AWSPolly = 'aws_polly',
  OpenAI = 'openai',
  GoogleTTS = 'google_tts',
  Azure = 'azure',
}

export enum AudioFormat {
  MP3 = 'mp3',
  WAV = 'wav',
  OGG = 'ogg',
  PCM = 'pcm',
  FLAC = 'flac',
}

export enum SynthesisStatus {
  Pending = 'pending',
  Processing = 'processing',
  Completed = 'completed',
  Failed = 'failed',
  Streaming = 'streaming',
}

export enum DeliveryMode {
  FileGeneration = 'file_generation',
  RealTimeStream = 'realtime_stream',
  WebSocket = 'websocket',
}

export enum ModelType {
  MultilingualV2 = 'eleven_multilingual_v2',
  TurboV2 = 'eleven_turbo_v2',
  TurboV2_5 = 'eleven_turbo_v2_5',
  Neural = 'neural',
  Standard = 'standard',
}

// ----------------
// ENTITIES
// ----------------

export interface VoiceSettings {
  /** Voice stability (0.0-1.0). Higher = more consistent, lower = more expressive */
  stability: number;
  /** Voice clarity/similarity (0.0-1.0). Higher = clearer, more similar to original */
  similarityBoost: number;
  /** Style exaggeration (0.0-1.0). Higher = more expressive */
  style: number;
  /** Enhance similarity to original speaker */
  useSpeakerBoost: boolean;
  /** Speaking rate (0.5-2.0). 1.0 = normal */
  speed?: number;
  /** Voice pitch adjustment (-20 to +20 semitones) */
  pitch?: number;
}

export interface Voice {
  /** Provider-specific voice identifier */
  id: string;
  /** Human-readable voice name */
  name: string;
  /** TTS provider for this voice */
  provider: ProviderType;
  /** ISO language code (en, en-US, es, fr) */
  language: string;
  /** Voice description */
  description?: string;
  /** URL to voice preview audio sample */
  previewUrl?: string;
  /** Whether voice is a cloned custom voice */
  isCloned?: boolean;
  /** male, female, neutral */
  gender?: string;
  /** young, middle-aged, old */
  ageGroup?: string;
  /** narration, conversational, news, meditation, video-game */
  useCase?: string;
}

export interface Provider {
  /** Provider name */
  name: string;
  /** Provider type */
  type: ProviderType;
  /** API endpoint URL */
  apiEndpoint?: string;
  /** Whether provider supports streaming */
  supportsStreaming: boolean;
  /** Whether provider supports voice cloning */
  supportsVoiceCloning: boolean;
  /** Supported audio formats */
  supportedFormats: AudioFormat[];
  /** Supported languages (ISO codes) */
  supportedLanguages: string[];
  /** Rate limit (requests per minute) */
  rateLimit?: number;
  /** USD cost per character */
  costPerChar?: number;
}

export interface SynthesisRequest {
  /** Unique request identifier */
  id: string;
  /** Text content to convert to speech */
  text: string;
  /** Voice to use for synthesis */
  voice?: Voice;
  /** Voice ID (alternative to voice object) */
  voiceId?: string;
  /** Provider to use */
  provider?: ProviderType;
  /** Output audio format */
  outputFormat: AudioFormat;
  /** Delivery mode (file or stream) */
  deliveryMode: DeliveryMode;
  /** Model to use for synthesis */
  model?: ModelType;
  /** Voice settings for fine-tuning */
  voiceSettings?: VoiceSettings;
  /** Request timestamp */
  requestedAt: Date;
  /** Callback URL for async completion */
  callbackUrl?: string;
}

export interface AudioFile {
  /** Audio format */
  format: AudioFormat;
  /** Local file path */
  filePath?: string;
  /** Remote URL (S3, CDN) */
  fileUrl?: string;
  /** Time-limited access URL */
  presignedUrl?: string;
  /** When presigned URL expires */
  expiresAt?: Date;
  /** File size in bytes */
  sizeBytes: number;
  /** Duration in milliseconds */
  durationMs: number;
  /** Sample rate in Hz */
  sampleRate: number;
  /** Bitrate in kbps */
  bitrate?: number;
  /** Number of channels (1=mono, 2=stereo) */
  channels: number;
  /** SHA256 content hash for deduplication */
  contentHash?: string;
}

export interface UsageMetrics {
  /** Number of characters processed */
  characterCount: number;
  /** Estimated cost in USD */
  estimatedCost: number;
  /** Provider used for synthesis */
  providerUsed: ProviderType;
  /** Model used for synthesis */
  modelUsed?: ModelType;
  /** Voice used for synthesis */
  voiceUsed?: Voice;
}

export interface SynthesisResult {
  /** Reference to original request */
  requestId: string;
  /** Synthesis status */
  status: SynthesisStatus;
  /** Generated audio file (if file delivery mode) */
  audioFile?: AudioFile;
  /** Raw audio data (base64) */
  audioData?: string;
  /** Error message if failed */
  errorMessage?: string;
  /** Processing time in milliseconds */
  processingTimeMs: number;
  /** Completion timestamp */
  completedAt?: Date;
  /** Usage metrics */
  usageMetrics?: UsageMetrics;
}

export interface StreamChunk {
  /** Audio data chunk (base64) */
  data: string;
  /** Chunk index in sequence */
  index: number;
  /** Whether this is the last chunk */
  isLast: boolean;
}

// ----------------
// TYPE GUARDS
// ----------------

export function isValidAudioFormat(value: string): value is AudioFormat {
  return Object.values(AudioFormat).includes(value as AudioFormat);
}

export function isValidProviderType(value: string): value is ProviderType {
  return Object.values(ProviderType).includes(value as ProviderType);
}

export function isValidSynthesisStatus(value: string): value is SynthesisStatus {
  return Object.values(SynthesisStatus).includes(value as SynthesisStatus);
}

// ----------------
// DEFAULTS
// ----------------

export const DEFAULT_VOICE_SETTINGS: VoiceSettings = {
  stability: 0.5,
  similarityBoost: 0.75,
  style: 0.0,
  useSpeakerBoost: true,
  speed: 1.0,
};

export const DEFAULT_AUDIO_FORMAT = AudioFormat.MP3;
export const DEFAULT_DELIVERY_MODE = DeliveryMode.FileGeneration;
export const DEFAULT_MODEL = ModelType.MultilingualV2;
