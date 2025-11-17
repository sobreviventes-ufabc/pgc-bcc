#!/usr/bin/env node
import 'dotenv/config';
import * as dotenv from 'dotenv';
import * as path from 'path';
import * as fs from 'fs';
import * as cdk from 'aws-cdk-lib';
import { RagCdkInfraStack } from '../lib/rag-cdk-infra-stack';

// Load environment variables from back-end/.env using multiple possible paths
const possiblePaths = [
  path.join(__dirname, '../../back-end/.env'),  // From compiled JS in cdk.out
  path.join(__dirname, '../back-end/.env'),     // From bin directory
  path.join(process.cwd(), '../back-end/.env'), // From current working directory
  path.join(process.cwd(), 'back-end/.env'),    // If run from project root
];

let envPath: string | undefined;
for (const testPath of possiblePaths) {
  const resolvedPath = path.resolve(testPath);
  if (fs.existsSync(resolvedPath)) {
    envPath = resolvedPath;
    break;
  }
}

if (envPath) {
  dotenv.config({ path: envPath });
  console.log(`Loading environment variables from: ${envPath}`);
} else {
  console.error('❌ ERROR: Could not find back-end/.env file in any expected location');
  console.error('Expected locations:');
  possiblePaths.forEach(p => console.error(`  - ${path.resolve(p)}`));
  console.error('\nPlease ensure the back-end/.env file exists with required environment variables.');
  process.exit(1);
}

const app = new cdk.App();
new RagCdkInfraStack(app, 'RagCdkInfraStack', {
  /* If you don't specify 'env', this stack will be environment-agnostic.
   * Account/Region-dependent features and context lookups will not work,
   * but a single synthesized template can be deployed anywhere. */

  /* Uncomment the next line to specialize this stack for the AWS Account
   * and Region that are implied by the current CLI configuration. */
  // env: { account: process.env.CDK_DEFAULT_ACCOUNT, region: process.env.CDK_DEFAULT_REGION },

  /* Uncomment the next line if you know exactly what Account and Region you
   * want to deploy the stack to. */
  // env: { account: '123456789012', region: 'us-east-1' },

  /* For more information, see https://docs.aws.amazon.com/cdk/latest/guide/environments.html */
});