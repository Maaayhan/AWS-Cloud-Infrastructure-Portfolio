import boto3
import os
# import shutil

student_number = "23905652"
region = "ap-southeast-1"

# Initialize the EC2 client
ec2 = boto3.client('ec2', region)

# Create a security group
response = ec2.create_security_group(
    GroupName=f"{student_number}-sg",
    Description="security group for development environment"
)
security_group_id = response['GroupId']

# Authorize inbound SSH traffic for the security group
ec2.authorize_security_group_ingress(
    GroupId=security_group_id,
    IpProtocol="tcp",
    FromPort=22,
    ToPort=22,
    CidrIp="0.0.0.0/0"
)

# Create a key pair and save the private key to a file
response = ec2.create_key_pair(KeyName=f"{student_number}-key")
private_key = response['KeyMaterial']

private_key_file = f"{student_number}-key.pem"

# Allow writing to the private key file
# os.chmod(private_key_file, 0o666)
with open(private_key_file, 'w') as key_file:
    key_file.write(private_key)
    
# Print message to confirm key file creation
print(f"Private key saved to {private_key_file}")

# Set the correct permissions for the private key file
os.chmod(private_key_file, 0o400)

# # Copy the private key file to ~/.ssh directory
# ssh_directory = os.path.expanduser("~/.ssh")
# if not os.path.exists(ssh_directory):
#     os.makedirs(ssh_directory)
# shutil.copy(private_key_file, ssh_directory)

print(f"Private key copied to {ssh_directory}")

# Launch an EC2 instance
response = ec2.run_instances(
    ImageId="ami-0497a974f8d5dcef8",
    SecurityGroupIds=[security_group_id],
    MinCount=1,
    MaxCount=1,
    InstanceType="t2.micro",
    KeyName=f"{student_number}-key"
)

print("Instance created successfully")

instance_id = response['Instances'][0]['InstanceId']

# Wait for the instance to be up and running
ec2.get_waiter('instance_running').wait(InstanceIds=[instance_id])

# Describe the instance to get its public IP address
response = ec2.describe_instances(InstanceIds=[instance_id])
public_ip_address = response['Reservations'][0]['Instances'][0]['PublicIpAddress']
print(f"Instance created successfully with Public IP: {public_ip_address}")
