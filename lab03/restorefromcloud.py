import os
import boto3

ROOT_DIR = '.'
ROOT_S3_DIR = '23905652-cloudstorage'
REGION = 'ap-southeast-1'

bucket_config = {'LocationConstraint': REGION}

s3 = boto3.client("s3", region_name=REGION)

def download_file(s3_key, local_path):
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    s3.download_file(ROOT_S3_DIR, s3_key, local_path)
    print(f"Downloaded: {s3_key}")

# List and download files from S3
response = s3.list_objects(Bucket=ROOT_S3_DIR)
for obj in response.get('Contents', []):
    s3_key = obj['Key']
    local_path = os.path.join(ROOT_DIR, s3_key)
    download_file(s3_key, local_path)

print("Download complete")