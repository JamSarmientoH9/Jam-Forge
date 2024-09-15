from flask import Flask, request, jsonify, abort
from whatsapp_client import WhatsAppClient
from gpt_client import GPTClient
import logging
from data_prepocessing import DataPreprocessor


# Initialize Flask app
app = Flask(__name__)

# Initialize WhatsApp client and the GPTClient classes
whatsapp_client = WhatsAppClient()

gpt_client = GPTClient()
data_preprocessor = DataPreprocessor()
# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


@app.route('/webhook', methods=['GET'])
def verify_webhook():
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')

    if mode and token:
        if mode == 'subscribe' and token == "toy_harto" :
            logging.info("Webhook verified")
            return challenge, 200
        else:
            logging.warning("Webhook verification failed")
            abort(403)
    logging.warning("Invalid request for webhook verification")
    return jsonify({"status": "Webhook endpoint is working!"}), 200

@app.route('/webhook', methods=['POST'])
def whatsapp_webhook():
    try:
        webhook_data = request.get_json()
        logging.info(f"Webhook data received: {webhook_data}")

        if 'entry' not in webhook_data or not webhook_data['entry']:
            logging.warning("No 'entry' in webhook data")
            return jsonify({"status": "no action needed"}), 200

        messages = webhook_data['entry'][0]['changes'][0]['value'].get('messages', [])

        if not messages:
            logging.warning("No messages found in payload")
            return jsonify({"status": "no messages"}), 200

        for message in messages:
            from_number = message['from']
            if 'text' in message:
                text = message['text']['body']
                logging.info(f"Message received from {from_number}: {text}")

                gpt_response = gpt_client.chat_with_gpt(text)
                if not gpt_response:
                    logging.error("Failed to get response from GPT")
                    gpt_response = "Lo siento, no pude procesar tu mensaje en este momento."

                logging.info(f"GPT Response: {gpt_response}")

                response_sent = whatsapp_client.send_message(
                    recipient_number=from_number,
                    message_type="text",
                    message_content={"body": gpt_response}
                )

                if not response_sent:
                    logging.error("Failed to send response to WhatsApp")
                    abort(500, description="Failed to send response")

    except Exception as e:
        logging.error(f"Error processing message: {e}")
        abort(500, description="Internal Server Error")

    return jsonify({"status": "success"}), 200


if __name__ == '__main__':
    app.run()