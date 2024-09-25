import boto3
import json

# Initialize the KMS client
kms_client = boto3.client('kms', region_name='ap-southeast-1')

# Your student number (to be used as the key alias)
STUDENT_NUMBER = '23905652_2'

# Your IAM username
IAM_USERNAME = '23905652@student.uwa.edu.au'  # Replace with your actual IAM username if different


def create_kms_key():
    # Create a new KMS key
    response = kms_client.create_key(
        Description=f'KMS key for student {STUDENT_NUMBER}',
        KeyUsage='ENCRYPT_DECRYPT',
        Origin='AWS_KMS'
    )
    
    key_id = response['KeyMetadata']['KeyId']
    
    # Create an alias for the key
    kms_client.create_alias(
        AliasName=f'alias/{STUDENT_NUMBER}',
        TargetKeyId=key_id
    )
    
    print(f"KMS key created with ID: {key_id}")
    return key_id

def attach_policy_to_key(key_id):
    # Define the policy
    policy = {
        "Version": "2012-10-17",
        "Id": "key-consolepolicy-3",
        "Statement": [
            {
                "Sid": "Enable IAM User Permissions",
                "Effect": "Allow",
                "Principal": {
                    "AWS": "arn:aws:iam::489389878001:root"
                },
                "Action": "kms:*",
                "Resource": "*"
            },
            {
                "Sid": "Allow access for Key Administrators",
                "Effect": "Allow",
                "Principal": {
                    "AWS": f"arn:aws:iam::489389878001:user/{IAM_USERNAME}"
                },
                "Action": [
                    "kms:Create*",
                    "kms:Describe*",
                    "kms:Enable*",
                    "kms:List*",
                    "kms:Put*",
                    "kms:Update*",
                    "kms:Revoke*",
                    "kms:Disable*",
                    "kms:Get*",
                    "kms:Delete*",
                    "kms:TagResource",
                    "kms:UntagResource",
                    "kms:ScheduleKeyDeletion",
                    "kms:CancelKeyDeletion"
                ],
                "Resource": "*"
            },
            {
                "Sid": "Allow use of the key",
                "Effect": "Allow",
                "Principal": {
                    "AWS": f"arn:aws:iam::489389878001:user/{IAM_USERNAME}"
                },
                "Action": [
                    "kms:Encrypt",
                    "kms:Decrypt",
                    "kms:ReEncrypt*",
                    "kms:GenerateDataKey*",
                    "kms:DescribeKey"
                ],
                "Resource": "*"
            },
            {
                "Sid": "Allow attachment of persistent resources",
                "Effect": "Allow",
                "Principal": {
                    "AWS": f"arn:aws:iam::489389878001:user/{IAM_USERNAME}"
                },
                "Action": [
                    "kms:CreateGrant",
                    "kms:ListGrants",
                    "kms:RevokeGrant"
                ],
                "Resource": "*",
                "Condition": {
                    "Bool": {
                        "kms:GrantIsForAWSResource": "true"
                    }
                }
            }
        ]
    }

    # Attach the policy to the key
    kms_client.put_key_policy(
        KeyId=key_id,
        PolicyName='default',
        Policy=json.dumps(policy)
    )
    
    print(f"Policy attached to key {key_id}")

def main():
    key_id = create_kms_key()
    attach_policy_to_key(key_id)
    print("KMS key creation and policy attachment completed successfully.")

if __name__ == "__main__":
    main()

