#!brew install sox
#!pip install gTTS

import configparser
import requests
import sys
from datetime import datetime
from gtts import gTTS
import os
import csv

api_key=('57519d394c970d37633e800dc962803c')
script_filename = __file__.split('.')[0]

name = 'Kati'
lat = '12.7441'
lon = '-8.0726'

def correct_time(unix):
    stamp = int(unix)
    return(datetime.utcfromtimestamp(stamp).strftime('%Y-%m-%d'))

def get_weather(api_key, lat, lon):
    url = "https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&units=metric&appid={}".format(lat, lon, api_key)
    r = requests.get(url)
    return r.json()

def make_audio_file(language,text,filename,city):
    tts = gTTS(text=text, lang=language, slow=False)
    file = (filename+city)
    tts.save(file+'.mp3')

def convert_mp3_to_wav():
    os.system("sh ./mp3_to_wav.sh {}".format(script_filename))

def remove_audio_files():
    os.system("sh ./remove_audio_files.sh") # remove all .mp3 and .wav files to clear diskspace

def clear_converted_map():
    os.system("sh ./clear_converted_map.sh {}".format(script_filename)) # remove all .wav files in the converted city map


def make_forecast(name, lat, lon):
    with open('database_kati.csv','w') as db:
        writer = csv.writer(db, delimiter=',')
        weather = get_weather(api_key, lat, lon)
        for i in range(len(weather)):
            writer.writerow(("Weather forecast in",name,"for",correct_time((weather['daily'][i]['dt']))))
            for data in weather:
                if 'rain' in data:
                    writer.writerow(("the expected rainfall is",weather['daily'][i]['rain'],"millimeters"))
                else:
                    writer.writerow(("There is no rainfall", "expected"))
            writer.writerow(("the expected temperature is",weather['daily'][i]['temp']['day'],"celsius"))
            writer.writerow(("the expected windstrength is",weather['daily'][i]['wind_speed'],"kilometers"))
            ### add french translations to database
            writer.writerow(("Prévisions météo dans",name,"pour",correct_time((weather['daily'][i]['dt']))))
            for data in weather:
                if 'rain' in data:
                    writer.writerow(("les précipitations attendues sont",weather['daily'][i]['rain'],"millimeters"))
                else:
                    writer.writerow(("Il n'y a pas de précipitations", "attendues"))
            writer.writerow(("la température attendue est",weather['daily'][i]['temp']['day'],"celsius"))
            writer.writerow(("la force du vent attendue est",weather['daily'][i]['wind_speed'],"kilometers"))
            break  #ervoor te zorgen dat je niet ineens 1000 audio files maakt

make_forecast(name, lat, lon)


file = open('database_kati.csv', 'r') #open de database
def make_filename():
    city = '' #lege variabele die wordt gevuld indien nieuwe citynaam wordt gevonden
    date = '' #lege variabele die wordt gevuld indien nieuwe datum wordt gevonden
    for record in file:
        filename = ''
        if "forecast" in record:
            split_record_name = (record.split(','))
            city = (split_record_name[1])
            filename = 'en_forecast_'
            make_audio_file('en',record,filename,city)
        elif 'temperature' in record:
            filename = 'en_temp_'
            make_audio_file('en',record,filename,city)
        elif 'rain' in record:
            filename = 'en_rainfall_'
            make_audio_file('en',record,filename,city)
        elif 'wind' in record:
            filename = 'en_wind_'
            make_audio_file('en',record,filename,city)
        elif "Prévisions" in record:
            split_record_name = (record.split(','))
            city = (split_record_name[1])
            filename = 'fr_forecast_'
            make_audio_file('fr',record,filename,city)
        elif 'température' in record:
            filename = 'fr_temp_'
            make_audio_file('fr',record,filename,city)
        elif 'précipitations' in record:
            filename = 'fr_rainfall_'
            make_audio_file('fr',record,filename,city)
        else:
            filename = 'fr_wind_'
            make_audio_file('fr',record,filename,city)
    convert_mp3_to_wav()
    remove_audio_files()
clear_converted_map()
make_filename()
