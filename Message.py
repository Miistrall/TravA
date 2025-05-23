from dotenv import load_dotenv
load_dotenv()

from twilio.rest import Client
import os

# Pobierz dane z zmiennych środowiskowych
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_whatsapp_number = os.getenv("TWILIO_WHATSAPP_NUMBER")
your_whatsapp_number = os.getenv("YOUR_WHATSAPP_NUMBER")

# Utwórz klienta Twilio
client = Client(account_sid, auth_token)

# Wyślij wiadomość
message = client.messages.create(
    body="Cześć Karolina! To jest testowa wiadomość od Twojego asystenta AI 🚗 - Mistral!",
    from_=twilio_whatsapp_number,
    to=your_whatsapp_number
)

print(f"Wiadomość wysłana! SID: {message.sid}")

# Upewnij się, że Twilio Sandbox jest aktywowany i Twój numer jest zweryfikowany