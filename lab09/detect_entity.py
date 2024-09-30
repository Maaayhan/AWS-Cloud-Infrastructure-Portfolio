import boto3

def detect_entities(text):
    client = boto3.client('comprehend')
    # First, detect the language
    response = client.detect_dominant_language(Text=text)
    language_code = response['Languages'][0]['LanguageCode']
    
    response = client.detect_entities(Text=text, LanguageCode=language_code)
    entities = response['Entities']
    print("Detected entities:")
    if not entities:
        print("No entities detected")
        return
    for entity in entities:
        confidence = entity['Score'] * 100  # Convert to percentage
        print(f"Entity: {entity['Text']}, Type: {entity['Type']}, with {confidence:.0f}% confidence")

# Test texts (reuse the texts from the previous parts)
texts = [
    "The French Revolution was a period of social and political upheaval in France and its colonies beginning in 1789 and ending in 1799.",
    "El Quijote es la obra más conocida de Miguel de Cervantes Saavedra. Publicada su primera parte con el título de El ingenioso hidalgo don Quijote de la Mancha a comienzos de 1605, es una de las obras más destacadas de la literatura española y la literatura universal, y una de las más traducidas. En 1615 aparecería la segunda parte del Quijote de Cervantes con el título de El ingenioso caballero don Quijote de la Mancha.",
    "Moi je n'étais rien Et voilà qu'aujourd'hui Je suis le gardien Du sommeil de ses nuits Je l'aime à mourir Vous pouvez détruire Tout ce qu'il vous plaira Elle n'a qu'à ouvrir L'espace de ses bras Pour tout reconstruire Pour tout reconstruire Je l'aime à mourir",
    "L'amor che move il sole e l'altre stelle."
]

# Test the function with each text
for text in texts:
    print("\nText:", text)
    detect_entities(text)
    print("\n")