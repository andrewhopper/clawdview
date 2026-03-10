/**
 * Data Pipeline Domain Model - TypeScript Types
 * Auto-generated from schema.yaml
 * Version: 1.0.0
 *
 * Data pipelines, ETL/ELT workflows, orchestration, transformations, data quality, and lineage tracking
 */

// ============================================
// ENUMS
// ============================================

/** Type of data pipeline */
export enum PipelineType {
  ETL = 'etl',
  ELT = 'elt',
  Streaming = 'streaming',
  Batch = 'batch',
  Hybrid = 'hybrid',
  CDC = 'cdc',
  Replication = 'replication',
}

/** Type of pipeline schedule */
export enum ScheduleType {
  Cron = 'cron',
  Interval = 'interval',
  Event = 'event',
  Manual = 'manual',
  Continuous = 'continuous',
}

/** Type of pipeline task */
export enum TaskType {
  Extract = 'extract',
  Transform = 'transform',
  Load = 'load',
  Quality = 'quality',
  Sensor = 'sensor',
  Trigger = 'trigger',
  Script = 'script',
  SQL = 'sql',
  Spark = 'spark',
  Python = 'python',
}

/** Rule for when task should run */
export enum TriggerRule {
  AllSuccess = 'all_success',
  AllFailed = 'all_failed',
  AllDone = 'all_done',
  OneSuccess = 'one_success',
  OneFailed = 'one_failed',
  NoneSkipped = 'none_skipped',
  NoneFailedOrSkipped = 'none_failed_or_skipped',
}

/** Type of pipeline run */
export enum RunType {
  Scheduled = 'scheduled',
  Manual = 'manual',
  Backfill = 'backfill',
  Retry = 'retry',
  External = 'external',
}

/** Status of pipeline or task run */
export enum RunStatus {
  Queued = 'queued',
  Running = 'running',
  Success = 'success',
  Failed = 'failed',
  Skipped = 'skipped',
  UpstreamFailed = 'upstream_failed',
  Cancelled = 'cancelled',
  Timeout = 'timeout',
}

/** Type of data source */
export enum DataSourceType {
  PostgreSQL = 'postgresql',
  MySQL = 'mysql',
  SQLServer = 'sqlserver',
  Oracle = 'oracle',
  MongoDB = 'mongodb',
  Cassandra = 'cassandra',
  Snowflake = 'snowflake',
  BigQuery = 'bigquery',
  Redshift = 'redshift',
  S3 = 's3',
  GCS = 'gcs',
  ADLS = 'adls',
  HttpApi = 'http_api',
  Kafka = 'kafka',
  Kinesis = 'kinesis',
  Salesforce = 'salesforce',
  ServiceNow = 'servicenow',
  CSV = 'csv',
  JSON = 'json',
  Parquet = 'parquet',
  Avro = 'avro',
  ORC = 'orc',
}

/** Type of data destination */
export enum DataDestinationType {
  PostgreSQL = 'postgresql',
  MySQL = 'mysql',
  SQLServer = 'sqlserver',
  Snowflake = 'snowflake',
  BigQuery = 'bigquery',
  Redshift = 'redshift',
  Databricks = 'databricks',
  S3 = 's3',
  GCS = 'gcs',
  ADLS = 'adls',
  ElasticSearch = 'elasticsearch',
  Kafka = 'kafka',
  Kinesis = 'kinesis',
}

/** Mode for data extraction */
export enum ExtractionMode {
  Full = 'full',
  Incremental = 'incremental',
  CDC = 'cdc',
  Snapshot = 'snapshot',
  Delta = 'delta',
}

/** Mode for loading data to destination */
export enum LoadMode {
  Append = 'append',
  Overwrite = 'overwrite',
  Upsert = 'upsert',
  Delete = 'delete',
  SCDType1 = 'scd_type1',
  SCDType2 = 'scd_type2',
}

/** Authentication type for connections */
export enum AuthType {
  UsernamePassword = 'username_password',
  ApiKey = 'api_key',
  OAuth2 = 'oauth2',
  IAM = 'iam',
  ServiceAccount = 'service_account',
  Certificate = 'certificate',
  JWT = 'jwt',
}

