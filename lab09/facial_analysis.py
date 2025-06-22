import boto3
from botocore.exceptions import ClientError

# Define a function to analyze faces in an image using Amazon Rekognition
def analyze_faces(bucket, image):
    # Create a Rekognition client using boto3
    rekognition_client = boto3.client('rekognition')
    try:
        # Call the detect_faces method of the Rekognition client
        # This method analyzes the image for facial features and attributes
        response = rekognition_client.detect_faces(
            # Specify the S3 bucket and image name
            Image={'S3Object': {'Bucket': bucket, 'Name': image}},
            # Request all available attributes for each detected face
            Attributes=['ALL']
        )
        # Print a header for the face detection results
        print(f"\nFaces detected in {image}:")
        # Check if any faces were detected
        if not response['FaceDetails']:
            print("No faces detected.")
        # Iterate through detected faces and print their attributes
        for face in response['FaceDetails']:
            # Print age range of the detected face
            print(f"- Age range: {face['AgeRange']['Low']}-{face['AgeRange']['High']}")
            # Print gender of the detected face with confidence score
            print(f"  Gender: {face['Gender']['Value']} ({face['Gender']['Confidence']:.2f}%)")
            # Print the top emotion detected for the face with confidence score
            print(f"  Top emotion: {face['Emotions'][0]['Type']} ({face['Emotions'][0]['Confidence']:.2f}%)")
            # Print whether the face is smiling with confidence score
            print(f"  Smile: {'Yes' if face['Smile']['Value'] else 'No'} ({face['Smile']['Confidence']:.2f}%)")
            # Print whether the face is wearing sunglasses with confidence score
            print(f"  Sunglasses: {'Yes' if face['Sunglasses']['Value'] else 'No'} ({face['Sunglasses']['Confidence']:.2f}%)")
            # Print whether the face has a beard with confidence score
            print(f"  Beard: {'Yes' if face['Beard']['Value'] else 'No'} ({face['Beard']['Confidence']:.2f}%)")
    # Handle any AWS-specific errors that might occur
    except ClientError as e:
        print(f"Error analyzing faces: {e}")

# Check if this script is being run as the main program
if __name__ == "__main__":
    # Set the S3 bucket name
    bucket_name = "23905652-lab9"
    # List of image files to be analyzed
    images = ["urban.jpg", "beach.jpg", "faces.jpg", "text.jpg"]
    
    # Iterate through the list of images and analyze faces in each one
    for image in images:
        analyze_faces(bucket_name, image)