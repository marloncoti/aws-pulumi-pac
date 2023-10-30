"""An AWS Python Pulumi program for aws community day gt"""
import pulumi
import pulumi_aws as aws
import pulumi_awsx as awsx  
from  pulumi_aws.ec2 import  _enums


#constats
project_name = 'community-day-gt'

# config 
config = pulumi.Config('aws-community-day-infra')

mandatory_tags= {
    'const-center': project_name,
    'stack': 'demo-stack',
    'owner': 'frontend-team'
}

# create vpc
vpc =  awsx.ec2.Vpc(
    resource_name= f'{project_name}-vpc',
    number_of_availability_zones=1,
    cidr_block='10.0.0.0/16',
    subnet_specs= [
        awsx.ec2.SubnetSpecArgs(
            type=awsx.ec2.SubnetType.PUBLIC,
            cidr_mask=20,
            name='community-day-public-subnet'
        ),
        awsx.ec2.SubnetSpecArgs(
            type=awsx.ec2.SubnetType.PRIVATE,
            cidr_mask=20,
            name='community-day-private-subnet'
        )
    ],
    tags= {
        'Name': f'{project_name}-vpc'
    }
    #tags = dict(mandatory_tags, Name = f'{project_name}-security-group')

)

## create a security group
web_security_group = aws.ec2.SecurityGroup(
    resource_name=f'{project_name}-security-group',
    vpc_id= vpc.vpc_id,
    name=f'{project_name}-security-group',
    ingress= [
        aws.ec2.SecurityGroupIngressArgs(
            protocol= "tcp", from_port=80, to_port= 80,  cidr_blocks=['0.0.0.0/0']
        ),
        aws.ec2.SecurityGroupIngressArgs(
            protocol= "tcp", from_port=22, to_port= 22,  cidr_blocks=['0.0.0.0/0']
        )
    ],
    tags= {
        'Name': f'{project_name}-security-group'
    }
    # tags = dict(mandatory_tags, Name = f'{project_name}-security-group')
)

## create instances
instance_count = config.get_int('instanceCount')
ami = config.get('ami')
ssh_key =  config.get('ssh_key')

for index in range(instance_count):
    resource_name = f'{project_name}-instance-${index + 1}'
    
    instance = aws.ec2.Instance(
        resource_name=resource_name,
        instance_type = "t2.micro",
        associate_public_ip_address= True,
        ami= ami,
        subnet_id= vpc.public_subnet_ids[0],
        vpc_security_group_ids= [web_security_group.id],
        user_data="""#!/bin/bash
        echo "Hello, World!" > index.html
        nohup busybox httpd -f -p 80 &
        """,
        tags={
            'Name': resource_name
        }
        # tags = dict(mandatory_tags, Name = resource_name)
    )
 




