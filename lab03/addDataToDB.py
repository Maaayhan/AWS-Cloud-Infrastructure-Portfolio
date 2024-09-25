import boto3
from botocore.exceptions import ClientError

# Constants
S3_BUCKET_NAME = '23905652-cloudstorage'
DYNAMODB_TABLE_NAME = 'CloudFiles'
REGION = 'ap-southeast-1'

# Initialize clients
s3 = boto3.client('s3', region_name=REGION)
dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000', region_name=REGION)

def get_file_attributes(bucket, key):
    try:
        response = s3.head_object(Bucket=bucket, Key=key)
        return {
            'fileName': key,
            'path': f"s3://{bucket}/{key}",
            'lastUpdated': response['LastModified'].isoformat()
        }
    except ClientError as e:
        print(f"Error getting attributes for {key}: {e}")
        return None

def write_to_dynamodb(table, user_id, owner, file_info):
    try:
        item = {
            'userId': user_id,
            'owner': owner,
            'permissions': s3.get_bucket_acl(Bucket=S3_BUCKET_NAME)['Grants'][0]['Permission'],
            **file_info
        }
        table.put_item(Item=item)
        print(f"Added to DynamoDB: {file_info['fileName']}")
    except ClientError as e:
        print(f"Error writing to DynamoDB: {e}")

def main():
    table = dynamodb.Table(DYNAMODB_TABLE_NAME)

    try:
        response = s3.list_objects(Bucket=S3_BUCKET_NAME)
        user_id = str(response['Contents'][0]['Owner']['ID'])
        owner = response['Contents'][0]['Owner']['DisplayName']
        for obj in response.get('Contents', []):
            file_attributes = get_file_attributes(S3_BUCKET_NAME, obj['Key'])
            if file_attributes:
                write_to_dynamodb(table, user_id, owner, file_attributes)

        print("Process completed. All files have been processed.")

    except ClientError as e:
        print(f"Error listing S3 objects: {e}")

if __name__ == "__main__":
    main()