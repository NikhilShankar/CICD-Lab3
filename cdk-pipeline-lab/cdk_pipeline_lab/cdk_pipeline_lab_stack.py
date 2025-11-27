from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    aws_s3 as s3,
)
from constructs import Construct

class CdkPipelineLabStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create S3 bucket
        bucket = s3.Bucket(self, "MyBucket")

        # Create Lambda function
        my_lambda = _lambda.Function(
            self, "HelloLambda",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="index.handler",
            code=_lambda.Code.from_asset("lambda")
        )

        # Create API Gateway
        api = apigw.LambdaRestApi(
            self, "HelloApi",
            handler=my_lambda,
            proxy=False
        )

        # Add /hello endpoint
        hello = api.root.add_resource("hello")
        hello.add_method("GET")