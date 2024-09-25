import boto3
import os

student_number = "23905652"
region = "ap-southeast-1"

# Initialize the EC2 client
ec2 = boto3.client('ec2', region_name=region)

def create_security_group():
    response = ec2.create_security_group(
        GroupName=f"{student_number}-sg",
        Description="Security group for ALB lab"
    )
    security_group_id = response['GroupId']

    # Authorize inbound SSH and HTTP traffic
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
    return security_group_id

def create_key_pair():
    key_name = f"{student_number}-key"
    response = ec2.create_key_pair(KeyName=key_name)
    private_key = response['KeyMaterial']

    private_key_file = f"{key_name}.pem"

    # Allow writing to the private key file
    with open(private_key_file, 'w') as key_file:
        key_file.write(private_key)
    
    # Set the correct permissions for the private key file
    os.chmod(private_key_file, 0o400)

    # # Copy the private key file to ~/.ssh directory
    # ssh_directory = os.path.expanduser("~/.ssh")
    # if not os.path.exists(ssh_directory):
    #     os.makedirs(ssh_directory)
    # shutil.copy(private_key_file, ssh_directory)

    print(f"Private key saved to {private_key_file}")
    return key_name

def get_availability_zones():
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
    response = ec2.run_instances(
        ImageId="ami-0497a974f8d5dcef8",
        InstanceType="t2.micro",
        KeyName=key_name,
        MaxCount=1,
        MinCount=1,
        SecurityGroupIds=[security_group_id],
        Placement={
            'AvailabilityZone': availability_zone
        },
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [
                    {'Key': 'Name', 'Value': f'{student_number}-vm{instance_number}'}
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

    # Create EC2 instances
    instance_ids = []
    for i, az in enumerate(availability_zones, start=1):
        instance_id = create_ec2_instance(security_group_id, key_name, az, i)
        instance_ids.append(instance_id)

    # Wait for instances to be running
    print("Waiting for instances to enter 'running' state...")
    waiter = ec2.get_waiter('instance_running')
    waiter.wait(InstanceIds=instance_ids)
    print("Instances are now running.")

    # Describe instances to get public IP addresses
    for i, instance_id in enumerate(instance_ids, start=1):
        response = ec2.describe_instances(InstanceIds=[instance_id])
        instance = response['Reservations'][0]['Instances'][0]
        public_ip = instance.get('PublicIpAddress', 'N/A')
        az = instance['Placement']['AvailabilityZone']
        print(f"Instance {i} (ID: {instance_id}) created in {az} with Public IP: {public_ip}")

if __name__ == "__main__":
    main()