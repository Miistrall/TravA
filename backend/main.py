"""
Main integration script for Travel Assistant.

Fetches current weather using Weather.py and sends it via WhatsApp using Message.py.
"""

from Weather import get_current_weather
from Message import get_env_variable
from dotenv import load_dotenv # type: ignore

def send_weather_via_whatsapp(city: str):
    """
    Fetch weather for the given city and send it via WhatsApp.
    """
    load_dotenv()
    try:
        weather = get_current_weather(city)
        description = weather['weather'][0]['description']
        temp = weather['main']['temp']
        message = f"Weather in {city}: {description}, temperature: {temp}°C"
        
        # Prepare WhatsApp message sending
        from twilio.rest import Client # type: ignore
        account_sid = get_env_variable("TWILIO_ACCOUNT_SID")
        auth_token = get_env_variable("TWILIO_AUTH_TOKEN")
        twilio_whatsapp_number = get_env_variable("TWILIO_WHATSAPP_NUMBER")
        recipient_whatsapp_number = get_env_variable("YOUR_WHATSAPP_NUMBER")
        client = Client(account_sid, auth_token)
        client.messages.create(
            body=message,
            from_=twilio_whatsapp_number,
            to=recipient_whatsapp_number
        )
        print("Weather sent via WhatsApp!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    city = input("Enter city name: ")
    send_weather_via_whatsapp(city)
