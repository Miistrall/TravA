"""
Main integration script for Travel Assistant.

Fetches current weather using Weather.py and sends it via WhatsApp using Message.py.
"""

from flask import Flask, request, Response # type: ignore
from Weather import get_current_weather, get_hourly_forecast
from Message import get_env_variable
from dotenv import load_dotenv # type: ignore
from twilio.twiml.messaging_response import MessagingResponse # type: ignore

app = Flask(__name__)

@app.route("/whatsapp", methods=["POST"])
def whatsapp_webhook():
    load_dotenv()
    incoming_msg = request.values.get("Body", "").strip()
    resp = MessagingResponse()
    reply = resp.message()

    if incoming_msg.lower().startswith("pogoda") or incoming_msg.lower().startswith("weather"):
        # Extract city name
        parts = incoming_msg.split(maxsplit=1)
        if len(parts) < 2:
            reply.body("Podaj nazwę miasta, np. 'pogoda Warszawa'")
        else:
            city = parts[1]
            try:
                weather = get_current_weather(city)
                description = weather['weather'][0]['description']
                temp = weather['main']['temp']
                message = f"Pogoda w {city}: {description}, temperatura: {temp}°C\n"
                forecast_list = get_hourly_forecast(city, hours=3)
                message += "Prognoza na kolejne godziny:\n"
                for forecast in forecast_list:
                    time = forecast['dt_txt']
                    desc = forecast['weather'][0]['description']
                    temp_f = forecast['main']['temp']
                    message += f"{time}: {desc}, {temp_f}°C\n"
                reply.body(message)
            except Exception as e:
                reply.body(f"Błąd: {e}")
    else:
        reply.body("Napisz 'pogoda [miasto]', np. 'pogoda Warszawa', aby otrzymać prognozę.")

    return Response(str(resp), mimetype="application/xml")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
