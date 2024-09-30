import boto3
from botocore.exceptions import ClientError

def extract_text(bucket, image):
    rekognition_client = boto3.client('rekognition')
    try:
        response = rekognition_client.detect_text(
            Image={'S3Object': {'Bucket': bucket, 'Name': image}}
        )
        print(f"\nText detected in {image}:")
        if not response['TextDetections']:
            print("No text detected.")
        for text in response['TextDetections']:
            if text['Type'] == 'LINE':
                print(f"- {text['DetectedText']}, with confidence {text['Confidence']:.2f}%")
    except ClientError as e:
        print(f"Error extracting text: {e}")

if __name__ == "__main__":
    bucket_name = "23905652-lab9"
    images = ["urban.jpg", "beach.jpg", "faces.jpg", "text.jpg"]
    
    for image in images:
        extract_text(bucket_name, image)