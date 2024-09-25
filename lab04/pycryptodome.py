import os, random, struct
from Crypto.Cipher import AES
from Crypto import Random
import boto3
import base64
import hashlib

# Initialize the S3 client
s3 = boto3.client('s3', region_name='ap-southeast-1')

# Your S3 bucket name
BUCKET_NAME = '23905652-cloudstorage'

BLOCK_SIZE = 16
CHUNK_SIZE = 64 * 1024

def encrypt_file(password, in_filename, out_filename):

    key = hashlib.sha256(password.encode("utf-8")).digest()

    iv = Random.new().read(AES.block_size)
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    filesize = os.path.getsize(in_filename)

    with open(in_filename, 'rb') as infile:
        with open(out_filename, 'wb') as outfile:
            outfile.write(struct.pack('<Q', filesize))
            outfile.write(iv)

            while True:
                chunk = infile.read(CHUNK_SIZE)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += ' '.encode("utf-8") * (16 - len(chunk) % 16)

                outfile.write(encryptor.encrypt(chunk))

def decrypt_file(password, in_filename, out_filename):

    key = hashlib.sha256(password.encode("utf-8")).digest()

    with open(in_filename, 'rb') as infile:
        origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        iv = infile.read(16)
        decryptor = AES.new(key, AES.MODE_CBC, iv)

        with open(out_filename, 'wb') as outfile:
            while True:
                chunk = infile.read(CHUNK_SIZE)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))

            outfile.truncate(origsize)

def process_s3_files(password):
    # List all objects in the bucket
    response = s3.list_objects_v2(Bucket=BUCKET_NAME)

    for obj in response.get('Contents', []):
        file_key = obj['Key']
        if not file_key.endswith(('.enc', '.dec')):
            # Download the file
            local_file = os.path.basename(file_key)
            s3.download_file(BUCKET_NAME, file_key, local_file)

            # Encrypt the file
            encrypted_file = local_file + ".enc"
            encrypt_file(password, local_file, encrypted_file)
            s3.upload_file(encrypted_file, BUCKET_NAME, f"{file_key}.enc")
            print(f"File {file_key} encrypted successfully")

            # Decrypt the file
            decrypted_file = local_file + ".dec"
            decrypt_file(password, encrypted_file, decrypted_file)
            s3.upload_file(decrypted_file, BUCKET_NAME, f"{file_key}.dec")
            print(f"File {file_key} decrypted successfully")

            # Compare original and decrypted files
            with open(local_file, 'rb') as f1, open(decrypted_file, 'rb') as f2:
                if f1.read() == f2.read():
                    print(f"File {file_key} was successfully encrypted and decrypted!")
                else:
                    print(f"Error: {file_key} and its decrypted version do not match.")

            # # Clean up local files
            # os.remove(local_file)
            # os.remove(encrypted_file)
            # os.remove(decrypted_file)

if __name__ == "__main__":
    password = 'kitty and the kat'  # You can change this password or make it a user input
    process_s3_files(password)