/**
 * Story Domain Model - TypeScript Types
 * Generated from: shared/domain-models/story/ontology.ttl
 * Version: 1.0.0
 * Standards: W3C RDF, OWL, SHACL
 *
 * Based on analysis of 10 classic children's books
 *
 * DO NOT EDIT MANUALLY - This file is auto-generated
 * To regenerate: /generate-domain story --lang typescript
 */

// ============================================
// Core Entity Types
// ============================================

/**
 * Complete narrative with metadata, genre, status, and timeline
 */
export interface Story {
  /** Unique identifier */
  id: string;

  /** Story title (1-200 characters) */
  title: string;

  /** Story author */
  author?: string;

  /** Publication year */
  publicationYear?: number;

  /** Current status */
  status: StoryStatus;

  /** Story genre */
  genre?: GenreType;

  /** Story timeline with time points and duration */
  timeline?: StoryTimeline;

  /** Characters in story (at least one required) */
  characters: Character[];

  /** Scenes in story (at least one required) */
  scenes: Scene[];

  /** Themes explored in story */
  themes?: Theme[];

  /** Plot structure */
  plot?: Plot;

  /** Conflicts in story */
  conflicts?: Conflict[];

  /** Visual style (for illustrated books) */
  visualStyle?: VisualStyle;

  /** Linguistic constraints (word count, vocabulary limits) */
  linguisticConstraints?: LinguisticConstraints;

  /** Seasonal progression */
  seasonalProgression?: SeasonalProgression;
}

/**
 * Person, animal, or entity in story with role, traits, and transformations over time
 */
export interface Character {
  /** Unique identifier */
  id: string;

  /** Character name */
  name: string;

  /** Character type (human, animal, anthropomorphic, etc.) */
  characterType: CharacterType;

  /** Role in story */
  role: CharacterRole;

  /** Species (for animals) */
  species?: string;

  /** Anthropomorphic traits (for anthropomorphic animals) */
  anthropomorphicTraits?: AnthropomorphicTrait[];

  /** Character description */
  description?: string;

  /** Appearances at different time points (for aging/transformation) */
  appearanceAtTime?: CharacterAtTime[];

  /** Group membership */
  groupMembership?: { groupId: string; role?: string };

  /** Character arc */
  arc?: Arc;
}

/**
 * Individual scene or chapter with location, characters, time, and events
 */
export interface Scene {
  /** Unique identifier */
  id: string;

  /** Scene title */
  title?: string;

  /** Scene number */
  sceneNumber: number;

  /** Scene content */
  content: string;

  /** Story this scene belongs to */
  storyId: string;

  /** Location where scene takes place */
  locationId: string;

  /** Characters featured in scene */
  characterIds: string[];

  /** Objects in scene */
  objectIds?: string[];

  /** Time point when scene occurs */
  timePointId?: string;

  /** Time of day */
  timeOfDay?: TimeOfDay;

  /** Season */
  season?: Season;

  /** Is this scene part of a repetitive pattern? */
  isRepetition?: boolean;

  /** Repetitive pattern this scene belongs to */
  repetitivePatternId?: string;

  /** Visual style for this scene */
  visualStyle?: VisualStyle;
}

/**
 * Physical or imaginary place where scenes occur
 */
export interface Location {
  /** Unique identifier */
  id: string;

  /** Location name */
  name: string;

  /** Location type */
  type: LocationType;

  /** Location description */
  description?: string;

  /** Is this a real-world location? */
  isRealWorld: boolean;

  /** Reality status (real, imaginary, perspective-dependent) */
  realityStatus?: RealityStatus;

  /** City (for real-world locations) */
  city?: string;

  /** State/province (for real-world locations) */
  state?: string;

  /** Country (for real-world locations) */
  country?: string;

  /** Geographic coordinates */
  coordinates?: { lat: number; lng: number };

  /** Object inventory for this location (Goodnight Moon style) */
  inventory?: ObjectInventory;
}

/**
 * Physical item or prop in story, may be symbolic or imaginary
 */
