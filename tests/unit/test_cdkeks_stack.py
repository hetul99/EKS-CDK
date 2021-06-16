import json
import pytest

from aws_cdk import core
from cdkeks.cdkeks_stack import CdkeksStack


def get_template():
    app = core.App()
    CdkeksStack(app, "cdkeks")
    return json.dumps(app.synth().get_stack("cdkeks").template)


def test_sqs_queue_created():
    assert("AWS::SQS::Queue" in get_template())


def test_sns_topic_created():
    assert("AWS::SNS::Topic" in get_template())
