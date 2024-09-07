"""
Controls the main logic for the ChatBot, including message processing and interaction with the GPT API to generate responses.

"""
import time
from gpt_client import GPTClient # import the GPTClient class

# Initialize the GPTClient
gpt_client = GPTClient()

#Function that collects user's message, stores and returns it in a "u_message" variable
def chat_with_user():
    u_message = input("👤: ")
    return u_message

#While loop that keeps asking the user for a message + interacts with the API to generate response

while True:
    message = chat_with_user()
    time.sleep(5)
    gpt_response = gpt_client.chat_with_gpt(message)
    print(f"🖥️: {gpt_response}")

