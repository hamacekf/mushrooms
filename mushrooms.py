import requests
from PIL import Image
from io import BytesIO

import numpy as np
import matplotlib.pyplot as plt

import cv2
import numpy as np

from email.mime.text import MIMEText
import smtplib
import sys

from datetime import date


def send_email(username, password, recipients, subject, body):
    # Vytvoření HTML zprávy
    message = MIMEText(body, 'html')
    message['Subject'] = subject
    message['From'] = username
    message['To'] = ', '.join(recipients)

    with smtplib.SMTP_SSL('smtp.seznam.cz', 465) as smtp:
        print('Přihlašuji se...')
        try:
            smtp.login(username, password)
        except Exception as e:
            print('Přihlášení se nepovedlo.', e)
            sys.exit()
    
        print('Odesílám email...')
        try:
            for recipient in recipients:
                smtp.sendmail(username, recipient, message.as_string())
                print(f'Email poslán na {recipient}')
        except Exception as e:
            print('Odeslání se nepovedlo.', e)
            sys.exit()

def visualize_color_ranges(color_ranges):
    fig, ax = plt.subplots(2, len(color_ranges), figsize=(15, 5))
    for i, (label, (lower, upper)) in enumerate(color_ranges.items()):
        lower = np.array(lower, dtype="uint8").reshape(1, 1, 3)
        upper = np.array(upper, dtype="uint8").reshape(1, 1, 3)
        
        lower_patch = np.ones((100, 100, 3), dtype="uint8") * lower
        upper_patch = np.ones((100, 100, 3), dtype="uint8") * upper
        
        ax[0, i].imshow(lower_patch)
        ax[0, i].set_title(f'{label} (lower)')
        ax[0, i].axis('off')
        
        ax[1, i].imshow(upper_patch)
        ax[1, i].set_title(f'{label} (upper)')
        ax[1, i].axis('off')
        
    plt.show()

# Funkce pro detekci, kolik pixelů v oblasti odpovídá jednotlivým pravděpodobnostem
def detect_and_display_probability(region_image, color_ranges):
    probabilities = {key: 0 for key in color_ranges}
    plt.figure(figsize=(15, 10))
    for i, (prob, (lower, upper)) in enumerate(color_ranges.items()):
        lower = np.array(lower, dtype="uint8")
        upper = np.array(upper, dtype="uint8")
        mask = cv2.inRange(region_image, lower, upper)
        probabilities[prob] = cv2.countNonZero(mask)
        
        # Aplikace masky na region_image
        masked_region = cv2.bitwise_and(region_image, region_image, mask=mask)
        
        # Zobrazení výsledného obrázku
        plt.subplot(2, 3, i + 1)
        plt.imshow(masked_region)
        plt.title(f'{prob}')
        plt.axis('off')
        
    plt.show()
    return probabilities

# URL obrázku
img_url = 'https://info.chmi.cz/bio/maps/houby_1.png'

# Stažení obrázku
response = requests.get(img_url)
img = Image.open(BytesIO(response.content)).convert('RGB')

# Konverze obrázku na formát kompatibilní s OpenCV
image = np.array(img)


y_range = (750, 850)
x_range = (1500, 1750)

y1, y2 = y_range
x1, x2 = x_range

region_image = image[y1:y2, x1:x2]



shift = 20

color_values = ([232,131,119], [250,181,142], [255,255,214], [177,221,156], [111,190,142])

color_ranges = {
    "velmi nizka": (np.clip(np.array(color_values[0]) - shift, 0, 255).tolist(), np.clip(np.array(color_values[0]) + shift, 0, 255).tolist()),
    "nizka": (np.clip(np.array(color_values[1]) - shift, 0, 255).tolist(), np.clip(np.array(color_values[1]) + shift, 0, 255).tolist()),
    "stredni": (np.clip(np.array(color_values[2]) - shift, 0, 255).tolist(), np.clip(np.array(color_values[2]) + shift, 0, 255).tolist()),
    "vysoka": (np.clip(np.array(color_values[3]) - shift, 0, 255).tolist(), np.clip(np.array(color_values[3]) + shift, 0, 255).tolist()),
    "velmi vysoka": (np.clip(np.array(color_values[4]) - shift, 0, 255).tolist(), np.clip(np.array(color_values[4]) + shift, 0, 255).tolist())
}

# Detekce a zobrazení pravděpodobností v oblasti
probabilities = detect_and_display_probability(region_image, color_ranges)

# Výpočet dominantní pravděpodobnosti
dominant_probability = max(probabilities, key=probabilities.get)


visualize_color_ranges(color_ranges)


print(f'Dominantní pravděpodobnost růstu hub ve vybrané oblasti je: {dominant_probability}')


message = MIMEText('Dokonalá automatizace v praxi. Nechávám Python, aby za mě posílal email. Jak lovely! :)')
subject = f'Růst hub v tvé oblasti pro den {str(date.today())}: {dominant_probability} pravděpodobnost'  # Předmět

username = os.getenv('EMAIL_USERNAME')
password = os.getenv('EMAIL_PASSWORD')
recipients = os.getenv('RECIPIENTS').split(',')

body = f'''
<html>
  <body>
    <p>Dominantní pravděpodobnost růstu hub ve tvé oblasti je {dominant_probability}<br>
       <a href="https://info.chmi.cz/bio/mapy.php?type=houby">Klikněte zde pro více informací</a>
    </p>
  </body>
</html>
'''

send_email(username, password, recipients, subject, body)