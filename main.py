import telebot
import requests
from exceptions.exceptions import LocationNotFoundError
from util.time import Time
from dotenv import load_dotenv
import os

load_dotenv(verbose=True)

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPEN_WEATHER_API_KEY = os.getenv("OPEN_WEATHER_API_KEY")
YANDEX_TRANSLATE_API_KEY = os.getenv("YANDEX_TRANSLATE_API_KEY")

OPEN_WEATHER_API_ENDPOINT = "http://api.openweathermap.org/data/2.5/weather"
YANDEX_TRANSLATE_API_ENDPOINT = "https://translate.yandex.net/api/v1.5/tr.json/translate"

bot = telebot.TeleBot(BOT_TOKEN)


def get_forecast(location_name):
    params = "?q=%s&units=metric&APPID=%s" % (location_name, OPEN_WEATHER_API_KEY)
    url = "%s%s" % (OPEN_WEATHER_API_ENDPOINT, params)

    response = requests.get(url)

    if response.status_code == 404:
        raise LocationNotFoundError(expression=url, message="Location '%s' not found by the API" % location_name)

    forecast = response.json()

    main_forecast = forecast["weather"][0]["main"]
    forecast_description = forecast["weather"][0]["description"]
    temperature = str(forecast["main"]["temp"])
    min_temperature = str(forecast["main"]["temp_min"])
    max_temperature = str(forecast["main"]["temp_max"])

    return main_forecast, forecast_description, temperature, min_temperature, max_temperature


def translate_text(text, translation):
    params = "?key=%s&text=%s&lang=%s&format=plain" % (YANDEX_TRANSLATE_API_KEY, text, translation)
    url = "%s%s" % (YANDEX_TRANSLATE_API_ENDPOINT, params)

    response = requests.get(url)

    return response.json()["text"][0]


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Este bot pode lhe fornecer a previsão do tempo para diversos locais ao redor do mundo!")

    time = Time.get_time()
    print("%s - Welcome message sent\n" % time)


@bot.message_handler(commands=['tempo'])
def send_forecast(message):
    location = message.text.replace("/tempo", "").strip()

    try:
        main_forecast, forecast_description, temperature, min_temperature, max_temperature = get_forecast(location)

        forecast = "%s (%s)\n" \
                   "%s °C (máx. %s °C e min. %s °C)" % (translate_text(main_forecast, "en-pt"),
                                                        translate_text(forecast_description, "en-pt"), temperature,
                                                        min_temperature, max_temperature)

        bot.reply_to(message, "Tempo em %s:\n%s" % (location, forecast))

        time = Time.get_time()
        print("%s - Forecast sent\nLocation: %s\n%s\n" % (time, location, forecast))

    except LocationNotFoundError as e:
        e.print_error()

        bot.reply_to(message, "Localização '%s' não encontrada. Tente novamente." % location)


bot.polling()
