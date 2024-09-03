import os
import requests
from dotenv import load_dotenv

class WhatsAppClient:
    def __init__(self):
        # Cargar variables de entorno
        load_dotenv()

        # Se obtiene el token e ID del número de teléfono de las variables de entorno
        self.access_token = os.getenv('WHATSAPP_ACCESS_TOKEN')
        self.phone_number_id = os.getenv('WHATSAPP_PHONE_NUMBER_ID')

        # Configurar la URL base y los headers para las solicitudes a la API
        self.base_url = f"https://graph.facebook.com/v20.0/{self.phone_number_id}/messages"
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

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

                # Ejemplo de una respuesta automática o robotizada
                response_message = f"Gracias por tu mensaje: {message_body}"
                self.send_text_message(from_number, response_message)

# Ejemplo de uso
if __name__ == "__main__":
    client = WhatsAppClient()

    # Ejemplo para enviar un mensaje de plantilla
    recipient_number = "18498613717" # aqui va el numero a quien sera enviado el mensaje
    template_name = "hello_world"
    language_code = "en_US"

    response = client.send_template_message(recipient_number, template_name, language_code)
    print("Template message response:", response)
