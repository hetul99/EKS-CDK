from aws_cdk import core

from .cdk_eks_1_stack import CdkeksStack

class WebServiceStage(core.Stage):
  def __init__(self, scope: core.Construct, id: str, **kwargs):
    super().__init__(scope, id, **kwargs)

    service = CdkeksStack(self, 'WebService')

    self.url_output = service.url_output