/** Type of data transformation */
export enum TransformationType {
  SQL = 'sql',
  Python = 'python',
  Spark = 'spark',
  Dbt = 'dbt',
  Custom = 'custom',
  NoCode = 'no_code',
}

/** Language for transformation logic */
export enum TransformationLanguage {
  SQL = 'sql',
  Python = 'python',
  Scala = 'scala',
  Java = 'java',
  R = 'r',
  JavaScript = 'javascript',
  Jinja = 'jinja',
}

/** How transformed data is materialized */
export enum MaterializationType {
  View = 'view',
  Table = 'table',
  Incremental = 'incremental',
  Ephemeral = 'ephemeral',
  Snapshot = 'snapshot',
}

/** Type of data model (dbt-style) */
export enum ModelType {
  Staging = 'staging',
  Intermediate = 'intermediate',
  Mart = 'mart',
  Snapshot = 'snapshot',
}

/** Type of data quality check */
export enum QualityCheckType {
  Completeness = 'completeness',
  Uniqueness = 'uniqueness',
  Validity = 'validity',
  Consistency = 'consistency',
  Accuracy = 'accuracy',
  Timeliness = 'timeliness',
  Schema = 'schema',
  Custom = 'custom',
}

/** Type of quality rule */
export enum RuleType {
  NotNull = 'not_null',
  Unique = 'unique',
  InRange = 'in_range',
  InList = 'in_list',
  Regex = 'regex',
  ForeignKey = 'foreign_key',
  Expression = 'expression',
  RowCount = 'row_count',
  Freshness = 'freshness',
}

/** Comparison operator for rules */
export enum ComparisonOperator {
  Equals = 'equals',
  NotEquals = 'not_equals',
  GreaterThan = 'greater_than',
  GreaterThanOrEqual = 'greater_than_or_equal',
  LessThan = 'less_than',
  LessThanOrEqual = 'less_than_or_equal',
  Between = 'between',
  In = 'in',
  NotIn = 'not_in',
  Contains = 'contains',
  StartsWith = 'starts_with',
  EndsWith = 'ends_with',
  Matches = 'matches',
}

/** Status of quality check */
export enum QualityStatus {
  Passed = 'passed',
  Failed = 'failed',
  Warning = 'warning',
  Skipped = 'skipped',
  Error = 'error',
}

/** Type of data test (dbt-style) */
export enum TestType {
  NotNull = 'not_null',
  Unique = 'unique',
  AcceptedValues = 'accepted_values',
  Relationships = 'relationships',
  Custom = 'custom',
}

/** Severity level */
export enum Severity {
  Critical = 'critical',
  Error = 'error',
  Warning = 'warning',
  Info = 'info',
}

/** Change data capture mode */
export enum CaptureMode {
  LogBased = 'log_based',
  Trigger = 'trigger',
  Timestamp = 'timestamp',
  FullRefresh = 'full_refresh',
  Query = 'query',
}

/** Type of database operation */
export enum OperationType {
  Insert = 'insert',
  Update = 'update',
  Delete = 'delete',
  Truncate = 'truncate',
}

/** Type of lineage relationship */
export enum LineageRelationship {
  DirectCopy = 'direct_copy',
  Transformed = 'transformed',
  Aggregated = 'aggregated',
  Filtered = 'filtered',
  Joined = 'joined',
}

/** Type of observability metric */
export enum MetricType {
  Duration = 'duration',
  RecordCount = 'record_count',
  ErrorRate = 'error_rate',
  Throughput = 'throughput',
  Latency = 'latency',
  Freshness = 'freshness',
  Cost = 'cost',
  CPU = 'cpu',
  Memory = 'memory',
}

/** Type of data alert */
export enum AlertType {
  PipelineFailure = 'pipeline_failure',
  DataQuality = 'data_quality',
  SchemaChange = 'schema_change',
  DataFreshness = 'data_freshness',
  Anomaly = 'anomaly',
  SLABreach = 'sla_breach',
  HighCost = 'high_cost',
}

/** Type of metric aggregation */
export enum AggregationType {
  Sum = 'sum',
  Average = 'average',
  Min = 'min',
  Max = 'max',
  Count = 'count',
  Percentile = 'percentile',
}

