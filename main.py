import botogram
import pycountry
import urllib, json 
import requests
import os
import datetime

#ADMIN = [569626820]
 
ABOUT = "This chatbot is used to fetch weather information on providing city name."
TOKEN = "6287696568:AAH2nHHJozIq-66glrpkgyknhPA1jbezLoA" 
#KEY= "9641b9143eb7da0e3cbc6015cd786fa4"
base_url = "https://api.openweathermap.org/data/2.5/onecall/timemachine"
API_KEY = os.environ.get("e23ae5e2c83c8d33cb06dc1bb4975465")

bot = botogram.create(TOKEN)
bot.owner = "Sayali Dalvi"
bot.about = ABOUT

def get_weather(city):
    res = urllib.request.urlopen(f"https://api.openweathermap.org/data/2.5/weather?q={city}&&units=metric&appid=e23ae5e2c83c8d33cb06dc1bb4975465").read()
    json_data = json.loads(res)
    # print(json_data)
    data = {
            "country_code" : str(json_data['sys']['country']),
            "coordinates" : str(json_data["coord"]["lon"]) + " " + str(json_data["coord"]["lat"]),
            "temp" : str(json_data["main"]["temp"]),
            "pressure" : str(json_data["main"]["pressure"]),
            "humidity" : str(json_data["main"]["humidity"]), 
            "city" : str(json_data['name']),
            "description" : str(json_data['weather'][0]['main']),
            "visibility" : str(json_data["visibility"]),
            "timezone" : str(json_data["timezone"])
    }
    return data

@bot.message_matches(r'(?i)^(hi|hello|hii|hiii|hey)')
def hello_command(chat, message):
    user_first_name = str(message.chat.first_name)
    """Say hello to the world!"""
    chat.send(f"""

    Hello, {user_first_name}!!
    Welcome to Weather Chatbot :)
    I can help you with weather information for any city..
    Please type <code>/start </code>for main menu
    """, syntax="html")

@bot.message_matches(r'(?i)^(thank you|thanks)')
def ty_command(chat, message):
    user_first_name = str(message.chat.first_name)
    chat.send(f"You're welcome, {user_first_name}! Happy to assist you...Thank you for using Weather API Bot.")

@bot.message_matches(r'(?i)^(bye|good bye)')
def bye_command(chat, message):
    user_first_name = str(message.chat.first_name)
    chat.send(f"Bye, {user_first_name}! Have a good day!! :)")

@bot.message_matches(r'(?i)^(tell me about yourself|what is your use|yourself)')
def urself_command(chat, message):
    user_first_name = str(message.chat.first_name)
    chat.send(f"Hello {user_first_name}! ,  I am a Weather API chatbot. I can assist you to fetch the real time dynamic weather information :) ")

#@bot.message_matches(r'(?i)^(what is weather today|weather)')
@bot.command("weather")
def weather(chat, message, args):
    """
    This feature is used to fetch weather information on providing city name.
    """
    try:
        res = get_weather(args[0])
        country_name = pycountry.countries.get(alpha_2=res['country_code']).name
        chat.send(f"""
        Country: {country_name}
        City : {res['city']}
        Cordinates : {res['coordinates']}
        Description : {res['description']}
        Temp : {res['temp']} °C
        Pressure : {res['pressure']} Pascal
        Humidity: {res['humidity']} %
        """)
    except IndexError:
        chat.send("Enter city name, for example <code>/weather Mumbai</code>", syntax="html")
    except:
        chat.send("Please try again later.")




@bot.command("forecast")
def forecast_command(chat, message):
    """
    This feature is used to give forecast weather details of next 4 days.
    """
    try:
        city_name = message.text.split(" ", 1)[1]
        api_key = "e23ae5e2c83c8d33cb06dc1bb4975465"

        url = f"http://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={api_key}"

        response = requests.get(url)
    
        if response.status_code == 200:
                data = response.json()
                forecast_list = data["list"]
                response_text = f"Hourly forecast for {city_name}:\n"

                for forecast in forecast_list:
                    forecast_date = forecast["dt_txt"]
                    forecast_temp = round(forecast["main"]["temp"] - 273.15, 2)
                    forecast_desc = forecast["weather"][0]["description"]
                    response_text += f"{forecast_date}: {forecast_desc}, Temperature: {forecast_temp}°C\n"

                    if len(response_text) > 3000: # Telegram message size limit
                        chat.send(response_text)
                        response_text = ""

                if len(response_text) > 0:
                    chat.send(response_text)
        else:
                chat.send("Error retrieving data.")
    except IndexError:
        chat.send("Enter city name, for example<code>/forecast Mumbai</code>", syntax="html")
    except:
        chat.send("Please try again later.")
    
    

@bot.command("pollution")
def pollution_command(chat, message, args):
    """
    This feature is used to give air pollution details of given city.
    """
    try:
        if len(args) != 1:
            chat.send("Please provide a city name as argument. eg: /pollution Mumbai")
            return
    
        city_name = args[0]
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid=e23ae5e2c83c8d33cb06dc1bb4975465"
        response = requests.get(url)
    
        if response.status_code != 200:
            chat.send("Error retrieving data.")
            return
    
        data = response.json()
        lat = data["coord"]["lat"]
        lon = data["coord"]["lon"]
    
        url = f"https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid=e23ae5e2c83c8d33cb06dc1bb4975465"
        response = requests.get(url)
    
        if response.status_code != 200:
            chat.send("Error retrieving data.")
            return
    
        air_pollution_data = response.json()
        aqi = air_pollution_data["list"][0]["main"]["aqi"]
        pm10 = air_pollution_data["list"][0]["components"]["pm10"]
        pm25 = air_pollution_data["list"][0]["components"]["pm2_5"]
        co2 = air_pollution_data["list"][0]["components"]["co"]
        no2 = air_pollution_data["list"][0]["components"]["no"]
        o3 = air_pollution_data["list"][0]["components"]["o3"]
        so2 = air_pollution_data["list"][0]["components"]["so2"]
    
        chat.send(f"""
        The air quality in {city_name} is currently {aqi}, with PM10 at {pm10} μg/m³ and PM2.5 at {pm25} μg/m³.
        Components in air :
        co2 : {co2}
        no2: {no2}
        o3: {o3}
        so2: {so2}""")
    except IndexError:
        chat.send("Enter city name, for example <code>/pollution Mumbai</code>", syntax="html")
    except:
        chat.send("Please try again later.")



@bot.command("history")
def history_command(chat, message):
    """
    This feature is used to give weather history of city using unix timestamp.
    """
    try:
        location = message.text.split(" ", 2)[1]
        date = message.text.split(" ", 2)[2]
        api_key = "e23ae5e2c83c8d33cb06dc1bb4975465"

        url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&dt={date}"

        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            temperature = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            pressure = data["main"]["pressure"]
            description = data["weather"][0]["description"]

            response_text = f"Weather on {date} in {location}: {description}, Temperature: {temperature} K, Humidity: {humidity}%, Pressure: {pressure} hPa"
            chat.send(response_text)
        else:
            chat.send("Error retrieving data.")
    except IndexError:
        chat.send("Enter city name, for example <code>/hisotry Mumbai unix_timestamp i.e /history Mumbai 1678677170</code>", syntax="html")
    except:
        chat.send("Please try again later.")




if __name__ == "__main__":
    bot.run()

