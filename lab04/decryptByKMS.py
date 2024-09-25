import boto3
import os

# Initialize the S3 and KMS clients
s3 = boto3.client('s3')
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

def decrypt_file(file_key):
    # Download the encrypted file
    local_file = os.path.basename(file_key)
    s3.download_file(BUCKET_NAME, file_key, local_file)

    with open(local_file, 'rb') as file:
        encrypted_contents = file.read()

    # Decrypt the file
    response = kms.decrypt(CiphertextBlob=encrypted_contents, KeyId=key_id)
    decrypted_contents = response['Plaintext']

    # Write the decrypted file
    decrypted_file = local_file.replace('.encrypted', '.decrypted')
    with open(decrypted_file, 'wb') as file:
        file.write(decrypted_contents)

    # Upload the decrypted file back to S3
    s3.upload_file(decrypted_file, BUCKET_NAME, file_key.replace('.encrypted', '.decrypted'))

    print(f"File {file_key} decrypted successfully")

    # Clean up local files
    os.remove(local_file)
    os.remove(decrypted_file)

def compare_files(original_key, decrypted_key):
    original_file = 'original_' + os.path.basename(original_key)
    decrypted_file = 'decrypted_' + os.path.basename(decrypted_key)
    
    s3.download_file(BUCKET_NAME, original_key, original_file)
    s3.download_file(BUCKET_NAME, decrypted_key, decrypted_file)
    
    with open(original_file, 'rb') as f1, open(decrypted_file, 'rb') as f2:
        if f1.read() == f2.read():
            print(f"File {original_key} was successfully decrypted and matches the original!")
        else:
            print(f"Error: {original_key} and its decrypted version do not match.")
    
    # os.remove(original_file)
    # os.remove(decrypted_file)

def main():
    global key_id
    key_id = get_kms_key_id()

    # List all objects in the bucket
    response = s3.list_objects_v2(Bucket=BUCKET_NAME)

    for obj in response.get('Contents', []):
        file_key = obj['Key']
        if file_key.endswith('.encrypted'):
            decrypt_file(file_key)
            original_key = file_key.replace('.encrypted', '')
            decrypted_key = file_key.replace('.encrypted', '.decrypted')
            compare_files(original_key, decrypted_key)

if __name__ == "__main__":
    main()