/** Channel for sending notifications */
export enum NotificationChannel {
  Email = 'email',
  Slack = 'slack',
  PagerDuty = 'pagerduty',
  Webhook = 'webhook',
  SMS = 'sms',
  Teams = 'teams',
}

/** Status of data incident */
export enum IncidentStatus {
  Open = 'open',
  Investigating = 'investigating',
  Resolved = 'resolved',
  Closed = 'closed',
}

/** Data sensitivity classification */
export enum DataClassification {
  Public = 'public',
  Internal = 'internal',
  Confidential = 'confidential',
  Restricted = 'restricted',
  PII = 'pii',
  PHI = 'phi',
}

/** Data storage format */
export enum DataFormat {
  CSV = 'csv',
  JSON = 'json',
  Parquet = 'parquet',
  Avro = 'avro',
  ORC = 'orc',
  Delta = 'delta',
  Iceberg = 'iceberg',
}

/** Data partitioning strategy */
export enum PartitionStrategy {
  Daily = 'daily',
  Hourly = 'hourly',
  Monthly = 'monthly',
  Yearly = 'yearly',
  Hash = 'hash',
  Range = 'range',
}

/** Log severity level */
export enum LogLevel {
  DEBUG = 'debug',
  INFO = 'info',
  WARNING = 'warning',
  ERROR = 'error',
  CRITICAL = 'critical',
}

// ============================================
// ENTITIES
// ============================================

export interface Pipeline {
  id: string;
  name: string;
  description?: string;
  type: PipelineType;
  schedule?: Schedule;
  tasks?: Task[];
  parameters?: object;
  tags?: string[];
  owner?: string;
  isEnabled?: boolean;
  retryPolicy?: RetryPolicy;
  timeoutSeconds?: number;
  sla?: SLA;
  createdAt: Date;
  updatedAt: Date;
}

export interface Schedule {
  id: string;
  type: ScheduleType;
  cronExpression?: string;
  interval?: number;
  startDate?: Date;
  endDate?: Date;
  timezone?: string;
  catchup?: boolean;
  maxActiveRuns?: number;
}

export interface Task {
  id: string;
  name: string;
  pipelineId: string;
  type: TaskType;
  operator?: string;
  config?: object;
  dependencies?: string[];
  retries?: number;
  retryDelay?: number;
  timeoutSeconds?: number;
  pool?: string;
  priority?: number;
  trigger?: TriggerRule;
}

export interface PipelineRun {
  id: string;
  pipelineId: string;
  runType: RunType;
  status: RunStatus;
  startedAt?: Date;
  completedAt?: Date;
  duration?: number;
  triggeredBy?: string;
  parameters?: object;
  taskRuns?: TaskRun[];
  metrics?: RunMetrics;
  errorMessage?: string;
}

export interface TaskRun {
  id: string;
  taskId: string;
  pipelineRunId: string;
  status: RunStatus;
  attemptNumber?: number;
  startedAt?: Date;
  completedAt?: Date;
  duration?: number;
  logs?: LogEntry[];
  metrics?: TaskMetrics;
  errorMessage?: string;
  errorStackTrace?: string;
}

export interface DataSource {
  id: string;
  name: string;
  type: DataSourceType;
  connectionConfig: ConnectionConfig;
  schema?: SourceSchema;
  extractionMode?: ExtractionMode;
  incrementalKey?: string;
  watermark?: string;
  isActive?: boolean;
  createdAt: Date;
  updatedAt: Date;
}

export interface DataDestination {
  id: string;
  name: string;
  type: DataDestinationType;
  connectionConfig: ConnectionConfig;
  loadMode?: LoadMode;
  schema?: DestinationSchema;
  partitionSpec?: PartitionSpec;
  isActive?: boolean;
  createdAt: Date;
  updatedAt: Date;
}

export interface ConnectionConfig {
  host?: string;
  port?: number;
  database?: string;
  schema?: string;
  username?: string;
  passwordSecretId?: string;
  connectionString?: string;
  authType?: AuthType;
  sslEnabled?: boolean;
  extraParams?: object;
}

export interface SourceSchema {
  tables?: TableConfig[];
  excludePatterns?: string[];
  includePatterns?: string[];
}

export interface TableConfig {
  name: string;
  columns?: string[];
  whereClause?: string;
  orderBy?: string;
  primaryKey?: string[];
}

