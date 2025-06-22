import boto3
from botocore.exceptions import ClientError


def analyze_sentiment(text):
    # Create a boto3 client for AWS Comprehend service
    client = boto3.client('comprehend')
    
    # First, detect the dominant language of the text
    response = client.detect_dominant_language(Text=text)
    language_code = response['Languages'][0]['LanguageCode']
    
    # Now, analyze sentiment with the detected language
    response = client.detect_sentiment(Text=text, LanguageCode=language_code)
    
    # Extract sentiment and confidence score
    sentiment = response['Sentiment']
    confidence = response['SentimentScore'][sentiment.capitalize()] * 100  # Convert to percentage
    
    # Print the sentiment analysis result
    print(f"The sentiment of the text is {sentiment} with {confidence:.0f}% confidence")

# List of test texts in different languages
texts = [
    "The French Revolution was a period of social and political upheaval in France and its colonies beginning in 1789 and ending in 1799.",
    "El Quijote es la obra más conocida de Miguel de Cervantes Saavedra. Publicada su primera parte con el título de El ingenioso hidalgo don Quijote de la Mancha a comienzos de 1605, es una de las obras más destacadas de la literatura española y la literatura universal, y una de las más traducidas.",
    "Moi je n'étais rien Et voilà qu'aujourd'hui Je suis le gardien Du sommeil de ses nuits Je l'aime à mourir Vous pouvez détruire Tout ce qu'il vous plaira Elle n'a qu'à ouvrir L'espace de ses bras Pour tout reconstruire Pour tout reconstruire Je l'aime à mourir",
    "L'amor che move il sole e l'altre stelle."
]

# Test the function with each text in the list
for text in texts:
    print("\nText:", text)
    analyze_sentiment(text)