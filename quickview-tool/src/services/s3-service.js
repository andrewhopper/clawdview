const { S3Client, PutObjectCommand, GetObjectCommand, HeadObjectCommand } = require('@aws-sdk/client-s3');
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

class S3Service {
  constructor(options = {}) {
    this.bucket = options.bucket || process.env.QV_S3_BUCKET;
    this.prefix = options.prefix || process.env.QV_S3_PREFIX || 'quickview-shares';
    this.region = options.region || process.env.AWS_REGION || process.env.QV_S3_REGION || 'us-east-1';
    this.urlExpiresIn = options.urlExpiresIn || parseInt(process.env.QV_S3_URL_EXPIRES, 10) || 3600;

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
    return `${this.prefix}/${id}/${safeName}`;
  }

  _getContentType(filename) {
    const ext = path.extname(filename).toLowerCase();
    return CONTENT_TYPE_MAP[ext] || 'application/octet-stream';
  }

  /**
   * Upload a file to S3 and return the object key.
   */
  async upload(filename, content, options = {}) {
    if (!this.isConfigured()) {
      throw new Error('S3 is not configured. Set QV_S3_BUCKET environment variable.');
    }

    const key = options.key || this._buildKey(filename);
    const contentType = this._getContentType(filename);

    const command = new PutObjectCommand({
      Bucket: this.bucket,
      Key: key,
      Body: content,
      ContentType: contentType,
    });

    await this.client.send(command);

    return { key, bucket: this.bucket, contentType };
  }

  /**
   * Publish a file to S3 with public-read ACL and return its public URL.
   */
  async publish(filename, content) {
    if (!this.isConfigured()) {
      throw new Error('S3 is not configured. Set QV_S3_BUCKET environment variable.');
    }

    const key = this._buildKey(filename);
    const contentType = this._getContentType(filename);

    const command = new PutObjectCommand({
      Bucket: this.bucket,
      Key: key,
      Body: content,
      ContentType: contentType,
      ACL: 'public-read',
    });

    await this.client.send(command);

    const publicUrl = this._buildPublicUrl(key);
    return { key, bucket: this.bucket, contentType, publicUrl };
  }

  /**
   * Generate a pre-signed URL for an already-uploaded object.
   */
  async getPresignedUrl(key, expiresIn) {
    if (!this.isConfigured()) {
      throw new Error('S3 is not configured. Set QV_S3_BUCKET environment variable.');
    }

    const command = new GetObjectCommand({
      Bucket: this.bucket,
      Key: key,
    });

    const url = await getSignedUrl(this.client, command, {
      expiresIn: expiresIn || this.urlExpiresIn,
    });

    return url;
  }

  /**
   * Upload a file and immediately return a pre-signed URL for sharing.
   */
  async shareWithPresignedUrl(filename, content, expiresIn) {
    const { key, bucket, contentType } = await this.upload(filename, content);
    const url = await this.getPresignedUrl(key, expiresIn);

    return { key, bucket, contentType, url, expiresIn: expiresIn || this.urlExpiresIn };
  }

  _buildPublicUrl(key) {
    const endpoint = process.env.QV_S3_ENDPOINT;
    if (endpoint) {
      return `${endpoint.replace(/\/$/, '')}/${this.bucket}/${key}`;
    }
    return `https://${this.bucket}.s3.${this.region}.amazonaws.com/${key}`;
  }
}

module.exports = S3Service;
