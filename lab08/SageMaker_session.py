import sagemaker
import boto3

import numpy as np  # For matrix operations and numerical processing
import pandas as pd  # For munging tabular data
from time import gmtime, strftime
import os

smclient = boto3.Session().client("sagemaker")
iam = boto3.client('iam')
sagemaker_role = iam.get_role(RoleName='SageMakerRole')['Role']['Arn']
region = 'ap-southeast-1' # use the region you are mapped to 
student_id = "23905652" # use your student id 
bucket = '23905652-lab8' # use <studentid-lab8> as your bucket name
prefix = f"sagemaker/{student_id}-hpo-xgboost-dm" 
# Create an S3 bucket using the bucket variable above. The bucket creation is done using the region variable above.
# Create an object into the bucket. The object is a folder and its name is the prefix variable above. 

# create the bucket
s3 = boto3.resource('s3')
# s3.create_bucket(Bucket=bucket, CreateBucketConfiguration={'LocationConstraint': region})

# create the folder
# s3.Object(bucket, prefix + '/').put(Body='')

boto3.Session().resource("s3").Bucket(bucket).Object(
    os.path.join(prefix, "train/train.csv")
).upload_file("train.csv")
boto3.Session().resource("s3").Bucket(bucket).Object(
    os.path.join(prefix, "validation/validation.csv")
).upload_file("validation.csv")