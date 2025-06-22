import boto3
import botocore
import os

# Student identifier used for naming resources
student_number = "23905652"

# AWS region where resources will be created
region = "ap-southeast-1"

# Initialize AWS service clients
ec2 = boto3.client('ec2', region_name=region)
elbv2 = boto3.client('elbv2', region_name=region)

def create_load_balancer(security_group_id, subnet_ids):
    """
    Create an Application Load Balancer (ALB) in the specified subnets with the given security group.
    
    :param security_group_id: ID of the security group to associate with the ALB
    :param subnet_ids: List of subnet IDs where the ALB will be created
    :return: ARN (Amazon Resource Name) of the created load balancer
    """
    response = elbv2.create_load_balancer(
        Name=f'{student_number}-alb', # Unique name for the ALB
        Subnets=subnet_ids, # Subnets where the ALB will be placed
        SecurityGroups=[security_group_id], # Security group for the ALB
        Scheme='internet-facing', # Makes the ALB accessible from the internet
        Type='application',  # Specifies an Application Load Balancer
        Tags=[
            {
                'Key': 'Name',
                'Value': f'{student_number}-alb'
            },
        ]
    )
    return response['LoadBalancers'][0]['LoadBalancerArn']

def create_target_group(vpc_id):
    """
    Create a target group for the ALB to route requests to EC2 instances.
    
    :param vpc_id: ID of the VPC where the target group will be created
    :return: ARN of the created target group
    """
    response = elbv2.create_target_group(
        Name=f'{student_number}-tg',  # Unique name for the target group
        Protocol='HTTP',  # Protocol used by the targets
        Port=80,  # Port on which the targets receive traffic
        VpcId=vpc_id,  # VPC where the target group is created
        HealthCheckPort='80',  # Port used for health checks
        HealthCheckProtocol='HTTP',  # Protocol used for health checks
        HealthCheckPath='/polls/',  # Path used for health checks
        HealthCheckIntervalSeconds=30,  # Time between health checks
        HealthCheckTimeoutSeconds=5,  # Timeout for health check responses
        HealthyThresholdCount=5,  # Number of successful checks to consider a target healthy
        UnhealthyThresholdCount=2,  # Number of failed checks to consider a target unhealthy
        Matcher={
            'HttpCode': '200'  # HTTP status code indicating a healthy target
        },
        TargetType='instance'  # Targets are EC2 instances
    )
    return response['TargetGroups'][0]['TargetGroupArn']

def create_listener(load_balancer_arn, target_group_arn):
    """
    Create a listener for the ALB to forward traffic to the target group.
    
    :param load_balancer_arn: ARN of the ALB
    :param target_group_arn: ARN of the target group
    :return: ARN of the created listener
    """
    response = elbv2.create_listener(
        LoadBalancerArn=load_balancer_arn,  # ALB to attach the listener to
        Protocol='HTTP',  # Protocol for incoming traffic
        Port=80,  # Port for incoming traffic
        DefaultActions=[
            {
                'Type': 'forward',  # Action type to forward traffic
                'TargetGroupArn': target_group_arn  # Target group to forward traffic to
            }
        ]
    )
    return response['Listeners'][0]['ListenerArn']

def register_targets(target_group_arn, instance_ids):
    """
    Register EC2 instances as targets in the target group.
    
    :param target_group_arn: ARN of the target group
    :param instance_ids: List of EC2 instance IDs to register
    """
    targets = [{'Id': instance_id} for instance_id in instance_ids]

    elbv2.register_targets(
        TargetGroupArn=target_group_arn,
        Targets=targets
    )

def main():

    # VPC and subnet IDs where the ALB and targets will be created
    vpc_id = 'vpc-0ad7c05df6174aa82'
    subnet_ids = ['subnet-0859ff38bfce967b8', 'subnet-056a5c6c3bd465883']
    
    # Security group ID for the ALB
    security_group_id = 'sg-05c6c36862582b514'
    
    # EC2 instance IDs to be registered as targets
    instance_ids = ['i-0114649b83dfc2d8a', 'i-046e7533e262ada51']

    print("Creating Application Load Balancer...")
    load_balancer_arn = create_load_balancer(security_group_id, subnet_ids)
    print(f"Load Balancer created: {load_balancer_arn}")

    print("Creating Target Group...")
    target_group_arn = create_target_group(vpc_id)
    print(f"Target Group created: {target_group_arn}")

    print("Creating listener...")
    listener_arn = create_listener(load_balancer_arn, target_group_arn)
    print(f"Listener created: {listener_arn}")

    print("Registering targets...")
    register_targets(target_group_arn, instance_ids)
    print("Targets registered")

    print("Setup complete!")

if __name__ == "__main__":
    main()