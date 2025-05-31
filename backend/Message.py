"""
WhatsApp Message Sender using Twilio API.

Loads configuration from environment variables and sends a WhatsApp message
using the Twilio API. Includes robust error handling and clear documentation.
"""

import os
from dotenv import load_dotenv
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

def get_env_variable(variable_name: str) -> str:
    """
    Retrieve the value of an environment variable.
    Raises an EnvironmentError if the variable is not set.
    """
    value = os.getenv(variable_name)
    if not value:
        raise EnvironmentError(f"Environment variable '{variable_name}' is not set.")
    return value

def send_whatsapp_message() -> None:
    """
    Send a WhatsApp message using Twilio API.
    """
    load_dotenv()
    try:
        account_sid = get_env_variable("TWILIO_ACCOUNT_SID")
        auth_token = get_env_variable("TWILIO_AUTH_TOKEN")
        twilio_whatsapp_number = get_env_variable("TWILIO_WHATSAPP_NUMBER")
        recipient_whatsapp_number = get_env_variable("YOUR_WHATSAPP_NUMBER")

        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body="Hello Karolina! This is a test message from your AI assistant 🚗 - Mistral!",
            from_=twilio_whatsapp_number,
            to=recipient_whatsapp_number
        )
        print(f"Message sent successfully! SID: {message.sid}")
    except (EnvironmentError, TwilioRestException) as error:
        print(f"Error: {error}")

if __name__ == "__main__":
    send_whatsapp_message()