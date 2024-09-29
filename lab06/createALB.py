import boto3
import botocore
import os

student_number = "23905652"
region = "ap-southeast-1"

ec2 = boto3.client('ec2', region_name=region)
elbv2 = boto3.client('elbv2', region_name=region)

def create_load_balancer(security_group_id, subnet_ids):
    response = elbv2.create_load_balancer(
        Name=f'{student_number}-alb',
        Subnets=subnet_ids,
        SecurityGroups=[security_group_id],
        Scheme='internet-facing',
        Type='application',
        Tags=[
            {
                'Key': 'Name',
                'Value': f'{student_number}-alb'
            },
        ]
    )
    return response['LoadBalancers'][0]['LoadBalancerArn']

def create_target_group(vpc_id):
    response = elbv2.create_target_group(
        Name=f'{student_number}-tg',
        Protocol='HTTP',
        Port=80,
        VpcId=vpc_id,
        HealthCheckPort='80',
        HealthCheckProtocol='HTTP',
        HealthCheckPath='/polls/',
        HealthCheckIntervalSeconds=30,
        HealthCheckTimeoutSeconds=5,
        HealthyThresholdCount=5,
        UnhealthyThresholdCount=2,
        Matcher={
            'HttpCode': '200'
        },
        TargetType='instance'
    )
    return response['TargetGroups'][0]['TargetGroupArn']

def create_listener(load_balancer_arn, target_group_arn):
    response = elbv2.create_listener(
        LoadBalancerArn=load_balancer_arn,
        Protocol='HTTP',
        Port=80,
        DefaultActions=[
            {
                'Type': 'forward',
                'TargetGroupArn': target_group_arn
            }
        ]
    )
    return response['Listeners'][0]['ListenerArn']

def register_targets(target_group_arn, instance_ids):
    targets = [{'Id': instance_id} for instance_id in instance_ids]

    elbv2.register_targets(
        TargetGroupArn=target_group_arn,
        Targets=targets
    )

def main():

    # Create Application Load Balancer
    vpc_id = 'vpc-0ad7c05df6174aa82'
    subnet_ids = ['subnet-0859ff38bfce967b8', 'subnet-056a5c6c3bd465883']
    security_group_id = 'sg-05c6c36862582b514'
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