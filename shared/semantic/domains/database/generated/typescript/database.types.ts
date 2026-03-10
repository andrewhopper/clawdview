/**
 * Database Domain Model - TypeScript Types
 * Auto-generated from schema.yaml
 * Version: 1.0.0
 *
 * Core database concepts: schemas, tables, indexes, constraints, queries, transactions, migrations
 */

// ============================================
// ENUMS
// ============================================

export enum DataType {
  // Numeric
  Integer = 'integer',
  BigInt = 'bigint',
  SmallInt = 'smallint',
  Decimal = 'decimal',
  Numeric = 'numeric',
  Real = 'real',
  DoublePrecision = 'double_precision',
  Serial = 'serial',
  BigSerial = 'bigserial',
  // Character
  Char = 'char',
  Varchar = 'varchar',
  Text = 'text',
  // Binary
  Bytea = 'bytea',
  Blob = 'blob',
  // Date/Time
  Date = 'date',
  Time = 'time',
  Timestamp = 'timestamp',
  TimestampTz = 'timestamptz',
  Interval = 'interval',
  // Boolean
  Boolean = 'boolean',
  // JSON
  Json = 'json',
  Jsonb = 'jsonb',
  // Array
  Array = 'array',
  // UUID
  Uuid = 'uuid',
  // Network
  Inet = 'inet',
  Cidr = 'cidr',
  MacAddr = 'macaddr',
  // Geometric
  Point = 'point',
  Line = 'line',
  Box = 'box',
  Circle = 'circle',
  Polygon = 'polygon',
  // Other
  Xml = 'xml',
  Money = 'money',
  Enum = 'enum',
  Range = 'range',
}

export enum IndexType {
  BTree = 'btree',
  Hash = 'hash',
  GiST = 'gist',
  SpGiST = 'spgist',
  GIN = 'gin',
  BRIN = 'brin',
  Bitmap = 'bitmap',
  FullText = 'fulltext',
  Spatial = 'spatial',
  Clustered = 'clustered',
  Nonclustered = 'nonclustered',
  Covering = 'covering',
  Filtered = 'filtered',
  Columnstore = 'columnstore',
}

export enum SortOrder {
  Ascending = 'ascending',
  Descending = 'descending',
}

export enum ReferentialAction {
  NoAction = 'no_action',
  Restrict = 'restrict',
  Cascade = 'cascade',
  SetNull = 'set_null',
  SetDefault = 'set_default',
}

export enum ViewCheckOption {
  None = 'none',
  Local = 'local',
  Cascaded = 'cascaded',
}

export enum ProcedureLanguage {
  SQL = 'sql',
  PLpgSQL = 'plpgsql',
  PLPython = 'plpython',
  PLPerl = 'plperl',
  PLJava = 'pljava',
  PLSQL = 'plsql',
  TSQL = 'tsql',
  JavaScript = 'javascript',
}

export enum ParameterMode {
  In = 'in',
  Out = 'out',
  InOut = 'inout',
  Variadic = 'variadic',
}

export enum SecurityType {
  Definer = 'definer',
  Invoker = 'invoker',
}

export enum TriggerTiming {
  Before = 'before',
  After = 'after',
  InsteadOf = 'instead_of',
}

export enum TriggerEvent {
  Insert = 'insert',
  Update = 'update',
  Delete = 'delete',
  Truncate = 'truncate',
}

export enum TriggerLevel {
  Row = 'row',
  Statement = 'statement',
}

export enum PartitionStrategy {
  Range = 'range',
  List = 'list',
  Hash = 'hash',
  Composite = 'composite',
}

export enum QueryType {
  Select = 'select',
  Insert = 'insert',
  Update = 'update',
  Delete = 'delete',
  CreateTable = 'create_table',
  AlterTable = 'alter_table',
  DropTable = 'drop_table',
  CreateIndex = 'create_index',
  DropIndex = 'drop_index',
  Transaction = 'transaction',
  DDL = 'ddl',
  DML = 'dml',
  DCL = 'dcl',
}