export interface Object {
  /** Unique identifier */
  id: string;

  /** Object name */
  name: string;

  /** Object type */
  type: ObjectType;

  /** Object description */
  description?: string;

  /** Reality status (real, imaginary, created) */
  realityStatus?: RealityStatus;

  /** Is this object symbolic? */
  isSymbolic: boolean;

  /** Symbolism description */
  symbolism?: string;

  /** Symbolic concepts */
  symbolizes?: Symbol[];

  /** Character who created/imagined this object */
  createdBy?: string;

  /** How object was created */
  creationMethod?: string;

  /** Location this object belongs to */
  locationId?: string;
}

/**
 * Plot structure with acts, turning points, and climax
 */
export interface Plot {
  /** Unique identifier */
  id: string;

  /** Story this plot belongs to */
  storyId: string;

  /** Plot summary */
  summary?: string;

  /** Number of acts */
  acts?: number;

  /** Key turning points */
  turningPoints?: TurningPoint[];

  /** Climax scene */
  climaxSceneId?: string;

  /** Resolution scene */
  resolutionSceneId?: string;
}

/**
 * Turning point in plot
 */
export interface TurningPoint {
  /** Scene where turning point occurs */
  sceneId: string;

  /** Description of turning point */
  description: string;

  /** Order in plot */
  order: number;
}

/**
 * Thematic element or message
 */
export interface Theme {
  /** Theme concept (friendship, courage, love) */
  concept: string;

  /** Theme description */
  description?: string;
}

/**
 * Central conflict driving the narrative
 */
export interface Conflict {
  /** Unique identifier */
  id: string;

  /** Conflict type */
  type: ConflictType;

  /** Conflict description */
  description: string;

  /** Characters involved */
  characterIds?: string[];

  /** Resolution scene */
  resolutionSceneId?: string;
}

/**
 * Character speech with speaker, content, and emotion
 */
export interface Dialogue {
  /** Unique identifier */
  id: string;

  /** Character speaking */
  speakerId: string;

  /** Dialogue content */
  content: string;

  /** Emotional tone */
  emotion?: string;

  /** Scene where dialogue occurs */
  sceneId: string;
}

/**
 * Character or story arc with beginning, middle, and end
 */
export interface Arc {
  /** Unique identifier */
  id: string;

  /** Arc description */
  description: string;

  /** Beginning state */
  beginning: string;

  /** Middle development */
  middle?: string;

  /** End state */
  end: string;
}

// ============================================
// TIME MODELING (High Priority)
// ============================================

/**
 * Specific moment or period in story timeline
 */
export interface TimePoint {
  /** Unique identifier */
  id: string;

  /** Timestamp (can be datetime, descriptive like "childhood", or day like "Monday") */
  timestamp: string;

  /** Description of this time point */
  description?: string;

  /** Season */
  season?: Season;

  /** Time of day */
  timeOfDay?: TimeOfDay;
}

/**
 * Character appearance and state at specific time point
 * (Used to model character aging: boy as child vs elderly)
 */
export interface CharacterAtTime {
  /** Unique identifier */
  id: string;

  /** Character this appearance belongs to */
  characterId: string;

  /** Time point when character appears this way */
  timePointId: string;

  /** Age (can be number, range, or life stage) */
  age?: Age;

  /** Life stage */
  lifeStage?: LifeStage;

  /** Physical description */
  physicalDescription: string;

  /** Emotional state */
  emotionalState?: string;

  /** Detailed appearance */
  appearance?: Appearance;
}

/**
 * Overall timeline of story with key time points and duration
 */
export interface StoryTimeline {
  /** Story this timeline belongs to */
  storyId: string;

  /** Time points in story */
  timePoints: TimePoint[];

  /** Total duration of story */
  duration?: string;
}

/**
 * Specific time within a day
 */
export interface TimeOfDay {
  /** Hour (0-23) */
  hour: number;

  /** Minute (0-59) */
  minute: number;

  /** Period of day */
  period?: DayPeriod;

  /** Light level */
  lightLevel?: LightLevel;

  /** Description */
  description?: string;
}

