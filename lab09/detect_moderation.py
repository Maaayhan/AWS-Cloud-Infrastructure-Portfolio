import boto3
from botocore.exceptions import ClientError

def moderate_image(bucket, image):
    rekognition_client = boto3.client('rekognition')
    try:
        response = rekognition_client.detect_moderation_labels(
            Image={'S3Object': {'Bucket': bucket, 'Name': image}},
            MinConfidence=75
        )
        print(f"\nModeration labels for {image}:")
        if not response['ModerationLabels']:
            print("No moderation labels detected.")
        for label in response['ModerationLabels']:
            print(f"- {label['Name']}: {label['Confidence']:.2f}%")
    except ClientError as e:
        print(f"Error moderating image: {e}")

if __name__ == "__main__":
    bucket_name = "23905652-lab9"
    images = ["urban.jpg", "beach.jpg", "faces.jpg", "text.jpg"]
    
    for image in images:
        moderate_image(bucket_name, image)