export enum ExecutionNodeType {
  SeqScan = 'seq_scan',
  IndexScan = 'index_scan',
  IndexOnlyScan = 'index_only_scan',
  BitmapScan = 'bitmap_scan',
  NestedLoop = 'nested_loop',
  HashJoin = 'hash_join',
  MergeJoin = 'merge_join',
  Sort = 'sort',
  Aggregate = 'aggregate',
  Group = 'group',
  Limit = 'limit',
  Materialize = 'materialize',
  Append = 'append',
  Unique = 'unique',
}

export enum ScanMethod {
  Sequential = 'sequential',
  Index = 'index',
  IndexOnly = 'index_only',
  Bitmap = 'bitmap',
  TidScan = 'tid_scan',
}

export enum JoinType {
  Inner = 'inner',
  Left = 'left',
  Right = 'right',
  Full = 'full',
  Cross = 'cross',
  Semi = 'semi',
  Anti = 'anti',
}

export enum IsolationLevel {
  ReadUncommitted = 'read_uncommitted',
  ReadCommitted = 'read_committed',
  RepeatableRead = 'repeatable_read',
  Serializable = 'serializable',
}

export enum TransactionStatus {
  Active = 'active',
  Committed = 'committed',
  RolledBack = 'rolled_back',
  Aborted = 'aborted',
  Prepared = 'prepared',
}

export enum LockResourceType {
  Table = 'table',
  Row = 'row',
  Page = 'page',
  Database = 'database',
  Schema = 'schema',
  Index = 'index',
}

export enum LockMode {
  Shared = 'shared',
  Exclusive = 'exclusive',
  IntentShared = 'intent_shared',
  IntentExclusive = 'intent_exclusive',
  Update = 'update',
}

export enum MigrationStatus {
  Pending = 'pending',
  InProgress = 'in_progress',
  Completed = 'completed',
  Failed = 'failed',
  RolledBack = 'rolled_back',
  Skipped = 'skipped',
}

export enum MigrationDirection {
  Up = 'up',
  Down = 'down',
}

export enum MigrationOperation {
  CreateTable = 'create_table',
  DropTable = 'drop_table',
  AlterTable = 'alter_table',
  AddColumn = 'add_column',
  DropColumn = 'drop_column',
  AlterColumn = 'alter_column',
  CreateIndex = 'create_index',
  DropIndex = 'drop_index',
  CreateConstraint = 'create_constraint',
  DropConstraint = 'drop_constraint',
  RawSql = 'raw_sql',
}

export enum ReplicaRole {
  Primary = 'primary',
  ReadReplica = 'read_replica',
  StandbySync = 'standby_sync',
  StandbyAsync = 'standby_async',
}

export enum ReplicaStatus {
  Active = 'active',
  Replicating = 'replicating',
  Lagging = 'lagging',
  Failed = 'failed',
  Offline = 'offline',
}

export enum ShardStatus {
  Active = 'active',
  Inactive = 'inactive',
  Migrating = 'migrating',
  Splitting = 'splitting',
  Merging = 'merging',
}

// ============================================
// ENTITIES
// ============================================

export interface DatabaseSchema {
  id: string;
  name: string;
  databaseId: string;
  owner?: string;
  description?: string;
  isPublic?: boolean;
  createdAt: Date;
  updatedAt: Date;
}

export interface Column {
  id: string;
  name: string;
  dataType: DataType;
  isNullable?: boolean;
  defaultValue?: string;
  maxLength?: number;
  precision?: number;
  scale?: number;
  isAutoIncrement?: boolean;
  isUnique?: boolean;
  description?: string;
  ordinalPosition?: number;
  collation?: string;
}

export interface PrimaryKey {
  id: string;
  name: string;
  columns: string[];
  isClustered?: boolean;
}

export interface ForeignKey {
  id: string;
  name: string;
  columns: string[];
  referencedTableId: string;
  referencedColumns: string[];
  onDelete?: ReferentialAction;
  onUpdate?: ReferentialAction;
  isDeferrable?: boolean;
  isEnforced?: boolean;
}

