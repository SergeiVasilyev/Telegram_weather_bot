import os
import pyowm
import telebot

from pathlib import Path
from dotenv import load_dotenv

dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)

os.system('cls' if os.name == 'nt' else 'clear')
owm = pyowm.OWM(os.getenv('PYOWM_API_KEY'))
bot = telebot.TeleBot(os.getenv('TELEBOT_API_KEY'))
mgr = owm.weather_manager()

count = 0

@bot.message_handler(content_types=['text'])
def send_echo(message):
	global count
	try:
		observation = mgr.weather_at_place( message.text )
	except Exception:
		if message.text == "_count":
			answer = "There were " + str(count) + " requests"
		else:
			answer = "You entered an incorrect location"

	else:
		observation = mgr.weather_at_place( message.text )
		w = observation.weather
		temp = round(w.temperature('celsius')["temp"])
		humidity = w.humidity
		wind = w.wind()['speed']
		location = observation.to_dict()['location']['name']
		
		answer = "Today in " + location + " " + w.detailed_status + "\n"
		answer += "Temperature " + str(temp) + chr(176) + "С \n"
		answer += "Humidity " + str(humidity) + "% \n"
		answer += "Wind " + str(wind) + " м/с \n"
		count += 1
		
	bot.send_message(message.chat.id, answer)

bot.polling( none_stop = True )