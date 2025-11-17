import * as cdk from "aws-cdk-lib";
import { Construct } from "constructs";

import {
  DockerImageFunction,
  DockerImageCode,
  FunctionUrlAuthType,
  Architecture,
} from "aws-cdk-lib/aws-lambda";

export class RagCdkInfraStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // Function to handle the API requests. Uses same base image, but different handler.
    const apiImageCode = DockerImageCode.fromImageAsset("../back-end", {
      cmd: ["rag_pipeline/api.handler"],
      buildArgs: {
        platform: "linux/amd64",
      },
    });
    const apiFunction = new DockerImageFunction(this, "ApiFunc", {
      code: apiImageCode,
      memorySize: 1024,
      timeout: cdk.Duration.seconds(300),
      architecture: Architecture.X86_64,
      environment: {
        GROQ_API_KEY: process.env.GROQ_API_KEY || "",
        OPENAI_API_KEY: process.env.OPENAI_API_KEY || "",
        OLLAMA_BASE_URL: "http://localhost:11434",
        MODEL_PROVIDER: "groq",
        EMBEDDINGS_PROVIDER: "nomic", 
        NOMIC_KEY: process.env.NOMIC_KEY || "",
        TABLE_NAME: process.env.TABLE_NAME || "",
        NLTK_DATA: "/tmp/nltk_data",
        MPLCONFIGDIR: "/tmp/matplotlib",
        HOME: "/tmp",
      },
    });

    // Public URL for the API function.
    const functionUrl = apiFunction.addFunctionUrl({
      authType: FunctionUrlAuthType.NONE,
    });

    // Output the URL for the API function.
    new cdk.CfnOutput(this, "FunctionUrl", {
      value: functionUrl.url + "health",
    });
  }
}