/**
 * Progression of seasons throughout story
 */
export interface SeasonalProgression {
  /** Story this progression belongs to */
  storyId: string;

  /** Starting season */
  startSeason: Season;

  /** Ending season */
  endSeason: Season;

  /** Seasonal milestones */
  seasonalMilestones?: SeasonalMilestone[];
}

/**
 * Seasonal milestone in story
 */
export interface SeasonalMilestone {
  /** Season */
  season: Season;

  /** Scene where milestone occurs */
  sceneId: string;

  /** Description */
  description: string;
}

/**
 * Flexible age representation
 */
export type Age =
  | { type: 'specific'; years: number }
  | { type: 'range'; min: number; max: number }
  | { type: 'stage'; stage: LifeStage }
  | { type: 'descriptive'; description: string };

/**
 * Physical appearance details
 */
export interface Appearance {
  /** Hair amount/color */
  hairAmount?: string;

  /** Posture */
  posture?: string;

  /** Facial expression */
  expression?: string;

  /** Clothing */
  clothing?: string;

  /** Other physical details */
  other?: string;
}

// ============================================
// TRANSFORMATION (High Priority)
// ============================================

/**
 * Physical or state transformation of character or object over time
 */
export interface Transformation {
  /** Unique identifier */
  id: string;

  /** Subject being transformed (character or object ID) */
  subjectId: string;

  /** Starting state */
  fromState: State;

  /** Ending state */
  toState: State;

  /** Type of transformation */
  transformationType: TransformationType;

  /** Duration of transformation */
  duration?: string;

  /** What triggers the transformation */
  trigger?: string;
}

/**
 * State in transformation
 */
export interface State {
  /** Life stage (for aging) */
  stage?: LifeStage;

  /** Physical form (for metamorphosis) */
  form?: string;

  /** Description */
  description: string;
}

// ============================================
// REALITY STATUS (High Priority)
// ============================================

/**
 * Whether element is real, imaginary, or perspective-dependent
 */
export interface RealityStatus {
  /** Is real */
  isReal: boolean;

  /** Is imaginary */
  isImaginary: boolean;

  /** Character who imagines this (for imaginary elements) */
  imaginedBy?: string;

  /** Perspective note */
  perspective?: string;
}

// ============================================
// REPETITIVE PATTERNS (Medium Priority)
// ============================================

/**
 * Repeated scene, dialogue, or structure with variations
 * (e.g., Green Eggs and Ham, Goodnight Moon)
 */
export interface RepetitivePattern {
  /** Unique identifier */
  id: string;

  /** Story this pattern belongs to */
  storyId: string;

  /** Type of pattern */
  patternType: PatternType;

  /** Base content that repeats */
  baseContent: string;

  /** Individual variations */
  variations: Variation[];

  /** Number of occurrences (must be 2+) */
  occurrences: number;
}

/**
 * Individual variation of repetitive pattern
 */
export interface Variation {
  /** Variation content */
  content: string;

  /** Location (for location-based variations) */
  locationId?: string;

  /** Scene */
  sceneId?: string;

  /** Order in sequence */
  order: number;
}

// ============================================
// OBJECT INVENTORIES (Medium Priority)
// ============================================

/**
 * Catalog of all objects in a location (Goodnight Moon style)
 */
export interface ObjectInventory {
  /** Location this inventory belongs to */
  locationId: string;

  /** Cataloged objects */
  objects: CatalogedObject[];

  /** Purpose of inventory */
  purpose?: InventoryPurpose;
}

/**
 * Object with position and significance in inventory
 */
export interface CatalogedObject {
  /** Object ID */
  objectId: string;

  /** Position in location */
  position: string;

  /** Significance */
  significance?: string;

  /** Is object addressed directly? (Goodnight Moon) */
  addressedDirectly?: boolean;
}

// ============================================
// SYMBOLIC OBJECTS (Medium Priority)
// ============================================

/**
 * Symbolic concept or meaning represented by object
 */
export interface Symbol {
  /** Concept (belonging, acceptance, childhood innocence) */
  concept: string;

