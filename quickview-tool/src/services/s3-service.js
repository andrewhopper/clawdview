const { S3Client, PutObjectCommand, GetObjectCommand } = require('@aws-sdk/client-s3');
const { getSignedUrl } = require('@aws-sdk/s3-request-presigner');
const path = require('path');
const crypto = require('crypto');

const CONTENT_TYPE_MAP = {
  '.html': 'text/html',
  '.jsx': 'text/javascript',
  '.js': 'application/javascript',
  '.py': 'text/x-python',
  '.css': 'text/css',
  '.json': 'application/json',
  '.md': 'text/markdown',
  '.svg': 'image/svg+xml',
  '.txt': 'text/plain',
  '.xml': 'application/xml',
  '.yaml': 'text/yaml',
  '.yml': 'text/yaml',
};

const MAX_EXPIRES_IN = 604800; // 7 days (AWS maximum)
const MIN_EXPIRES_IN = 60;     // 1 minute

class S3Service {
  constructor(options = {}) {
    this.bucket = options.bucket || process.env.QV_S3_BUCKET;
    this.prefix = options.prefix || process.env.QV_S3_PREFIX || 'quickview-shares';
    this.region = options.region || process.env.AWS_REGION || process.env.QV_S3_REGION || 'us-east-1';
    this.urlExpiresIn = options.urlExpiresIn || parseInt(process.env.QV_S3_URL_EXPIRES, 10) || 3600;
    this.projectName = options.projectName || process.env.QV_PROJECT_NAME || 'default';
    this.sessionId = options.sessionId || crypto.randomBytes(4).toString('hex');

    const clientConfig = { region: this.region };

    if (options.endpoint || process.env.QV_S3_ENDPOINT) {
      clientConfig.endpoint = options.endpoint || process.env.QV_S3_ENDPOINT;
      clientConfig.forcePathStyle = true;
    }

    if (options.accessKeyId || process.env.QV_S3_ACCESS_KEY_ID) {
      clientConfig.credentials = {
        accessKeyId: options.accessKeyId || process.env.QV_S3_ACCESS_KEY_ID,
        secretAccessKey: options.secretAccessKey || process.env.QV_S3_SECRET_ACCESS_KEY,
      };
    }

    this.client = new S3Client(clientConfig);
  }

  isConfigured() {
    return !!this.bucket;
  }

  _buildKey(filename) {
    const id = crypto.randomBytes(8).toString('hex');
    const safeName = path.basename(filename).replace(/[^a-zA-Z0-9._-]/g, '_');
    const safeProject = this.projectName.replace(/[^a-zA-Z0-9._-]/g, '_');
    return `${this.prefix}/${safeProject}/${this.sessionId}/${id}-${safeName}`;
  }

  _getContentType(filename) {
    const ext = path.extname(filename).toLowerCase();
    return CONTENT_TYPE_MAP[ext] || 'application/octet-stream';
  }

  _clampExpiresIn(expiresIn) {
    const value = expiresIn || this.urlExpiresIn;
    return Math.max(MIN_EXPIRES_IN, Math.min(MAX_EXPIRES_IN, value));
  }

  /**
   * Upload a file to S3 and return a pre-signed URL for sharing.
   */
  async share(filename, content, expiresIn) {
    if (!this.isConfigured()) {
      throw new Error('S3 is not configured. Set QV_S3_BUCKET environment variable.');
    }

    const key = this._buildKey(filename);
    const contentType = this._getContentType(filename);
    const clampedExpiry = this._clampExpiresIn(expiresIn);

    await this.client.send(new PutObjectCommand({
      Bucket: this.bucket,
      Key: key,
      Body: content,
      ContentType: contentType,
    }));

    const url = await getSignedUrl(this.client, new GetObjectCommand({
      Bucket: this.bucket,
      Key: key,
    }), { expiresIn: clampedExpiry });

    return { key, bucket: this.bucket, contentType, url, expiresIn: clampedExpiry };
  }
}

module.exports = S3Service;
