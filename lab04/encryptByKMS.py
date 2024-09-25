import boto3
import os

# Initialize the S3 and KMS clients
s3 = boto3.client("s3")
kms = boto3.client('kms')

# Your S3 bucket name and KMS key alias
BUCKET_NAME = '23905652-cloudstorage'
KEY_ALIAS = 'alias/23905652_2'

def get_kms_key_id():
    response = kms.list_aliases()
    for alias in response['Aliases']:
        if alias['AliasName'] == KEY_ALIAS:
            return alias['TargetKeyId']
    raise Exception(f"KMS key with alias {KEY_ALIAS} not found")

def encrypt_file(file_key):
    # Download the file
    local_file = os.path.basename(file_key)
    s3.download_file(BUCKET_NAME, file_key, local_file)

    with open(local_file, 'rb') as file:
        file_contents = file.read()

    # Encrypt the file
    response = kms.encrypt(KeyId=key_id, Plaintext=file_contents)
    encrypted_contents = response['CiphertextBlob']

    # Write the encrypted file
    encrypted_file = f"{local_file}.encrypted"
    with open(encrypted_file, 'wb') as file:
        file.write(encrypted_contents)

    # Upload the processed file back to S3
    s3.upload_file(encrypted_file, BUCKET_NAME, f"{file_key}.encrypted")

    print(f"File {file_key} encrypted successfully")
    
    # # Clean up local files
    # os.remove(local_file)
    # os.remove(encrypted_file)

def main():
    global key_id
    key_id = get_kms_key_id()

    # List all objects in the bucket
    response = s3.list_objects_v2(Bucket=BUCKET_NAME)

    for obj in response.get('Contents', []):
        file_key = obj['Key']
        if not file_key.endswith('.encrypted'):
            encrypt_file(file_key)

if __name__ == "__main__":
    main()