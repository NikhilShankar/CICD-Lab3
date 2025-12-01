from aws_cdk import (
    Stack,
    RemovalPolicy,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    aws_s3 as s3,
    aws_dynamodb as dynamodb,
)
from constructs import Construct

class CdkPipelineLabStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Student ID prefix
        student_id = "9026254"

        # Create S3 bucket
        bucket = s3.Bucket(
            self, f"{student_id}-MyBucket",
            bucket_name=f"{student_id}-my-bucket",
            removal_policy=RemovalPolicy.DESTROY
        )

        # Create DynamoDB table for quotes
        quotes_table = dynamodb.Table(
            self, f"{student_id}-QuotesTable",
            table_name=f"{student_id}-QuotesTable",
            partition_key=dynamodb.Attribute(
                name="id",
                type=dynamodb.AttributeType.STRING
            ),
            removal_policy=RemovalPolicy.DESTROY
        )

        # Create Lambda function
        my_lambda = _lambda.Function(
            self, f"{student_id}-HelloLambda",
            function_name=f"{student_id}-HelloLambda",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="index.handler",
            code=_lambda.Code.from_asset("lambda"),
            environment={
                "QUOTES_TABLE_NAME": quotes_table.table_name,
                "BUCKET_NAME": bucket.bucket_name
            }
        )

        # Grant Lambda permissions to read/write DynamoDB
        quotes_table.grant_read_write_data(my_lambda)

        # Grant Lambda permissions to read/write S3
        bucket.grant_read_write(my_lambda)

        # Create API Gateway
        api = apigw.LambdaRestApi(
            self, f"{student_id}-HelloApi",
            rest_api_name=f"{student_id}-HelloApi",
            handler=my_lambda,
            proxy=False
        )

        # Add /hello endpoint
        hello = api.root.add_resource("hello")
        hello.add_method("GET")