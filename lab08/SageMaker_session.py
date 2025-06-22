# Import necessary libraries
import sagemaker  # Amazon SageMaker library for machine learning tasks
import boto3  # AWS SDK for Python, used to interact with various AWS services

# Import data processing libraries
import numpy as np  # NumPy: For matrix operations and numerical processing
import pandas as pd  # Pandas: For handling and analyzing structured data

# Import time-related functions and OS module
from time import gmtime, strftime  # For working with timestamps
import os  # For interacting with the operating system

# Set up AWS service clients
smclient = boto3.Session().client("sagemaker")  # Create a SageMaker client
iam = boto3.client('iam')  # Create an IAM (Identity and Access Management) client

# Retrieve the ARN (Amazon Resource Name) for the SageMaker role
sagemaker_role = iam.get_role(RoleName='SageMakerRole')['Role']['Arn']

# Set up variables for AWS resources
region = 'ap-southeast-1'  # Specify the AWS region (Singapore in this case)
student_id = "23905652"  # Set the student ID
bucket = '23905652-lab8'  # Define the S3 bucket name
prefix = f"sagemaker/{student_id}-hpo-xgboost-dm"  # Define the S3 object prefix

# Create an S3 bucket
s3 = boto3.resource('s3')  # Create an S3 resource
s3.create_bucket(
    Bucket=bucket, 
    CreateBucketConfiguration={'LocationConstraint': region}
)  # Create the bucket in the specified region

# Create a folder (object) in the S3 bucket
s3.Object(bucket, prefix + '/').put(Body='')  # Create an empty object (folder) in the bucket

boto3.Session().resource("s3").Bucket(bucket).Object(
    os.path.join(prefix, "train/train.csv")
).upload_file("train.csv")
boto3.Session().resource("s3").Bucket(bucket).Object(
    os.path.join(prefix, "validation/validation.csv")
).upload_file("validation.csv")