export interface DestinationSchema {
  tableName: string;
  databaseName?: string;
  schemaName?: string;
  createIfNotExists?: boolean;
}

export interface PartitionSpec {
  columns: string[];
  strategy?: PartitionStrategy;
  format?: string;
}

export interface Transformation {
  id: string;
  name: string;
  type: TransformationType;
  inputSource: string;
  outputDestination: string;
  logic: TransformationLogic;
  dependencies?: string[];
  isIncremental?: boolean;
  materialization?: MaterializationType;
  tags?: string[];
  createdAt: Date;
  updatedAt: Date;
}

export interface TransformationLogic {
  language: TransformationLanguage;
  code: string;
  template?: string;
  variables?: object;
  compiledCode?: string;
}

export interface DataModel {
  id: string;
  name: string;
  modelType: ModelType;
  sql: string;
  materialization: MaterializationType;
  dependencies?: string[];
  columns?: ColumnDefinition[];
  tests?: DataTest[];
  tags?: string[];
  metadata?: object;
}

export interface ColumnDefinition {
  name: string;
  dataType?: string;
  description?: string;
  tests?: string[];
  constraints?: string[];
}

export interface DataQualityCheck {
  id: string;
  name: string;
  type: QualityCheckType;
  target: string;
  rule: QualityRule;
  severity: Severity;
  schedule?: Schedule;
  isBlocking?: boolean;
  notificationConfig?: NotificationConfig;
  createdAt: Date;
  updatedAt: Date;
}

export interface QualityRule {
  ruleType: RuleType;
  column?: string;
  expression?: string;
  threshold?: number;
  expectedValue?: string;
  allowedValues?: string[];
  regex?: string;
  comparisonOperator?: ComparisonOperator;
}

export interface QualityCheckResult {
  id: string;
  checkId: string;
  status: QualityStatus;
  executedAt: Date;
  rowsChecked?: number;
  rowsPassed?: number;
  rowsFailed?: number;
  passRate?: number;
  failedRows?: object[];
  metrics?: object;
  errorMessage?: string;
}

export interface DataTest {
  id: string;
  name: string;
  testType: TestType;
  modelId: string;
  column?: string;
  config?: object;
  severity?: Severity;
}

export interface DataProfile {
  id: string;
  datasetId: string;
  profiledAt: Date;
  rowCount?: number;
  columnCount?: number;
  sizeBytes?: number;
  columns?: ColumnProfile[];
  correlations?: ColumnCorrelation[];
}

export interface ColumnProfile {
  name: string;
  dataType?: string;
  nullCount?: number;
  nullPercentage?: number;
  distinctCount?: number;
  distinctPercentage?: number;
  min?: string;
  max?: string;
  mean?: number;
  median?: number;
  stdDev?: number;
  topValues?: ValueFrequency[];
}

export interface ValueFrequency {
  value: string;
  count: number;
  percentage?: number;
}

export interface ColumnCorrelation {
  column1: string;
  column2: string;
  correlation?: number;
}

export interface DataLineage {
  id: string;
  datasetId: string;
  upstreamDatasets?: LineageEdge[];
  downstreamDatasets?: LineageEdge[];
  transformations?: string[];
  capturedAt: Date;
  metadata?: object;
}

export interface LineageEdge {
  datasetId: string;
  relationshipType: LineageRelationship;
  transformationId?: string;
  columns?: ColumnLineage[];
}

export interface ColumnLineage {
  sourceColumn: string;
  targetColumn: string;
  transformation?: string;
}

export interface CDCStream {
  id: string;
  name: string;
  sourceId: string;
  destinationId: string;
  captureMode: CaptureMode;
  tables?: string[];
  isActive?: boolean;
  watermark?: string;
  createdAt: Date;
  updatedAt: Date;
}

export interface ChangeEvent {
  id: string;
  streamId: string;
  operationType: OperationType;
  tableName: string;
  primaryKeyValue?: string;
  beforeData?: object;
  afterData?: object;
  timestamp: Date;
  transactionId?: string;
  sequenceNumber?: number;
}

export interface DataObservability {
  id: string;
  pipelineId: string;
  metrics?: ObservabilityMetric[];
  alerts?: DataAlert[];
  sla?: SLA;
  incidents?: DataIncident[];
}

