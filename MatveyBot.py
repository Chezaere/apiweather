import requests
import json
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from bs4 import BeautifulSoup


TOKEN, API_KEY, URL_WEATHER_API = '6194811158:AAEO6BLzw-71rI8sb0aDa4ssq4cB2QTAvi0', '024231d957544541191bed7d32c258cd', 'https://api.openweathermap.org/data/2.5/weather'
bot = telebot.TeleBot(TOKEN)
EMOJI_CODE = {200: '⛈',
              201: '⛈',
              202: '⛈',
              210: '🌩',
              211: '🌩',
              212: '🌩',
              221: '🌩',
              230: '⛈',
              231: '⛈',
              232: '⛈',
              301: '🌧',
              302: '🌧',
              310: '🌧',
              311: '🌧',
              312: '🌧',
              313: '🌧',
              314: '🌧',
              321: '🌧',
              500: '🌧',
              501: '🌧',
              502: '🌧',
              503: '🌧',
              504: '🌧',
              511: '🌧',
              520: '🌧',
              521: '🌧',
              522: '🌧',
              531: '🌧',
              600: '🌨',
              601: '🌨',
              602: '🌨',
              611: '🌨',
              612: '🌨',
              613: '🌨',
              615: '🌨',
              616: '🌨',
              620: '🌨',
              621: '🌨',
              622: '🌨',
              701: '🌫',
              711: '🌫',
              721: '🌫',
              731: '🌫',
              741: '🌫',
              751: '🌫',
              761: '🌫',
              762: '🌫',
              771: '🌫',
              781: '🌫',
              800: '☀️',
              801: '🌤',
              802: '☁️',
              803: '☁️',
              804: '☁️'}
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(KeyboardButton('Получить погоду', request_location=True))
keyboard.add(KeyboardButton('О проекте'))

def get_weather(lon, lat):
    params = {'lat': lat,
              'lon': lon,
              'lang': 'ru',
              'units': 'metric',
              'appid': API_KEY}
    response = requests.get(url=URL_WEATHER_API, params=params).json()
    print(response)
    city_name = response['name']
    description = response['weather'][0]['description']
    code = response['weather'][0]['id']
    temp = response['main']['temp']
    temp_feels_like = response['main']['feels_like']
    humidity = response['main']['humidity']
    emoji = EMOJI_CODE[code]
    message = f'Погода в: {city_name}\n'
    message += f'{emoji} {description.capitalize()}.\n'
    message += f'Температура {temp}°C.\n'
    message += f'Ощущается {temp_feels_like}°C.\n'
    message += f'Влажность {humidity}%.\n'
    return message

@bot.message_handler(commands=['start'])
def send_welcome(message):
    text = 'Отправь мне свое местоположение и я отправлю тебе погоду.'
    bot.send_message(message.chat.id, text, reply_markup=keyboard)

@bot.message_handler(content_types=['location'])
def send_weather(message):
    lon, lat = message.location.longitude, message.location.latitude
    weather = get_weather(lon, lat)
    if weather:
        bot.send_message(message.chat.id, weather, reply_markup=keyboard)

@bot .message_handler(regexp='О прокте')
def send_about(message):
    bot.send_message(message.chat.id, 'Бот который может сказать вам погоду в вашем городе, где бы вы не находились!\n'
                                      'Нам достаточно просто узнать ваше местоположение!', reply_markup=keyboard)

bot.infinity_polling()


