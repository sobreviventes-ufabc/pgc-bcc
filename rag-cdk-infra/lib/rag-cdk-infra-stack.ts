import * as cdk from "aws-cdk-lib";
import { Construct } from "constructs";

import {
  DockerImageFunction,
  DockerImageCode,
  Architecture,
} from "aws-cdk-lib/aws-lambda";
import * as apigateway from "aws-cdk-lib/aws-apigateway";
import * as dotenv from "dotenv";
import * as path from "path";

export class RagCdkInfraStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // Load environment variables from back-end/.env
    const envPath = path.join(__dirname, "../../back-end/.env");
    dotenv.config({ path: envPath });
    
    // Read environment variables after loading
    const envVars = dotenv.parse(require('fs').readFileSync(envPath));

    // Validate required environment variables
    const requiredVars = ['API_KEY', 'OPENAI_API_KEY', 'NOMIC_KEY'];
    const missingVars = requiredVars.filter(varName => !envVars[varName]);
    
    if (missingVars.length > 0) {
      throw new Error(
        `Missing required environment variables in back-end/.env: ${missingVars.join(', ')}`
      );
    }

    // Function to handle the API requests. Uses same base image, but different handler.
    const apiImageCode = DockerImageCode.fromImageAsset("../back-end", {
      cmd: ["rag_pipeline/api.handler"],
      buildArgs: {
        platform: "linux/amd64",
      },
    });
    const apiFunction = new DockerImageFunction(this, "ApiFunc", {
      code: apiImageCode,
      memorySize: 2048,  // Increased memory for faster processing
      timeout: cdk.Duration.seconds(900),  // Max Lambda timeout (15 minutes)
      architecture: Architecture.X86_64,
      environment: {
        GROQ_API_KEY: envVars.GROQ_API_KEY || "",
        OPENAI_API_KEY: envVars.OPENAI_API_KEY || "",
        OLLAMA_BASE_URL: "http://localhost:11434",
        MODEL_PROVIDER: "openai",
        EMBEDDINGS_PROVIDER: "nomic", 
        NOMIC_KEY: envVars.NOMIC_KEY || "",
        TABLE_NAME: envVars.TABLE_NAME || "",
        NLTK_DATA: "/tmp/nltk_data",
        MPLCONFIGDIR: "/tmp/matplotlib",
        HOME: "/tmp",
      },
    });

    // Create API Gateway REST API
    const api = new apigateway.RestApi(this, "RagApi", {
      restApiName: "RAG Service API",
      description: "API Gateway for RAG Lambda with API Key authentication",
      defaultCorsPreflightOptions: {
        allowOrigins: apigateway.Cors.ALL_ORIGINS,
        allowMethods: apigateway.Cors.ALL_METHODS,
        allowHeaders: [
          "Content-Type",
          "X-Amz-Date",
          "Authorization",
          "X-Api-Key",
          "X-Amz-Security-Token",
        ],
      },
      deployOptions: {
        stageName: "prod",
      },
    });

    const lambdaIntegration = new apigateway.LambdaIntegration(apiFunction, {
      requestTemplates: { "application/json": '{ "statusCode": "200" }' },
    });

    const healthResource = api.root.addResource("health");
    healthResource.addMethod("GET", lambdaIntegration, { apiKeyRequired: true });

    const askResource = api.root.addResource("ask");
    askResource.addMethod("POST", lambdaIntegration, { apiKeyRequired: true });

    const chatResource = api.root.addResource("chat");
    chatResource.addMethod("POST", lambdaIntegration, { apiKeyRequired: true });

    // Ensure API_KEY is defined
    const apiKeyValue = envVars.API_KEY;
    if (!apiKeyValue) {
      throw new Error(
        "API_KEY environment variable is required. Please set it in back-end/.env file."
      );
    }

    const apiKey = api.addApiKey("RagApiKey", {
      apiKeyName: "rag-api-key",
      value: apiKeyValue,
    });

    // Create Usage Plan to control API usage and prevent abuse
    const usagePlan = api.addUsagePlan("RagUsagePlan", {
      name: "RAG API Usage Plan", // Display name in AWS Console
      throttle: {
        rateLimit: 5,    // Maximum requests per second (steady-state rate)
        burstLimit: 20,   // Maximum concurrent requests allowed in a burst
      },
      quota: {
        limit: 10000,                   // Maximum number of requests allowed
        period: apigateway.Period.DAY, // Time period for the quota (per day)
      },
    });

    // Associate API Key with Usage Plan
    usagePlan.addApiKey(apiKey);
    usagePlan.addApiStage({
      stage: api.deploymentStage,
    });

    // Output the API Gateway URL and API Key
    new cdk.CfnOutput(this, "ApiGatewayUrl", {
      value: api.url,
      description: "API Gateway endpoint URL",
    });

    new cdk.CfnOutput(this, "ApiKeyId", {
      value: apiKey.keyId,
      description: "API Key ID (retrieve value from AWS Console)",
    });
  }
}