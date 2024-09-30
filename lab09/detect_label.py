import boto3
from botocore.exceptions import ClientError

def detect_labels(bucket, image):
    rekognition_client = boto3.client('rekognition')
    try:
        response = rekognition_client.detect_labels(
            Image={'S3Object': {'Bucket': bucket, 'Name': image}},
            MaxLabels=10,
            MinConfidence=85
        )
        print(f"\nLabels detected for {image}:")
        for label in response['Labels']:
            print(f"- {label['Name']}: {label['Confidence']:.2f}%")
    except ClientError as e:
        print(f"Error detecting labels: {e}")

if __name__ == "__main__":
    bucket_name = "23905652-lab9"
    images = ["urban.jpg", "beach.jpg", "faces.jpg", "text.jpg"]
    
    for image in images:
        detect_labels(bucket_name, image)