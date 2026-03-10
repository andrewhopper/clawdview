/**
 * Human Task Domain Model - TypeScript Types
 * Generated from: shared/semantic/domains/human-task/schema.yaml
 * Version: 1.0.0
 *
 * Human-in-the-loop review and approval of AI-generated content
 *
 * DO NOT EDIT MANUALLY - Regenerate with: npm run generate:types
 */

// ============================================
// Shared Constructs
// ============================================

/**
 * Abstraction over who/what is performing an action
 */
export interface Actor {
  /** Actor type */
  type: ActorType;

  /** ID in appropriate domain */
  id: string;

  /** Cached display name */
  displayName?: string;
}

/**
 * Reference to entity in another domain
 */
export interface ExternalRef {
  /** Domain name */
  domain: string;

  /** Entity type */
  entity: string;

  /** ID in external domain */
  id: string;

  /** Version for optimistic locking */
  version?: number;
}

/**
 * Instance of feedback on a specific dimension
 */
export interface FeedbackSignal {
  /** FK to FeedbackDimension */
  dimensionId: string;

  /** Normalized value */
  value: number;

  /** How captured */
  sourceModality: Modality;

  /** Original input */
  rawInput?: string;

  /** NLU confidence */
  confidence?: number;
}

// ============================================
// Core Task Entities
// ============================================

/**
 * A unit of work requiring judgment from an actor
 */
export interface Task {
  /** Unique identifier */
  id: string;

  /** FK to TaskType */
  typeId: string;

  /** Who should review */
  assignedTo: Actor;

  /** Current status */
  status: TaskStatus;

  /** Content to review */
  input: TaskInput;

  /** Computed priority for queue ordering */
  priority: Priority;

  /** What created this task */
  source: Actor;

  /** Reference to origin entity */
  sourceRef?: ExternalRef;

  /** Cross-system tracing */
  correlationId?: string;

  /** For filtering/sorting */
  contextTags?: string[];

  /** AI suggestion */
  recommendation?: Recommendation;

  /** Blocking tasks */
  dependencies?: TaskDependency[];

  /** What this affects */
  impacts?: DownstreamImpact[];

  /** Soft deadline */
  dueAt?: Date;

  /** Hard deadline */
  expiresAt?: Date;

  /** When resolved */
  completedAt?: Date;

  /** When created */
  createdAt: Date;

  /** Last modification */
  updatedAt: Date;
}

/**
 * Content to be reviewed
 */
export interface TaskInput {
  /** For minimal UI/voice (max 50 chars) */
  brief: string;

  /** Scannable summary (max 200 chars) */
  summary: string;

  /** Full content, validated by TaskType.inputSchema */
  payload: unknown;

  /** Attachments */
  attachments?: Attachment[];

  /** Input context */
  context?: InputContext;
}

/**
 * The outcome of an actor's judgment
 */
export interface TaskDecision {
  /** Unique identifier */
  id: string;

  /** FK to Task */
  taskId: string;

  /** Who decided */
  actor: Actor;

  /** FK to ActionType */
  actionId: string;

  /** Nuanced feedback */
  feedback?: FeedbackSignal[];

  /** Free-form text */
  note?: string;

  /** Voice/file reference */
  noteAttachmentRef?: ExternalRef;

  /** Matched AI suggestion? */
  followedRecommendation?: boolean;

  /** Time to decide (ms) */
  latencyMs?: number;

  /** When decided */
  createdAt: Date;
}

/**
 * A deferred task with trigger conditions
 */
export interface Reminder {
  /** Unique identifier */
  id: string;

  /** FK to Task */
  taskId: string;

  /** Who set reminder */
  actor: Actor;

  /** Time, location, event, or context */
  trigger: ReminderTrigger;

  /** Current state */
  status: ReminderStatus;

  /** Notification reference when fired */
  notificationRef?: ExternalRef;

  /** When fired */
  triggeredAt?: Date;

  /** When set */
  createdAt: Date;

  /** Last modification */
  updatedAt: Date;
}

/**
 * Tasks that must be reviewed together
 */
export interface TaskBundle {
  /** Unique identifier */
  id: string;

  /** Bundle name */
  name: string;

  /** What this bundle represents */
  description?: string;

  /** Bundle type */
  bundleType: BundleType;

  /** Tasks in bundle */
  tasks: BundleTask[];

  /** Current state */
  status: BundleStatus;

  /** FK to ApprovalPattern */
  approvalPatternId: string;

  /** What created bundle */
  source: Actor;

  /** Reference to origin */
  sourceRef?: ExternalRef;

  /** When created */
  createdAt: Date;

  /** Last modification */
  updatedAt: Date;