export interface UniqueConstraint {
  id: string;
  name: string;
  columns: string[];
  isNullsDistinct?: boolean;
}

export interface CheckConstraint {
  id: string;
  name: string;
  expression: string;
  isEnforced?: boolean;
}

export interface IndexColumn {
  columnName: string;
  sortOrder?: SortOrder;
  isDescending?: boolean;
  nullsFirst?: boolean;
  collation?: string;
}

export interface Index {
  id: string;
  name: string;
  tableId: string;
  type: IndexType;
  columns: IndexColumn[];
  isUnique?: boolean;
  isPrimary?: boolean;
  isClustered?: boolean;
  whereClause?: string;
  includeColumns?: string[];
  fillFactor?: number;
  sizeBytes?: number;
  createdAt: Date;
  updatedAt: Date;
}

export interface Table {
  id: string;
  name: string;
  schemaId: string;
  description?: string;
  columns: Column[];
  primaryKey?: PrimaryKey;
  foreignKeys?: ForeignKey[];
  uniqueConstraints?: UniqueConstraint[];
  checkConstraints?: CheckConstraint[];
  indexes?: Index[];
  triggers?: Trigger[];
  rowCount?: number;
  sizeBytes?: number;
  isPartitioned?: boolean;
  partitionStrategy?: PartitionStrategy;
  createdAt: Date;
  updatedAt: Date;
}

export interface View {
  id: string;
  name: string;
  schemaId: string;
  definition: string;
  isMaterialized?: boolean;
  isUpdatable?: boolean;
  checkOption?: ViewCheckOption;
  description?: string;
  createdAt: Date;
  updatedAt: Date;
}

export interface MaterializedView extends View {
  lastRefreshedAt?: Date;
  refreshSchedule?: string;
  isAutoRefresh?: boolean;
  sizeBytes?: number;
  rowCount?: number;
}

export interface ProcedureParameter {
  name: string;
  dataType: DataType;
  mode: ParameterMode;
  defaultValue?: string;
  ordinalPosition?: number;
}

export interface StoredProcedure {
  id: string;
  name: string;
  schemaId: string;
  language: ProcedureLanguage;
  definition: string;
  parameters?: ProcedureParameter[];
  returnType?: DataType;
  isFunction?: boolean;
  isAggregate?: boolean;
  securityType?: SecurityType;
  description?: string;
  createdAt: Date;
  updatedAt: Date;
}

export interface Trigger {
  id: string;
  name: string;
  tableId: string;
  timing: TriggerTiming;
  event: TriggerEvent;
  level?: TriggerLevel;
  condition?: string;
  procedureId: string;
  isEnabled?: boolean;
  executionOrder?: number;
  createdAt: Date;
  updatedAt: Date;
}

export interface Sequence {
  id: string;
  name: string;
  schemaId: string;
  currentValue: number;
  increment?: number;
  minValue?: number;
  maxValue?: number;
  startValue?: number;
  cache?: number;
  isCycle?: boolean;
  ownedByTable?: string;
  ownedByColumn?: string;
  createdAt: Date;
  updatedAt: Date;
}

export interface PartitionBounds {
  lower?: string;
  upper?: string;
  values?: string[];
  modulus?: number;
  remainder?: number;
}

export interface Partition {
  id: string;
  name: string;
  parentTableId: string;
  strategy: PartitionStrategy;
  expression?: string;
  bounds?: PartitionBounds;
  sizeBytes?: number;
  rowCount?: number;
  createdAt: Date;
}

export interface QueryParameter {
  name: string;
  dataType: DataType;
  value?: string;
  ordinalPosition?: number;
}

