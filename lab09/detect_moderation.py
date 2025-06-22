import boto3
from botocore.exceptions import ClientError

# Define a function to moderate an image using Amazon Rekognition
def moderate_image(bucket, image):
    # Create a Rekognition client using boto3
    rekognition_client = boto3.client('rekognition')
    try:
        # Call the detect_moderation_labels method of the Rekognition client
        # This method analyzes the image for inappropriate or offensive content
        response = rekognition_client.detect_moderation_labels(
            # Specify the S3 bucket and image name
            Image={'S3Object': {'Bucket': bucket, 'Name': image}},
            # Set the minimum confidence threshold for detected labels (75%)
            MinConfidence=75
        )
        # Print a header for the moderation results
        print(f"\nModeration labels for {image}:")
        # Check if any moderation labels were detected
        if not response['ModerationLabels']:
            print("No moderation labels detected.")
        # Iterate through detected moderation labels and print them
        for label in response['ModerationLabels']:
            print(f"- {label['Name']}: {label['Confidence']:.2f}%")
    # Handle any AWS-specific errors that might occur
    except ClientError as e:
        print(f"Error moderating image: {e}")

# Check if this script is being run as the main program
if __name__ == "__main__":
    # Set the S3 bucket name
    bucket_name = "23905652-lab9"
    # List of image files to be moderated
    images = ["urban.jpg", "beach.jpg", "faces.jpg", "text.jpg"]
    
    # Iterate through the list of images and moderate each one
    for image in images:
        moderate_image(bucket_name, image)