  /** Interpretation/meaning */
  interpretation: string;

  /** Cultural context */
  culturalContext?: string;
}

// ============================================
// CHARACTER GROUPS (Medium Priority)
// ============================================

/**
 * Group of related characters (siblings, family, team)
 */
export interface CharacterGroup {
  /** Unique identifier */
  id: string;

  /** Group name */
  name: string;

  /** Group members */
  members: GroupMember[];

  /** Group type */
  groupType: GroupType;
}

/**
 * Individual member of character group with distinctive traits
 */
export interface GroupMember {
  /** Character ID */
  characterId: string;

  /** Role in group */
  role?: string;

  /** Distinctive traits that set apart from siblings */
  distinctiveTraits: string[];

  /** Relationship to others */
  relationToOthers?: string;
}

// ============================================
// VISUAL STYLE (Low Priority)
// ============================================

/**
 * Visual/artistic style of story (for illustrated books)
 */
export interface VisualStyle {
  /** Story or scene ID */
  storyId?: string;
  sceneId?: string;

  /** Medium (collage, watercolor, pencil) */
  medium?: string;

  /** Color palette */
  colorPalette?: string[];

  /** Visual progression */
  visualProgression?: VisualProgression;
}

/**
 * Visual progression throughout story
 */
export interface VisualProgression {
  /** Type of progression */
  type: ProgressionType;

  /** Description */
  description: string;

  /** Purpose */
  purpose: string;
}

// ============================================
// LINGUISTIC CONSTRAINTS (Low Priority)
// ============================================

/**
 * Linguistic constraints and statistics
 */
export interface LinguisticConstraints {
  /** Story ID */
  storyId: string;

  /** Number of unique words */
  uniqueWords?: number;

  /** Total word count */
  totalWords?: number;

  /** Repeated word statistics */
  repeatedWord?: { word: string; count: number };

  /** Reading level */
  readingLevel?: ReadingLevel;

  /** Additional constraints */
  constraints?: string[];
}

// ============================================
// Enum Types
// ============================================

export enum StoryStatus {
  Draft = 'draft',
  InProgress = 'in-progress',
  Complete = 'complete',
  Published = 'published',
}

export enum CharacterRole {
  Protagonist = 'protagonist',
  Antagonist = 'antagonist',
  Supporting = 'supporting',
  Minor = 'minor',
}

export enum CharacterType {
  Human = 'human',
  Animal = 'animal',
  AnthropomorphicAnimal = 'anthropomorphic-animal',
  InanimateObject = 'inanimate-object',
  Imaginary = 'imaginary',
  Mythical = 'mythical',
}

export enum ConflictType {
  PersonVsPerson = 'person-vs-person',
  PersonVsNature = 'person-vs-nature',
  PersonVsSelf = 'person-vs-self',
  PersonVsSociety = 'person-vs-society',
}

export enum GenreType {
  Fantasy = 'fantasy',
  SciFi = 'sci-fi',
  Romance = 'romance',
  Thriller = 'thriller',
  Mystery = 'mystery',
  Horror = 'horror',
  Literary = 'literary',
  Historical = 'historical',
  ChildrensLiterature = 'childrens-literature',
}

export enum LocationType {
  Landmark = 'landmark',
  Building = 'building',
  Park = 'park',
  Street = 'street',
  Natural = 'natural',
  Indoor = 'indoor',
  Outdoor = 'outdoor',
}

export enum ObjectType {
  Prop = 'prop',
  Weapon = 'weapon',
  Vehicle = 'vehicle',
  Artifact = 'artifact',
  NaturalObject = 'natural-object',
  SymbolicObject = 'symbolic-object',
}

export enum LifeStage {
  Infant = 'infant',
  Toddler = 'toddler',
  Child = 'child',
  Preteen = 'preteen',
  Teenager = 'teenager',
  YoungAdult = 'young-adult',
  MiddleAged = 'middle-aged',
  Elderly = 'elderly',
}

