#!/usr/bin/env python3
import os

from aws_cdk import core as cdk
from eks_cdk.eks_cdk_stack import CdkeksStack
from eks_cdk.pipeline_stack import PipelineStack

# For consistency with TypeScript code, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core

from eks_cdk.eks_cdk_stack import CdkeksStack


app = core.App()
CdkeksStack(app, "ekscdk")
PipelineStack(app, 'PipelineStack', env={
    'account': '128222158613',
    'region': 'us-west-2',
})
    

app.synth()
