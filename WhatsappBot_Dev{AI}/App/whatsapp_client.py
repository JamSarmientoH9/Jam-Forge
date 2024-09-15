import os
import requests
from dotenv import load_dotenv
from gpt_client import GPTClient

class WhatsAppClient:
    def __init__(self):
        # Cargar variables de entorno
        load_dotenv()

        # Se obtiene el token e ID del número de teléfono de las variables de entorno
        self.access_token = os.getenv('ACCES_TOKEN')
        self.phone_number_id = os.getenv('PHONE_NUMBER_ID')

        # Configurar la URL base y los headers para las solicitudes a la API
        self.base_url = f"https://graph.facebook.com/v20.0/{self.phone_number_id}/messages"
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        self.gpt_client = GPTClient()
    def send_message(self, recipient_number, message_type, message_content):
        # Preparar el payload para enviar el mensaje
        payload = {
            "messaging_product": "whatsapp",
            "to": recipient_number,
            "type": message_type,
            message_type: message_content
        }

        # Enviar la solicitud POST a la API de WhatsApp
        response = requests.post(self.base_url, headers=self.headers, json=payload)

        # Manejar la respuesta
        if response.status_code == 200:
            print("Message sent successfully!")
            return response.json()
        else:
            print(f"Error sending message: {response.status_code}")
            print(f"Response details: {response.text}")
            return None

    def send_template_message(self, recipient_number, template_name, language_code="en_US"):
        payload = {
            "messaging_product": "whatsapp",
            "to": recipient_number,
            "type": "template",
            "template": {
                "name": template_name,
                "language": {
                    "code": language_code
                }
            }
        }
        return self.send_request(payload)
    # resultados de la solicitud para depurar
    def send_request(self, payload):
        response = requests.post(self.base_url, headers=self.headers, json=payload)
        print(f"Full API response: {response.text}")
        if response.status_code == 200:
            print("Message sent successfully!")
            return response.json()
        else:
            print(f"Error sending message: {response.status_code}")
            print(f"Response details: {response.text}")
            return None

    def process_incoming_message(self, webhook_data):
        # Extrae la información relevante de los mensajes para enviársela al servidor
        messages = webhook_data.get('messages', [])

        for message in messages:
            from_number = message.get('from')  # Extrae el número del remitente
            message_body = message.get('text', {}).get('body', '')  # Extrae el contenido del mensaje de texto

            # Se procesa el mensaje
            if message_body:
                print(f"Mensaje recibido de {from_number}: {message_body}")

                # Usar GPT para generar una respuesta
                gpt_response = self.gpt_client.generate_response(message_body)

                # Enviar la respuesta generada por GPT
                self.send_message(from_number, "text", {"body": gpt_response})

# Ejemplo de uso
if __name__ == "__main__":
    client = WhatsAppClient()

    recipient_number = "18498613717"
    message_type = "text"
    message_content = {
        "body": "ESTOY HARTO"  # El mensaje de texto debe estar en un diccionario con 'body'
    }

    # Llamada para enviar el mensaje
    whatsapp_client = WhatsAppClient()
    response_sent = whatsapp_client.send_message(
        recipient_number=recipient_number,
        message_type=message_type,
        message_content=message_content
    )

"""PROCUREN DE ACTUALIZAR CADA VEZ SU ACCES TOKEN Y DEMAS,GRACIAS :)"""