export enum TransformationType {
  Metamorphosis = 'metamorphosis',
  Aging = 'aging',
  MagicalTransformation = 'magical-transformation',
  ImaginaryCreation = 'imaginary-creation',
  EnvironmentalChange = 'environmental-change',
}

export enum Season {
  Spring = 'spring',
  Summer = 'summer',
  Fall = 'fall',
  Winter = 'winter',
}

export enum DayPeriod {
  Morning = 'morning',
  Afternoon = 'afternoon',
  Evening = 'evening',
  Night = 'night',
  Dawn = 'dawn',
  Dusk = 'dusk',
}

export enum LightLevel {
  Bright = 'bright',
  Dim = 'dim',
  Dark = 'dark',
}

export enum PatternType {
  Refrain = 'refrain',
  Ritual = 'ritual',
  QuestionAnswer = 'question-answer',
  Escalation = 'escalation',
}

export enum InventoryPurpose {
  BedrimeRitual = 'bedtime-ritual',
  SceneDetail = 'scene-detail',
  MemoryDevice = 'memory-device',
}

export enum AnthropomorphicTrait {
  Speech = 'speech',
  Clothing = 'clothing',
  HumanEmotions = 'human-emotions',
  WalksUpright = 'walks-upright',
  UsesTools = 'uses-tools',
}

export enum GroupType {
  Siblings = 'siblings',
  Family = 'family',
  Friends = 'friends',
  Team = 'team',
}

export enum ProgressionType {
  Growing = 'growing',
  Shrinking = 'shrinking',
  Darkening = 'darkening',
  Lightening = 'lightening',
  ColorShift = 'color-shift',
}

export enum ReadingLevel {
  PreReader = 'pre-reader',
  EmergingReader = 'emerging-reader',
  BeginningReader = 'beginning-reader',
  EarlyReader = 'early-reader',
}

// ============================================
// Validation Functions
// ============================================

/**
 * Validation result
 */
export interface ValidationResult {
  valid: boolean;
  errors: string[];
}

/**
 * Validate Story entity
 */
export function validateStory(story: Story): ValidationResult {
  const errors: string[] = [];

  // Title required, 1-200 characters
  if (!story.title || story.title.length < 1 || story.title.length > 200) {
    errors.push('Story title is required and must be between 1-200 characters');
  }

  // Status required
  if (!story.status) {
    errors.push('Story status is required');
  }

  // Must have at least one character
  if (!story.characters || story.characters.length === 0) {
    errors.push('Story must have at least one character');
  }

  // Must have at least one scene
  if (!story.scenes || story.scenes.length === 0) {
    errors.push('Story must have at least one scene');
  }

  return { valid: errors.length === 0, errors };
}

/**
 * Validate Character entity
 */
export function validateCharacter(character: Character): ValidationResult {
  const errors: string[] = [];

  // Name required, 1-100 characters
  if (!character.name || character.name.length < 1 || character.name.length > 100) {
    errors.push('Character name is required and must be 1-100 characters');
  }

  // Character type required
  if (!character.characterType) {
    errors.push('Character type is required');
  }

  // Role required
  if (!character.role) {
    errors.push('Character role is required');
  }

  // Anthropomorphic animals should have species
  if (character.characterType === CharacterType.AnthropomorphicAnimal && !character.species) {
    errors.push('Anthropomorphic animals should have species defined');
  }

  return { valid: errors.length === 0, errors };
}

/**
 * Validate Scene entity
 */
export function validateScene(scene: Scene): ValidationResult {
  const errors: string[] = [];

  // Scene number required and positive
  if (!scene.sceneNumber || scene.sceneNumber < 1) {
    errors.push('Scene number is required and must be positive integer');
  }

  // Location required
  if (!scene.locationId) {
    errors.push('Scene must take place at a valid location');
  }

  // Content required
  if (!scene.content || scene.content.length === 0) {
    errors.push('Scene content is required and must not be empty');
  }

  return { valid: errors.length === 0, errors };
}

/**
 * Validate Location entity
 */
