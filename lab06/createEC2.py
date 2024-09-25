import boto3
import os
import sys

# Student information
student_number = "23905652"
region = "ap-southeast-1"
ami_id = "ami-0497a974f8d5dcef8"

# Initialize the EC2 client
ec2 = boto3.client('ec2', region_name=region)

def create_security_group():
    try:
        response = ec2.create_security_group(
            GroupName=f"{student_number}-sg",
            Description="Security group for development environment"
        )
        security_group_id = response['GroupId']
        
        ec2.authorize_security_group_ingress(
            GroupId=security_group_id,
            IpPermissions=[
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 80,
                    'ToPort': 80,
                    'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                },
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 22,
                    'ToPort': 22,
                    'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                }
            ]
        )
        print(f"Security Group created successfully: {security_group_id}")
        return security_group_id
    except Exception as e:
        print(f"Error creating security group: {e}")
        sys.exit(1)

def create_key_pair():
    try:
        key_name = f"{student_number}-key"
        response = ec2.create_key_pair(KeyName=key_name)
        private_key = response['KeyMaterial']
        private_key_file = f"{key_name}.pem"
        
        with open(private_key_file, 'w') as key_file:
            key_file.write(private_key)
        
        os.chmod(private_key_file, 0o400)
        print(f"Private key saved to {private_key_file}")
        return key_name
    except Exception as e:
        print(f"Error creating key pair: {e}")
        sys.exit(1)

def launch_ec2_instance(security_group_id, key_name):
    try:
        response = ec2.run_instances(
            ImageId=ami_id,
            InstanceType="t2.micro",
            KeyName=key_name,
            SecurityGroupIds=[security_group_id],
            MinCount=1,
            MaxCount=1
        )
        instance_id = response['Instances'][0]['InstanceId']
        print(f"EC2 instance {instance_id} has been launched")
        return instance_id
    except Exception as e:
        print(f"Error launching EC2 instance: {e}")
        sys.exit(1)

def get_instance_info(instance_id):
    ec2.get_waiter('instance_running').wait(InstanceIds=[instance_id])
    response = ec2.describe_instances(InstanceIds=[instance_id])
    instance_info = response['Reservations'][0]['Instances'][0]
    return instance_info

def main():
    security_group_id = create_security_group()
    key_name = create_key_pair()
    instance_id = launch_ec2_instance(security_group_id, key_name)
    instance_info = get_instance_info(instance_id)
    
    print(f"Instance ID: {instance_id}")
    print(f"Public DNS: {instance_info.get('PublicDnsName', 'N/A')}")
    print(f"Public IP: {instance_info.get('PublicIpAddress', 'N/A')}")

if __name__ == "__main__":
    main()