  /** When resolved */
  completedAt?: Date;
}

// ============================================
// Configuration Entities
// ============================================

/**
 * Defines a category of human tasks
 */
export interface TaskType {
  /** Unique identifier */
  id: string;

  /** Display name */
  name: string;

  /** What this type represents */
  description?: string;

  /** Validates TaskInput.payload */
  inputSchema: Record<string, unknown>;

  /** FK to ActionType[] */
  availableActions: string[];

  /** Which dimensions apply */
  feedbackDimensions?: DimensionRef[];

  /** Default multi-reviewer pattern */
  defaultApprovalPatternId?: string;

  /** Enabled */
  isActive: boolean;

  /** When created */
  createdAt: Date;

  /** Last modification */
  updatedAt: Date;
}

/**
 * Defines an action an actor can take
 */
export interface ActionType {
  /** Unique identifier */
  id: string;

  /** Display name */
  name: string;

  /** What this action means */
  description?: string;

  /** Completes the task? */
  isTerminal: boolean;

  /** Must provide feedback */
  requiresFeedback?: boolean;

  /** When created */
  createdAt: Date;

  /** Last modification */
  updatedAt: Date;
}

/**
 * Defines an axis for feedback
 */
export interface FeedbackDimension {
  /** Unique identifier */
  id: string;

  /** Display name */
  name: string;

  /** What this measures */
  description?: string;

  /** Scale type */
  scaleType: ScaleType;

  /** Scale minimum */
  minValue: number;

  /** Scale maximum */
  maxValue: number;

  /** Initial value */
  defaultValue: number;

  /** Min label */
  minLabel: string;

  /** Max label */
  maxLabel: string;

  /** Middle label */
  midLabel?: string;

  /** For discrete scales */
  discreteOptions?: DiscreteOption[];

  /** When created */
  createdAt: Date;

  /** Last modification */
  updatedAt: Date;
}

/**
 * Configures multi-reviewer decision aggregation
 */
export interface ApprovalPattern {
  /** Unique identifier */
  id: string;

  /** Display name */
  name: string;

  /** Pattern type */
  type: ApprovalPatternType;

  /** For quorum (0.0-1.0) */
  threshold?: number;

  /** Minimum required */
  minReviewers?: number;

  /** Auto-decide after hours */
  timeoutHours?: number;

  /** Tie breaker strategy */
  tieBreaker?: TieBreakerStrategy;

  /** When created */
  createdAt: Date;

  /** Last modification */
  updatedAt: Date;
}

// ============================================
// Priority Types
// ============================================

/**
 * Task priority for queue ordering
 */
export interface Priority {
  /** 0.0-1.0, higher = more urgent */
  score: number;

  /** Human-readable explanation */
  reason?: string;

  /** Components that contributed */
  factors?: PriorityFactor[];

  /** When calculated */
  computedAt: Date;

  /** Manual adjustment */
  override?: PriorityOverride;
}

/**
 * Factor contributing to priority score
 */
export interface PriorityFactor {
  /** Factor name */
  name: string;

  /** Factor weight */
  weight: number;

  /** Factor value */
  value: number;

  /** weight * value */
  contribution: number;
}

/**
 * Actor-level priority adjustment
 */
export interface PriorityOverride {
  /** Who made adjustment */
  actor: Actor;

  /** -1.0 to +1.0 adjustment */
  adjustment: number;

  /** Why adjusted */
  reason?: string;

  /** Auto-remove after */
  expiresAt?: Date;
}

// ============================================
// Recommendation Types
// ============================================

/**
 * AI recommendation for a task
 */
export interface Recommendation {
  /** Recommended action ID */
  actionId: string;

  /** Confidence (0.0-1.0) */
  confidence: number;

  /** Strength tier */
  strength: RecommendationStrength;

  /** Why this recommendation */
  reasoning?: string;

  /** Alternative options */
  alternatives?: RecommendationAlternative[];

  /** When generated */
  createdAt: Date;
}

/**
 * Alternative recommendation
 */
export interface RecommendationAlternative {
  /** Action ID */
  actionId: string;

  /** Confidence */
  confidence: number;
}

// ============================================
// Supporting Types
// ============================================

export interface Attachment {
  id: string;
  name: string;
  mimeType: string;
  sizeBytes: number;
  url: string;
}

export interface InputContext {
  relatedEntities?: ExternalRef[];
  metadata?: Record<string, unknown>;
}

export interface TaskDependency {
  taskId: string;
  type: DependencyType;
}

export interface DownstreamImpact {
  type: ImpactType;
  severity: ImpactSeverity;
  description: string;
  affectedEntities?: ExternalRef[];
}

