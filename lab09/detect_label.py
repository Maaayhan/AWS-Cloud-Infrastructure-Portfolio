import boto3
from botocore.exceptions import ClientError

def detect_labels(bucket, image):
    """
    Detect labels in an image stored in an S3 bucket using AWS Rekognition.
    
    :param bucket: Name of the S3 bucket containing the image
    :param image: Name of the image file in the S3 bucket
    """
    # Initialize the AWS Rekognition client
    rekognition_client = boto3.client('rekognition')
    
    try:
        # Call the detect_labels API of AWS Rekognition
        response = rekognition_client.detect_labels(
            Image={'S3Object': {'Bucket': bucket, 'Name': image}},  # Specify the S3 object
            MaxLabels=10,  # Limit the number of labels to return
            MinConfidence=85  # Set the minimum confidence threshold for labels
        )
        
        # Print the detected labels
        print(f"\nLabels detected for {image}:")
        for label in response['Labels']:
            print(f"- {label['Name']}: {label['Confidence']:.2f}%")
    
    except ClientError as e:
        # Handle any errors that occur during the API call
        print(f"Error detecting labels: {e}")

if __name__ == "__main__":
    # Set the S3 bucket name
    bucket_name = "23905652-lab9"
    
    # List of images to analyze
    images = ["urban.jpg", "beach.jpg", "faces.jpg", "text.jpg"]
    
    # Iterate through each image and detect labels
    for image in images:
        detect_labels(bucket_name, image)