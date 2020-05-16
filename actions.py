from rasa_sdk import Action
from rasa_sdk.events import SlotSet
import requests

class ActionWeather(Action):
	def name(self):
		return 'action_weather'
		
	def run(self, dispatcher, tracker, domain):
		from apixu.client import ApixuClient
		api_key = '46eff37dce25f901d5d4dad8f3d7aa1c' #your apixu key
		client = ApixuClient(api_key)
		
		loc = tracker.get_slot('location')
		api_address='http://api.weatherstack.com/current?access_key={}&query={}'.format(api_key,loc) #for json data		
		current = requests.get(api_address).json()
		#current = client.current(q=loc)
		
		country = current['location']['country']
		city = current['location']['name']
		#condition = current['current']['condition']['text']
		temperature_c = current['current']['temperature']
		humidity = current['current']['humidity']
		wind_mph = current['current']['wind_speed']
		
		response = """In {} at the moment. The temperature is {}' degrees, the humidity is {}% and the wind speed is {} mph.""".format( city, temperature_c, humidity, wind_mph)

		#response = """It is currently {} in {} at the moment. The temperature is {} degrees, the humidity is {}% and the wind speed is {} mph.""".format( city, temperature_c, humidity, wind_mph)
						
		dispatcher.utter_message(response)
		return [SlotSet('location',loc)]

