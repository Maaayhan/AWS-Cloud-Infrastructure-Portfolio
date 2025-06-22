import boto3
from botocore.exceptions import ClientError

# Define a function to extract text from an image using Amazon Rekognition
def extract_text(bucket, image):
    # Create a Rekognition client using boto3
    rekognition_client = boto3.client('rekognition')
    try:
        # Call the detect_text method of the Rekognition client
        # This method analyzes the image for text content
        response = rekognition_client.detect_text(
            # Specify the S3 bucket and image name
            Image={'S3Object': {'Bucket': bucket, 'Name': image}}
        )
        # Print a header for the text detection results
        print(f"\nText detected in {image}:")
        # Check if any text was detected
        if not response['TextDetections']:
            print("No text detected.")
        # Iterate through detected text elements
        for text in response['TextDetections']:
            # Only print text elements of type 'LINE' (full lines of text)
            if text['Type'] == 'LINE':
                # Print the detected text and its confidence score
                print(f"- {text['DetectedText']}, with confidence {text['Confidence']:.2f}%")
    # Handle any AWS-specific errors that might occur
    except ClientError as e:
        print(f"Error extracting text: {e}")

# Check if this script is being run as the main program
if __name__ == "__main__":
    # Set the S3 bucket name
    bucket_name = "23905652-lab9"
    # List of image files to be analyzed
    images = ["urban.jpg", "beach.jpg", "faces.jpg", "text.jpg"]
    
    # Iterate through the list of images and extract text from each one
    for image in images:
        extract_text(bucket_name, image)