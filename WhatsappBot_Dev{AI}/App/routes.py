from flask import Flask, request, jsonify, abort
from whatsapp_client import WhatsAppClient
from gpt_client import GPTClient
import logging
import os

# Initialize Flask app
app = Flask(__name__)

# Initialize WhatsApp client and the GPTClient classes
whatsapp_client = WhatsAppClient()

gpt_client = GPTClient()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@app.route('/webhook', methods=['POST'])
def whatsapp_webhook():
    try:
        # Parse JSON payload from the request
        webhook_data = request.get_json()
        if not webhook_data:
            logging.error("Invalid JSON payload received")
            abort(400, description="Invalid JSON payload")

        # Extract messages
        messages = webhook_data.get('messages', [])
        if not messages:
            logging.warning("No messages found in payload")
            return jsonify({"status": "success"}), 200

        # Process each message
        for message in messages:
            from_number = message.get('from')
            text = message.get('text', {}).get('body', '')

            if text:
                logging.info(f"Message received from {from_number}: {text}")

                # Generate response from GPT
                gpt_response = gpt_client.chat_with_gpt(text)
                if not gpt_response:
                    logging.error("Failed to get response from GPT")
                    abort(500, description="Failed to generate response")

                logging.info(f"GPT Response: {gpt_response}")

                # Send response back to WhatsApp
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
    app.run(debug=True, port=int(os.getenv('PORT', 5000)))
