import boto3
from botocore.exceptions import ClientError
import os

# Initialize the S3 client
s3_client = boto3.client('s3')

def create_bucket(bucket_name, region):
    """
    Create an S3 bucket in a specified region
    
    :param bucket_name: Name of the bucket to create
    :param region: String region to create bucket in, e.g., 'ap-southeast-1'
    :return: True if bucket created, else False
    """
    try:
        # Define the location constraint for the bucket
        location = {'LocationConstraint': region}
        
        # Create the bucket with the specified name and region
        s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)
        print(f"Bucket {bucket_name} created successfully")
    except ClientError as e:
        # Handle any errors that occur during bucket creation
        print(f"Error creating bucket: {e}")
        return False
    return True

def upload_file(file_name, bucket, object_name):
    """
    Upload a file to an S3 bucket
    
    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """
    try:
        # Upload the file to S3
        s3_client.upload_file(file_name, bucket, object_name)
        print(f"File {file_name} uploaded successfully")
    except ClientError as e:
        # Handle any errors that occur during file upload
        print(f"Error uploading file: {e}")
        return False
    return True

# Main execution
if __name__ == "__main__":
    # Set the bucket name and region
    bucket_name = "23905652-lab9"
    region = "ap-southeast-1"
    
    # Attempt to create the bucket
    if create_bucket(bucket_name, region):
        # If bucket creation is successful, proceed to upload images
        image_folder = "img"  # Folder containing the images
        images = ["urban.jpg", "beach.jpg", "faces.jpg", "text.jpg"]  # List of image files to upload
        
        # Iterate through each image and upload it to the bucket
        for image in images:
            # Construct the full file path
            file_path = os.path.join(image_folder, image)
            # Upload the file to S3
            upload_file(file_path, bucket_name, image)