export interface BundleTask {
  taskId: string;
  order?: number;
  isRequired: boolean;
}

export interface DimensionRef {
  dimensionId: string;
  isRequired?: boolean;
}

export interface DiscreteOption {
  value: number;
  label: string;
}

// ============================================
// Enums
// ============================================

export enum ActorType {
  USER = 'USER',
  SYSTEM = 'SYSTEM',
  SERVICE = 'SERVICE',
  AUTOMATION = 'AUTOMATION',
  DELEGATE = 'DELEGATE',
  AGENT = 'AGENT',
}

export enum TaskStatus {
  PENDING = 'PENDING',
  ACTIVE = 'ACTIVE',
  DEFERRED = 'DEFERRED',
  COMPLETED = 'COMPLETED',
  EXPIRED = 'EXPIRED',
  CANCELLED = 'CANCELLED',
}

export enum ReminderStatus {
  PENDING = 'PENDING',
  TRIGGERED = 'TRIGGERED',
  DISMISSED = 'DISMISSED',
  EXPIRED = 'EXPIRED',
}

export enum BundleType {
  PARALLEL = 'PARALLEL',
  SEQUENTIAL = 'SEQUENTIAL',
  ATOMIC = 'ATOMIC',
  CONDITIONAL = 'CONDITIONAL',
}

export enum BundleStatus {
  PENDING = 'PENDING',
  ACTIVE = 'ACTIVE',
  PARTIAL = 'PARTIAL',
  COMPLETED = 'COMPLETED',
  FAILED = 'FAILED',
  CANCELLED = 'CANCELLED',
}

export enum ApprovalPatternType {
  SINGLE = 'SINGLE',
  ANY = 'ANY',
  ALL = 'ALL',
  MAJORITY = 'MAJORITY',
  QUORUM = 'QUORUM',
  WEIGHTED = 'WEIGHTED',
}

export enum TieBreakerStrategy {
  REJECT = 'REJECT',
  APPROVE = 'APPROVE',
  ESCALATE = 'ESCALATE',
  OLDEST = 'OLDEST',
  DEFER = 'DEFER',
}

export enum RecommendationStrength {
  STRONG = 'STRONG',       // >= 0.90
  MODERATE = 'MODERATE',   // 0.70-0.89
  WEAK = 'WEAK',          // 0.50-0.69
  NONE = 'NONE',          // < 0.50
}

export enum ScaleType {
  CONTINUOUS = 'CONTINUOUS',
  DISCRETE = 'DISCRETE',
  BINARY = 'BINARY',
}

export enum DependencyType {
  REQUIRES_APPROVAL = 'REQUIRES_APPROVAL',
  REQUIRES_COMPLETION = 'REQUIRES_COMPLETION',
  REQUIRES_DATA = 'REQUIRES_DATA',
  CONFLICTS_WITH = 'CONFLICTS_WITH',
  SUPERSEDES = 'SUPERSEDES',
}

export enum ImpactType {
  SYSTEM = 'SYSTEM',
  PROCESS = 'PROCESS',
  FINANCIAL = 'FINANCIAL',
  COMMUNICATION = 'COMMUNICATION',
  ACCESS = 'ACCESS',
  DATA = 'DATA',
  EXTERNAL = 'EXTERNAL',
}

export enum ImpactSeverity {
  INFO = 'INFO',
  LOW = 'LOW',
  MEDIUM = 'MEDIUM',
  HIGH = 'HIGH',
  CRITICAL = 'CRITICAL',
}

export enum Modality {
  VISUAL_TOUCH = 'VISUAL_TOUCH',
  VISUAL_CLICK = 'VISUAL_CLICK',
  VOICE = 'VOICE',
  VOICE_WITH_DISPLAY = 'VOICE_WITH_DISPLAY',
  HAPTIC = 'HAPTIC',
  AMBIENT = 'AMBIENT',
}

// ============================================
// Reminder Trigger Types
// ============================================

export type ReminderTrigger =
  | TimeBasedTrigger
  | LocationBasedTrigger
  | EventBasedTrigger
  | ContextBasedTrigger;

export interface TimeBasedTrigger {
  type: 'time';
  at: Date;
}

export interface LocationBasedTrigger {
  type: 'location';
  placeRef: ExternalRef;
  condition: 'arrive' | 'leave';
  radiusMeters?: number;
}

export interface EventBasedTrigger {
  type: 'event';
  eventRef: ExternalRef;
  condition: 'before' | 'after' | 'during';
  offsetMinutes?: number;
}

export interface ContextBasedTrigger {
  type: 'context';
  contextId: string;
  condition: string;
}