export interface ExecutionNode {
  id: string;
  nodeType: ExecutionNodeType;
  parentNodeId?: string;
  relationName?: string;
  indexName?: string;
  scanMethod?: ScanMethod;
  joinType?: JoinType;
  joinCondition?: string;
  filter?: string;
  estimatedRows?: number;
  estimatedCost?: number;
  actualRows?: number;
  actualLoops?: number;
  children?: ExecutionNode[];
}

export interface QueryPlan {
  id: string;
  queryId: string;
  root?: ExecutionNode;
  totalCost?: number;
  startupCost?: number;
  planningTime?: number;
  executionTime?: number;
  createdAt: Date;
}

export interface Query {
  id: string;
  sql: string;
  queryType: QueryType;
  parameters?: QueryParameter[];
  executionPlan?: QueryPlan;
  estimatedCost?: number;
  estimatedRows?: number;
  executedAt?: Date;
  durationMs?: number;
  rowsAffected?: number;
}

export interface Savepoint {
  id: string;
  name: string;
  transactionId: string;
  createdAt: Date;
}

export interface Transaction {
  id: string;
  isolationLevel: IsolationLevel;
  status: TransactionStatus;
  isReadOnly?: boolean;
  startedAt: Date;
  committedAt?: Date;
  rolledBackAt?: Date;
  savepoints?: Savepoint[];
}

export interface Lock {
  id: string;
  resourceType: LockResourceType;
  resourceId: string;
  lockMode: LockMode;
  transactionId: string;
  isBlocking?: boolean;
  blockedBy?: string;
  acquiredAt: Date;
  releasedAt?: Date;
}

export interface MigrationStep {
  id: string;
  stepNumber: number;
  operation: MigrationOperation;
  sql: string;
  rollbackSql?: string;
  isReversible?: boolean;
  executedAt?: Date;
  errorMessage?: string;
}

export interface Migration {
  id: string;
  version: string;
  name: string;
  description?: string;
  steps: MigrationStep[];
  status: MigrationStatus;
  direction: MigrationDirection;
  executedAt?: Date;
  durationMs?: number;
  errorMessage?: string;
  checksum?: string;
  createdAt: Date;
}

export interface Replica {
  id: string;
  primaryDatabaseId: string;
  endpoint: string;
  region?: string;
  role: ReplicaRole;
  replicationLag?: number;
  status: ReplicaStatus;
  isPrimary?: boolean;
  priority?: number;
  createdAt: Date;
  updatedAt: Date;
}

export interface ShardKeyRange {
  minValue: string;
  maxValue: string;
  isMinInclusive?: boolean;
  isMaxInclusive?: boolean;
}

export interface Shard {
  id: string;
  name: string;
  shardKey: string;
  keyRange?: ShardKeyRange;
  databaseId: string;
  endpoint?: string;
  status: ShardStatus;
  rowCount?: number;
  sizeBytes?: number;
  createdAt: Date;
  updatedAt: Date;
}

// ============================================
// ACTIONS
// ============================================

export interface CreateTableParams {
  schemaId: string;
  name: string;
  columns: Column[];
  primaryKey?: PrimaryKey;
}

export interface CreateIndexParams {
  tableId: string;
  name: string;
  type: IndexType;
  columns: IndexColumn[];
  isUnique?: boolean;
  whereClause?: string;
}

export interface AddColumnParams {
  tableId: string;
  column: Column;
}

export interface AddForeignKeyParams {
  tableId: string;
  foreignKey: ForeignKey;
}

export interface ExecuteQueryParams {
  sql: string;
  parameters?: QueryParameter[];
  timeout?: number;
}

export interface ExplainQueryParams {
  sql: string;
  analyze?: boolean;
}

export interface CreateMigrationParams {
  version: string;
  name: string;
  steps: MigrationStep[];
}

export interface ApplyMigrationParams {
  migrationId: string;
}

export interface RollbackMigrationParams {
  migrationId: string;
}

export interface CreateReplicaParams {
  primaryDatabaseId: string;
  region?: string;
  role?: ReplicaRole;
}

export interface CreateShardParams {
  name: string;
  shardKey: string;
  keyRange: ShardKeyRange;
}
