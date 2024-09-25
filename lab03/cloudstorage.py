import os
import boto3
import base64

# ------------------------------
# CITS5503
#
# cloudstorage.py
#
# skeleton application to copy local files to S3
#
# Given a root local directory, will return files in each level and
# copy to same path on S3
#
# ------------------------------ 


ROOT_DIR = '.'
ROOT_S3_DIR = '23905652-cloudstorage'


s3 = boto3.client("s3")

bucket_config = {'LocationConstraint': 'ap-southeast-1'} #Replace the region with your allocated region name.

def upload_file(folder_name, file, file_name):
    print(f"Uploading {file}")
    s3_key = os.path.join(folder_name, file_name)
    s3.upload_file(file, ROOT_S3_DIR, s3_key)


# Main program
# Insert code to create bucket if not there

try:
    s3.create_bucket(Bucket=ROOT_S3_DIR, CreateBucketConfiguration=bucket_config)
    print(f"Bucket {ROOT_S3_DIR} created successfully")
except Exception as error:
     print(f"Error creating bucket or bucket already exists: {error}")


# parse directory and upload files

for dir_name, subdir_list, file_list in os.walk(ROOT_DIR, topdown=True):
    if dir_name != ROOT_DIR:
        relative_dir = os.path.relpath(dir_name, ROOT_DIR)
        for fname in file_list:
            file_path = os.path.join(dir_name, fname)
            upload_file(relative_dir, file_path, fname)


print("done")
