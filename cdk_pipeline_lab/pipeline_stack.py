from aws_cdk import (
    Stack,
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as codepipeline_actions,
    aws_codebuild as codebuild,
)
from constructs import Construct

class PipelineStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Student ID prefix
        student_id = "9026254"

        # Connection ARN
        connection_arn = "arn:aws:codeconnections:us-east-1:867344462708:connection/9462f619-d105-410c-b8fb-feb930ccbac5"

        # Create the pipeline
        pipeline = codepipeline.Pipeline(
            self, f"{student_id}-CdkPipeline",
            pipeline_name=f"{student_id}-CdkPipeline"
        )

        # Source stage
        source_output = codepipeline.Artifact()
        source_action = codepipeline_actions.CodeStarConnectionsSourceAction(
            action_name="GitHub_Source",
            owner="NikhilShankar",
            repo="CICD-Lab3",
            branch="master",
            output=source_output,
            connection_arn=connection_arn
        )

        pipeline.add_stage(
            stage_name="Source",
            actions=[source_action]
        )

        # Build stage
        build_output = codepipeline.Artifact()
        build_project = codebuild.PipelineProject(
            self, f"{student_id}-CdkBuild",
            project_name=f"{student_id}-CdkBuild",
            environment=codebuild.BuildEnvironment(
                build_image=codebuild.LinuxBuildImage.STANDARD_7_0
            ),
            build_spec=codebuild.BuildSpec.from_source_filename("buildspec.yml")
        )

        build_action = codepipeline_actions.CodeBuildAction(
            action_name="CDK_Build",
            project=build_project,
            input=source_output,
            outputs=[build_output]
        )

        pipeline.add_stage(
            stage_name="Build",
            actions=[build_action]
        )