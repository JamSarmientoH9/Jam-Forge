import os
from dotenv import load_dotenv

load_dotenv()

TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
VERIFY_TOKEN = os.getenv('VERIFY_TOKEN')
ACCES_TOKEN= os.getenv('YOUR_ACCES_TOKEN_HERE')
PHONE_NUMBER_ID= os.getenv('YOUR_PHONE_ID_HERE')

# Other config values :)
API_BASE_URL ='https://graph.facebook.com/v20.0/'

