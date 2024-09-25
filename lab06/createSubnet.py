import boto3
import botocore
import time

student_number = "23905652"
region = "ap-southeast-1"

ec2 = boto3.client('ec2', region_name=region)
elbv2 = boto3.client('elbv2', region_name=region)

def get_subnets(vpc_id):
    response = ec2.describe_subnets(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])
    return response['Subnets']

def create_new_instance(vpc_id, existing_subnet, security_group_id):
    # Get all availability zones
    azs = [az['ZoneName'] for az in ec2.describe_availability_zones()['AvailabilityZones']]
    
    # Choose a different AZ
    new_az = next(az for az in azs if az != existing_subnet['AvailabilityZone'])
    
    # Check if there's already a subnet in the new AZ
    subnets = get_subnets(vpc_id)
    new_subnet = next((s for s in subnets if s['AvailabilityZone'] == new_az), None)
    
    if not new_subnet:
        # Create a new subnet if one doesn't exist
        cidr_block = '10.0.{}.0/24'.format(len(subnets) + 1)
        new_subnet = ec2.create_subnet(VpcId=vpc_id, CidrBlock=cidr_block, AvailabilityZone=new_az)['Subnet']
        print(f"Created new subnet: {new_subnet['SubnetId']} in {new_az}")
    else:
        print(f"Using existing subnet: {new_subnet['SubnetId']} in {new_az}")
    
    # Create a new instance
    response = ec2.run_instances(
        ImageId='ami-0f74c08b8b5effa56',  # Amazon Linux 2 AMI ID for ap-southeast-1
        InstanceType='t2.micro',
        MaxCount=1,
        MinCount=1,
        NetworkInterfaces=[{
            'SubnetId': new_subnet['SubnetId'],
            'DeviceIndex': 0,
            'AssociatePublicIpAddress': True,
            'Groups': [security_group_id]
        }],
        TagSpecifications=[{
            'ResourceType': 'instance',
            'Tags': [{'Key': 'Name', 'Value': f'{student_number}-new-instance'}]
        }]
    )
    
    new_instance_id = response['Instances'][0]['InstanceId']
    
    # Wait for the instance to be running
    waiter = ec2.get_waiter('instance_running')
    waiter.wait(InstanceIds=[new_instance_id])
    
    return new_instance_id, new_subnet['SubnetId']

def main():

    vpc_id = 'vpc-0ad7c05df6174aa82'
    existing_subnet_id = 'subnet-056a5c6c3bd465883'
    security_group_id = 'sg-0f9e2da7d76e55014'
    existing_instance_id = 'i-0d74b68d7cd4677d7'
    
    existing_subnet = next(s for s in get_subnets(vpc_id) if s['SubnetId'] == existing_subnet_id)
    
    print("Creating new EC2 instance in a different Availability Zone...")
    new_instance_id, new_subnet_id = create_new_instance(vpc_id, existing_subnet, security_group_id)
    print(f"New instance created: {new_instance_id}")
    print(f"New subnet ID: {new_subnet_id}")
    
    subnet_ids = [existing_subnet_id, new_subnet_id]
    print(f"Using subnet IDs for ALB: {subnet_ids}")

if __name__ == "__main__":
    main()