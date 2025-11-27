#!/usr/bin/env python3
import os

import aws_cdk as cdk

from cdk_pipeline_lab.cdk_pipeline_lab_stack import CdkPipelineLabStack
from cdk_pipeline_lab.pipeline_stack import PipelineStack


app = cdk.App()

CdkPipelineLabStack(app, "CdkPipelineLabStack")

PipelineStack(app, "PipelineStack")

app.synth()