export interface ObservabilityMetric {
  name: string;
  type: MetricType;
  value: number;
  timestamp: Date;
  dimensions?: object;
  unit?: string;
}

export interface DataAlert {
  id: string;
  name: string;
  type: AlertType;
  severity: Severity;
  condition: AlertCondition;
  notificationConfig?: NotificationConfig;
  isActive?: boolean;
  createdAt: Date;
}

export interface AlertCondition {
  metricName: string;
  operator: ComparisonOperator;
  threshold: number;
  window?: number;
  aggregation?: AggregationType;
}

export interface NotificationConfig {
  channels?: NotificationChannel[];
  recipients?: string[];
  template?: string;
}

export interface DataIncident {
  id: string;
  title: string;
  description?: string;
  severity: Severity;
  status: IncidentStatus;
  affectedPipelines?: string[];
  affectedDatasets?: string[];
  rootCause?: string;
  resolution?: string;
  detectedAt: Date;
  resolvedAt?: Date;
}

export interface SLA {
  id: string;
  name: string;
  maxDuration?: number;
  maxLatency?: number;
  minFreshness?: number;
  availabilityTarget?: number;
}

export interface DataCatalog {
  id: string;
  name: string;
  datasets?: DatasetMetadata[];
  glossary?: GlossaryTerm[];
}

export interface DatasetMetadata {
  id: string;
  name: string;
  description?: string;
  owner?: string;
  domain?: string;
  tags?: string[];
  classification?: DataClassification;
  schema?: object;
  location?: string;
  format?: DataFormat;
  partitions?: string[];
  statistics?: DatasetStatistics;
  lineage?: DataLineage;
  createdAt: Date;
  updatedAt: Date;
}

export interface DatasetStatistics {
  rowCount?: number;
  sizeBytes?: number;
  columnCount?: number;
  lastRefreshed?: Date;
  growthRate?: number;
}

export interface GlossaryTerm {
  id: string;
  term: string;
  definition: string;
  synonyms?: string[];
  relatedTerms?: string[];
  owner?: string;
  domain?: string;
}

export interface RetryPolicy {
  maxRetries?: number;
  retryDelay?: number;
  backoffMultiplier?: number;
  maxRetryDelay?: number;
  retryableErrors?: string[];
}

export interface RunMetrics {
  recordsProcessed?: number;
  recordsFailed?: number;
  bytesProcessed?: number;
  duration?: number;
  cpuTime?: number;
  memoryPeakMB?: number;
  cost?: number;
}

export interface TaskMetrics {
  recordsRead?: number;
  recordsWritten?: number;
  recordsFiltered?: number;
  bytesRead?: number;
  bytesWritten?: number;
  duration?: number;
}

export interface LogEntry {
  timestamp: Date;
  level: LogLevel;
  message: string;
  context?: object;
}

// ============================================
// ACTIONS
// ============================================

export interface CreatePipelineParams {
  name: string;
  type: PipelineType;
  tasks: Task[];
  schedule?: Schedule;
}

export interface RunPipelineParams {
  pipelineId: string;
  runType?: RunType;
  parameters?: object;
}

export interface CreateDataSourceParams {
  name: string;
  type: DataSourceType;
  connectionConfig: ConnectionConfig;
}

export interface CreateTransformationParams {
  name: string;
  type: TransformationType;
  logic: TransformationLogic;
}

export interface CreateQualityCheckParams {
  name: string;
  target: string;
  rule: QualityRule;
  severity: Severity;
}

export interface RunQualityCheckParams {
  checkId: string;
}

export interface ProfileDatasetParams {
  datasetId: string;
  sampleSize?: number;
}

export interface TrackLineageParams {
  datasetId: string;
  upstreamDatasets?: string[];
  transformationId?: string;
}

export interface CreateCDCStreamParams {
  name: string;
  sourceId: string;
  destinationId: string;
  captureMode: CaptureMode;
}

export interface CreateDataAlertParams {
  name: string;
  type: AlertType;
  condition: AlertCondition;
}

export interface RegisterDatasetParams {
  name: string;
  description?: string;
  owner?: string;
  schema?: object;
}
