import boto3
from botocore.exceptions import ClientError

def analyze_faces(bucket, image):
    rekognition_client = boto3.client('rekognition')
    try:
        response = rekognition_client.detect_faces(
            Image={'S3Object': {'Bucket': bucket, 'Name': image}},
            Attributes=['ALL']
        )
        print(f"\nFaces detected in {image}:")
        if not response['FaceDetails']:
            print("No faces detected.")
        for face in response['FaceDetails']:
            # print(face)
            print(f"- Age range: {face['AgeRange']['Low']}-{face['AgeRange']['High']}")
            print(f"  Gender: {face['Gender']['Value']} ({face['Gender']['Confidence']:.2f}%)")
            print(f"  Top emotion: {face['Emotions'][0]['Type']} ({face['Emotions'][0]['Confidence']:.2f}%)")
            print(f"  Smile: {'Yes' if face['Smile']['Value'] else 'No'} ({face['Smile']['Confidence']:.2f}%)")
            print(f"  Sunglasses: {'Yes' if face['Sunglasses']['Value'] else 'No'} ({face['Sunglasses']['Confidence']:.2f}%)")
            print(f"  Beard: {'Yes' if face['Beard']['Value'] else 'No'} ({face['Beard']['Confidence']:.2f}%)")
    except ClientError as e:
        print(f"Error analyzing faces: {e}")

if __name__ == "__main__":
    bucket_name = "23905652-lab9"
    images = ["urban.jpg", "beach.jpg", "faces.jpg", "text.jpg"]
    
    for image in images:
        analyze_faces(bucket_name, image)