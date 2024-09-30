import boto3

def detect_language(text):
    client = boto3.client('comprehend')

    response = client.detect_dominant_language(Text=text)
    language = response['Languages'][0]
    language_code = language['LanguageCode']
    confidence = language['Score'] * 100  # Convert to percentage
    
    # Map language codes to full names
    language_map = {
        'en': 'English', 'es': 'Spanish', 'fr': 'French', 'it': 'Italian'
        # Add more languages as needed
    }
    
    language_name = language_map.get(language_code, language_code)
    
    print(f"{language_name} detected with {confidence:.0f}% confidence")

# Test texts
texts = [
    "The French Revolution was a period of social and political upheaval in France and its colonies beginning in 1789 and ending in 1799.",
    "El Quijote es la obra más conocida de Miguel de Cervantes Saavedra. Publicada su primera parte con el título de El ingenioso hidalgo don Quijote de la Mancha a comienzos de 1605, es una de las obras más destacadas de la literatura española y la literatura universal, y una de las más traducidas. En 1615 aparecería la segunda parte del Quijote de Cervantes con el título de El ingenioso caballero don Quijote de la Mancha.",
    "Moi je n'étais rien Et voilà qu'aujourd'hui Je suis le gardien Du sommeil de ses nuits Je l'aime à mourir Vous pouvez détruire Tout ce qu'il vous plaira Elle n'a qu'à ouvrir L'espace de ses bras Pour tout reconstruire Pour tout reconstruire Je l'aime à mourir",
    "L'amor che move il sole e l'altre stelle."
]

# Test the function with each text
for text in texts:
    detect_language(text)