export function validateLocation(location: Location): ValidationResult {
  const errors: string[] = [];

  // Name required, 1-200 characters
  if (!location.name || location.name.length < 1 || location.name.length > 200) {
    errors.push('Location name is required and must be 1-200 characters');
  }

  // Type required
  if (!location.type) {
    errors.push('Location type is required');
  }

  // Real-world locations should have city/state
  if (location.isRealWorld && !location.city) {
    errors.push('Real-world locations should have city and state/country defined');
  }

  return { valid: errors.length === 0, errors };
}

/**
 * Validate Object entity
 */
export function validateObject(obj: Object): ValidationResult {
  const errors: string[] = [];

  // Name required, 1-200 characters
  if (!obj.name || obj.name.length < 1 || obj.name.length > 200) {
    errors.push('Object name is required and must be 1-200 characters');
  }

  // Type required
  if (!obj.type) {
    errors.push('Object type is required');
  }

  // Symbolic objects should have symbolism
  if (obj.isSymbolic && !obj.symbolism) {
    errors.push('Objects marked as symbolic should have symbolism text defined');
  }

  return { valid: errors.length === 0, errors };
}

/**
 * Validate TimePoint entity
 */
export function validateTimePoint(timePoint: TimePoint): ValidationResult {
  const errors: string[] = [];

  // Timestamp required
  if (!timePoint.timestamp || timePoint.timestamp.length === 0) {
    errors.push('TimePoint timestamp is required');
  }

  return { valid: errors.length === 0, errors };
}

/**
 * Validate CharacterAtTime entity
 */
export function validateCharacterAtTime(cat: CharacterAtTime): ValidationResult {
  const errors: string[] = [];

  // Time point required
  if (!cat.timePointId) {
    errors.push('CharacterAtTime must reference a valid TimePoint');
  }

  // Physical description required
  if (!cat.physicalDescription || cat.physicalDescription.length === 0) {
    errors.push('Physical description is required for CharacterAtTime');
  }

  return { valid: errors.length === 0, errors };
}

/**
 * Validate Transformation entity
 */
export function validateTransformation(transformation: Transformation): ValidationResult {
  const errors: string[] = [];

  // Type required
  if (!transformation.transformationType) {
    errors.push('Transformation type is required');
  }

  // From state required
  if (!transformation.fromState || !transformation.fromState.description) {
    errors.push('Transformation fromState is required');
  }

  // To state required
  if (!transformation.toState || !transformation.toState.description) {
    errors.push('Transformation toState is required');
  }

  return { valid: errors.length === 0, errors };
}

/**
 * Validate RepetitivePattern entity
 */
export function validateRepetitivePattern(pattern: RepetitivePattern): ValidationResult {
  const errors: string[] = [];

  // Pattern type required
  if (!pattern.patternType) {
    errors.push('Pattern type is required');
  }

  // Base content required
  if (!pattern.baseContent || pattern.baseContent.length === 0) {
    errors.push('Base content is required for repetitive pattern');
  }

  // Occurrences must be 2+
  if (!pattern.occurrences || pattern.occurrences < 2) {
    errors.push('Occurrences must be at least 2 for a repetitive pattern');
  }

  return { valid: errors.length === 0, errors };
}

/**
 * Validate CharacterGroup entity
 */
export function validateCharacterGroup(group: CharacterGroup): ValidationResult {
  const errors: string[] = [];

  // Name required
  if (!group.name || group.name.length === 0) {
    errors.push('Character group name is required');
  }

  // Must have at least 2 members
  if (!group.members || group.members.length < 2) {
    errors.push('Character group must have at least 2 members');
  }

  return { valid: errors.length === 0, errors };
}

/**
 * Validate Dialogue entity
 */
export function validateDialogue(dialogue: Dialogue): ValidationResult {
  const errors: string[] = [];

  // Speaker required
  if (!dialogue.speakerId) {
    errors.push('Dialogue must have a character as speaker');
  }

  // Content required
  if (!dialogue.content || dialogue.content.length === 0) {
    errors.push('Dialogue content is required and must not be empty');
  }

  return { valid: errors.length === 0, errors };
}
