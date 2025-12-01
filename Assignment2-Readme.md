Steps:
Part 1: AWS CDK Project Setup
Set up a new AWS CDK project:

Initialize a new AWS CDK project in your preferred programming language (TypeScript, Python, or Java). For this example, we will use TypeScript.
mkdir my-cdk-project
cd my-cdk-project
cdk init app --language=typescript
Create Resources Using AWS CDK:

Inside your CDK project, open the lib/my-cdk-project-stack.ts (or the equivalent file for your language) and define the following resources:

Amazon S3 Bucket:

import * as cdk from 'aws-cdk-lib';
import * as s3 from 'aws-cdk-lib/aws-s3';

export class MyCdkProjectStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);
    
    // Create S3 bucket
    new s3.Bucket(this, 'MyFirstBucket', {
      versioned: true,
      removalPolicy: cdk.RemovalPolicy.DESTROY,  // Only for dev/test environments
    });
  }
}
AWS Lambda Function:

import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as s3 from 'aws-cdk-lib/aws-s3';

const myLambda = new lambda.Function(this, 'MyLambda', {
  runtime: lambda.Runtime.NODEJS_14_X,
  handler: 'index.handler',
  code: lambda.Code.fromInline(`
    exports.handler = async function(event) {
      console.log('Lambda invoked!');
      return { statusCode: 200, body: 'Hello, World!' };
    }
  `),
  environment: {
    BUCKET_NAME: myBucket.bucketName,
  },
});
Amazon DynamoDB Table:

import * as dynamodb from 'aws-cdk-lib/aws-dynamodb';

const myTable = new dynamodb.Table(this, 'MyTable', {
  partitionKey: { name: 'id', type: dynamodb.AttributeType.STRING },
  tableName: 'MyTable',
  removalPolicy: cdk.RemovalPolicy.DESTROY,  // Only for dev/test environments
});
Deploy the resources:

To deploy your CDK stack, run the following commands:

cdk synth
cdk deploy
Ensure that the resources are successfully created in the AWS console.

Part 2: Set up GitHub Repository for Source Control
Create a GitHub Repository

Link GitHub to AWS CodePipeline:

Go to the AWS CodePipeline console.
Create a new pipeline, selecting GitHub as the source provider.
You will need to authenticate to GitHub and select your repository and branch (e.g., master or main).
Part 3: Set up AWS CodePipeline
Create a CodePipeline for Continuous Integration/Continuous Deployment:

You will use AWS CodePipeline to automate the process of deploying your resources when changes are pushed to your GitHub repository.

Steps:

Source Stage: Configure the source stage to pull code from your GitHub repository. Select the repository and branch that contains your AWS CDK code.

Build Stage: Set up a build stage to use AWS CodeBuild for compiling and synthesizing your AWS CDK stack.

Create a buildspec.yml file in the root of your GitHub repository to define the build process.
Example buildspec.yml:

version: 0.2
phases:
  install:
    commands:
      - npm install -g aws-cdk
      - npm install
  build:
    commands:
      - cdk synth
      - cdk deploy --require-approval never
artifacts:
  files:
    - '**/*'
Deploy Stage: Once the build completes successfully, add a deploy stage to your pipeline. Use AWS CloudFormation (via AWS CDK) to deploy the resources.

Connect the Pipeline:

Once your pipeline is created, verify that it runs correctly by pushing new changes to your GitHub repository.
Each time you push to GitHub, CodePipeline should automatically trigger the build and deploy process.
Part 4: Testing the Pipeline
Test the Setup:

Make changes to your AWS CDK code in the GitHub repository (e.g., modify the Lambda function or S3 bucket).
Push the changes to GitHub.
Observe the AWS CodePipeline console to ensure that the changes trigger a new pipeline execution, resulting in updated resources.
Verify Deployment:

Check the AWS Console to verify the resources:
S3 Bucket should exist and be accessible.
Lambda Function should be listed and executable.
DynamoDB Table should be created and accessible.
Submission Instructions:
GitHub Repository URL: Submit the link to your GitHub repository containing the AWS CDK code.
AWS Console Verification: Provide screenshots or a brief description of your deployed AWS resources in the console (S3, Lambda, DynamoDB).
CodePipeline Execution Logs: Submit the logs or status screenshots showing the successful execution of your CodePipeline.