import boto3
import os

# Student identifier used for naming resources
student_number = "23905652"
# AWS region where resources will be created
region = "ap-southeast-1"

# Initialize the EC2 client
# This creates a boto3 client for interacting with EC2 services in the specified region
ec2 = boto3.client('ec2', region_name=region)

def create_security_group():
    # Create a new security group with a name based on the student number
    response = ec2.create_security_group(
        GroupName=f"{student_number}-sg",
        Description="Security group for Web Application"
    )
    security_group_id = response['GroupId']

    # Configure inbound rules to allow HTTP (port 80) and SSH (port 22) traffic from anywhere
    # This is necessary to access the web server and to SSH into the instances
    ec2.authorize_security_group_ingress(
        GroupId=security_group_id,
        IpPermissions=[
        {
            'IpProtocol': 'tcp',
            'FromPort': 80,
            'ToPort': 80,
            'IpRanges': [{'CidrIp': '0.0.0.0/0'}] # Allow HTTP traffic from any IP
        },
        {
            'IpProtocol': 'tcp',
            'FromPort': 22,
            'ToPort': 22,
            'IpRanges': [{'CidrIp': '0.0.0.0/0'}] # Allow SSH traffic from any IP
        }
    ]
    )
    print(f"Created Security Group: {security_group_id}")
    return security_group_id

def create_key_pair():
    # Generate a new key pair for SSH access to the EC2 instances
    key_name = f"{student_number}-key"
    response = ec2.create_key_pair(KeyName=key_name)
    private_key = response['KeyMaterial']

    # Save the private key to a file with the key name
    private_key_file = f"{key_name}.pem"

    # Allow writing to the private key file
    with open(private_key_file, 'w') as key_file:
        key_file.write(private_key)
    
    # Set the correct permissions for the private key file (read-only by owner)
    # This is important for security reasons and is required by SSH
    os.chmod(private_key_file, 0o400)

    print(f"Private key saved to {private_key_file}")
    return key_name

def get_availability_zones():
    # Retrieve the first two availability zones in the specified region
    # This is used to distribute instances across multiple AZs for high availability
    response = ec2.describe_availability_zones(
        Filters=[
            {
                'Name': 'region-name',
                'Values': [region]
            },
        ]
    )
    return [az['ZoneName'] for az in response['AvailabilityZones'][:2]]

def create_ec2_instance(security_group_id, key_name, availability_zone, instance_number):
    # Launch a new EC2 instance with specified parameters
    response = ec2.run_instances(
        ImageId="ami-0497a974f8d5dcef8", # Amazon Linux 2 AMI ID for ap-southeast-1
        InstanceType="t2.micro", # Free tier instance type
        KeyName=key_name, # Key pair for SSH access
        MaxCount=1, # Launch a single instance
        MinCount=1, # Launch a single instance
        SecurityGroupIds=[security_group_id], # Attach the created security group
        Placement={
            'AvailabilityZone': availability_zone # Specify the AZ for the instance
        },
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [
                    {'Key': 'Name', 'Value': f'{student_number}-vm{instance_number}'} # Tag the instance with a name
                ]
            }
        ]
    )
    instance_id = response['Instances'][0]['InstanceId']
    print(f"Created EC2 instance: {instance_id} in {availability_zone}")
    return instance_id

def main():
    # Create security group
    security_group_id = create_security_group()

    # Create key pair
    key_name = create_key_pair()

    # Get availability zones
    availability_zones = get_availability_zones()

    # Wait for all instances to reach the 'running' state
    # This ensures that the instances are fully initialized before we try to access them
    instance_ids = []
    for i, az in enumerate(availability_zones, start=1):
        instance_id = create_ec2_instance(security_group_id, key_name, az, i)
        instance_ids.append(instance_id)

    # Wait for all instances to reach the 'running' state
    print("Waiting for instances to enter 'running' state...")
    waiter = ec2.get_waiter('instance_running')
    waiter.wait(InstanceIds=instance_ids)
    print("Instances are now running.")

    # Retrieve and display public IP addresses of the created instances
    # This information is useful for connecting to the instances via SSH or HTTP
    for i, instance_id in enumerate(instance_ids, start=1):
        response = ec2.describe_instances(InstanceIds=[instance_id])
        instance = response['Reservations'][0]['Instances'][0]
        public_ip = instance.get('PublicIpAddress', 'N/A')
        az = instance['Placement']['AvailabilityZone']
        print(f"Instance {i} (ID: {instance_id}) created in {az} with Public IP: {public_ip}")

if __name__ == "__main__":
    main()