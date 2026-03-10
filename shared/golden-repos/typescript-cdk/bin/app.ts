#!/usr/bin/env node
/**
 * CDK application entry point.
 * Supports multi-context, multi-stage deployments.
 */

import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import { loadConfig, getContext, getStage } from '../config';
import { ApiStack } from '../lib/stacks/api-stack';
import { MonitoringStack } from '../lib/stacks/monitoring-stack';

// Load configuration for current context and stage
const config = loadConfig();

console.log(`\n🚀 Deploying Infrastructure`);
console.log(`   Context: ${config.context}`);
console.log(`   Stage: ${config.stage}`);
console.log(`   Account: ${config.account}`);
console.log(`   Region: ${config.region}`);
console.log(`   Project: ${config.projectName}\n`);

const app = new cdk.App();

// Monitoring stack (deploy first for alert topic)
const monitoring = new MonitoringStack(app, 'Monitoring', { config });

// API stack
const api = new ApiStack(app, 'Api', { config });

// Add dependencies if needed
api.addDependency(monitoring);

app.synth();
