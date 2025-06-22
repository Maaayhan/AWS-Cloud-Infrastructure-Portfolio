import boto3

# Create an EC2 client
ec2 = boto3.client('ec2')

# Get the region descriptions
response = ec2.describe_regions()

# Extract the needed data
regions = response['Regions']

# Print the header
print(f"{'Endpoint':<40} {'RegionName'}")
print("="*50)

# Print each region's Endpoint and RegionName
for region in regions:
    endpoint = region['Endpoint']
    region_name = region['RegionName']
    print(f"{endpoint:<40} {region_name}")
