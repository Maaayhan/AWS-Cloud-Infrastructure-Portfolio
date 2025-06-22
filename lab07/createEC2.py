import boto3
import os

# Student number used for naming resources
student_number = "23905652"
# Specify the AWS region
region = "ap-southeast-1"

# Initialize the EC2 client
# This will use the default credential configuration (e.g., from ~/.aws/credentials file)
ec2 = boto3.client('ec2', region)

# Create a security group
# Security groups act like a firewall for your EC2 instances
response = ec2.create_security_group(
    GroupName=f"{student_number}-sg",
    Description="security group for development environment"
)
security_group_id = response['GroupId']

# Authorize inbound traffic for the security group
# This allows HTTP (port 80) and SSH (port 22) traffic from any IP (0.0.0.0/0)
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
print(f"Created Security Group: {security_group_id}")

# Create a key pair
# Key pairs are used for SSH access to EC2 instances
response = ec2.create_key_pair(KeyName=f"{student_number}-key")
private_key = response['KeyMaterial']

# Save the private key to a file
private_key_file = f"{student_number}-key.pem"
with open(private_key_file, 'w') as key_file:
    key_file.write(private_key)

# Set the correct permissions for the private key file
# 0o400 means read permission only for the file owner
os.chmod(private_key_file, 0o400)

# Launch an EC2 instance
# ImageId specifies the AMI (Amazon Machine Image) to use
# SecurityGroupIds specifies which security group to use
# InstanceType specifies the type of instance, t2.micro is available in the free tier
# KeyName specifies which key pair to use
# TagSpecifications adds a Name tag to the instance
response = ec2.run_instances(
    ImageId="ami-0497a974f8d5dcef8",
    SecurityGroupIds=[security_group_id],
    MinCount=1,
    MaxCount=1,
    InstanceType="t2.micro",
    KeyName=f"{student_number}-key",
    TagSpecifications=[
        {
            'ResourceType': 'instance',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': f"{student_number}-vm"
                }
            ]
        }
    ]
)

print("Instance created successfully")

# Get the ID of the newly created instance
instance_id = response['Instances'][0]['InstanceId']

# Wait for the instance to enter the 'running' state
# This is a synchronous operation and will block until the instance is running
ec2.get_waiter('instance_running').wait(InstanceIds=[instance_id])

# Get the public IP address of the instance
response = ec2.describe_instances(InstanceIds=[instance_id])
public_ip_address = response['Reservations'][0]['Instances'][0]['PublicIpAddress']
print(f"Instance created successfully with Public IP: {public_ip_address}")