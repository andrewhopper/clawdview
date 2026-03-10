/**
 * Configuration tests.
 */

import { describe, it, expect } from 'vitest';
import * as path from 'path';
import * as fs from 'fs';
import { envConfigSchema } from '../config/schema';
import * as yaml from 'yaml';

describe('Configuration', () => {
  const configDir = path.join(__dirname, '../config');
  const envFiles = ['dev.yml', 'stage.yml', 'prod.yml'];

  it.each(envFiles)('validates %s configuration', (fileName) => {
    const filePath = path.join(configDir, fileName);

    if (!fs.existsSync(filePath)) {
      console.warn(`Skipping ${fileName} - file not found`);
      return;
    }

    const fileContents = fs.readFileSync(filePath, 'utf8');
    const rawConfig = yaml.parse(fileContents);
    const env = fileName.replace('.yml', '');

    const result = envConfigSchema.safeParse({ ...rawConfig, env });

    if (!result.success) {
      console.error(`Validation errors for ${fileName}:`, result.error.format());
    }

    expect(result.success).toBe(true);
  });

  it('has required notification emails', () => {
    const devConfig = yaml.parse(
      fs.readFileSync(path.join(configDir, 'dev.yml'), 'utf8')
    );

    expect(devConfig.notifications).toBeDefined();
    expect(devConfig.notifications.adminEmail).toBeDefined();
  });
});
