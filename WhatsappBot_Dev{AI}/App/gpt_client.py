"""
Develop a client to interact with the ChatGPT API. This client should handle authentication, send messages to the API, and process the responses.
"""

from openai import OpenAI
from gpt_instructions import who_is_gpt #Import to access variable storing all instructions
import os #Import os module to acces .env file

class GPTClient:
    def __init__(self):
        #Authenticates by accesing the "OPEN_AI_KEY"
        self.client = OpenAI(api_key = os.environ.get('OPEN_AI_KEY'))

        #Variable that stores all instructions for the AI (from the "who_is_gpt var in gpt_instructions")
        self.instructions = who_is_gpt

        #Functions that takes user's input from "chatbot.py"
    def chat_with_gpt(self,prompt):

        response = self.client.chat.completions.create(

        model = "gpt-3.5-turbo",
        
        messages = [

            {"role": "system", "content": self.instructions}, #Responsible for instructing the AI
            {"role": "user", "content": prompt}, #Tells the AI the user's input!

        ],
        max_tokens=90, #Writes at most 400 characters
        temperature = 1.0 #Higher temperature (2) --> random answers, lower (0)--> repetititve. Set at the middle
        )

        return response.choices[0].message.strip()
