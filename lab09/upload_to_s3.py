import boto3
from botocore.exceptions import ClientError
import os

# Initialize clients
s3_client = boto3.client('s3')

def create_bucket(bucket_name, region):
    try:
        location = {'LocationConstraint': region}
        s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)
        print(f"Bucket {bucket_name} created successfully")
    except ClientError as e:
        print(f"Error creating bucket: {e}")
        return False
    return True

def upload_file(file_name, bucket, object_name):
    try:
        s3_client.upload_file(file_name, bucket, object_name)
        print(f"File {file_name} uploaded successfully")
    except ClientError as e:
        print(f"Error uploading file: {e}")
        return False
    return True

# Main execution
if __name__ == "__main__":
    bucket_name = "23905652-lab9"  # Replace with your desired bucket name
    region = "ap-southeast-1"  # Replace with your AWS region

    # Create bucket
    if create_bucket(bucket_name, region):
        # Upload images
        image_folder = "img"
        images = ["urban.jpg", "beach.jpg", "faces.jpg", "text.jpg"]
        
        for image in images:
            file_path = os.path.join(image_folder, image)
            upload_file(file_path, bucket_name, image)