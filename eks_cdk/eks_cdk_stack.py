
from aws_cdk import core, aws_ec2, aws_iam, aws_eks


class CdkeksStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)


        eks_vpc = aws_ec2.Vpc(
            self, "VPC",
            cidr="10.0.0.0/16"
        )

        # Create IAM Role For EC2 bastion instance to be able to manage the cluster
        bastion_role = aws_iam.Role(
            self, "BastionRole",
            assumed_by=aws_iam.CompositePrincipal(
                aws_iam.ServicePrincipal("ec2.amazonaws.com"),
                aws_iam.AccountRootPrincipal()
            )
        )
        self.bastion_role = bastion_role
        # Create EC2 Instance Profile for that Role
        instance_profile = aws_iam.CfnInstanceProfile(
            self, "InstanceProfile",
            roles=[bastion_role.role_name]            
        )

        # Create SecurityGroup for the Control Plane ENIs
        eks_security_group = aws_ec2.SecurityGroup(
            self, "EKSSecurityGroup",
            vpc=eks_vpc,
            allow_all_outbound=True
        )
        
        eks_security_group.add_ingress_rule(
            aws_ec2.Peer.ipv4('10.0.0.0/16'),
            aws_ec2.Port.all_traffic()
        )    

        # Create an EKS Cluster
        eks_cluster = aws_eks.Cluster(
            self, "cluster",
            vpc=eks_vpc,
            masters_role=bastion_role,
            default_capacity_type=aws_eks.DefaultCapacityType.NODEGROUP,
            default_capacity_instance=aws_ec2.InstanceType("t2.micro"),
            default_capacity=2,
            security_group=eks_security_group,
            endpoint_access=aws_eks.EndpointAccess.PUBLIC_AND_PRIVATE,
            version=aws_eks.KubernetesVersion.V1_18
        )
        
        self.url_output = core.CfnOutput(self, 'CIDR',
            value=eks_vpc.cidr)