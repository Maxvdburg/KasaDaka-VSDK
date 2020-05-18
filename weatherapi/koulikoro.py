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

name = 'Koulikoro'
lat = '12.8627'
lon = '-7.5599'

def correct_time(unix):
    stamp = int(unix)
    return(datetime.utcfromtimestamp(stamp).strftime('%Y-%m-%d'))

def get_weather(api_key, lat, lon):
    url = "https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&units=metric&appid={}".format(lat, lon, api_key)
    r = requests.get(url)
    return r.json()

def make_audio_file(language,text,filename,city,date):
    tts = gTTS(text=text, lang=language, slow=False)
    file = (filename+city+date)
    tts.save(file+'.mp3')

def convert_mp3_to_wav():
    os.system("sh ./mp3_to_wav.sh {}".format(script_filename)) # convert all .mp3 files to .wav files

def remove_audio_files():
    os.system("sh ./remove_audio_files.sh") # remove all .mp3 and .wav files to clear diskspace

def clear_converted_map():
    os.system("sh ./clear_converted_map.sh {}".format(script_filename)) # remove all .wav files in the converted city map

def make_one_weatherforecast():
    os.system("sh ./make_one_file.sh {}".format(script_filename)) # create one single file for each forecast

def make_forecast(name, lat, lon):
    with open('database_koulikoro.csv','w') as db:
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
            break

make_forecast(name, lat, lon)


file = open('database_koulikoro.csv', 'r')
def make_filename():
    city = ''
    date = ''
    for record in file:
        filename = ''
        if "forecast" in record:
            split_record_name = (record.split(','))
            city = (split_record_name[1])
            date = (split_record_name[3].split(' ')[0])
            filename = 'en_forecast_'
            make_audio_file('en',record,filename,city,date)
        elif 'temperature' in record:
            filename = 'en_temp_'
            make_audio_file('en',record,filename,city,date)
        elif 'rain' in record:
            filename = 'en_rainfall_'
            make_audio_file('en',record,filename,city,date)
        elif 'wind' in record:
            filename = 'en_wind_'
            make_audio_file('en',record,filename,city,date)
        elif "Prévisions" in record:
            split_record_name = (record.split(','))
            city = (split_record_name[1])
            date = (split_record_name[3].split(' ')[0])
            filename = 'fr_forecast_'
            make_audio_file('fr',record,filename,city,date)
        elif 'température' in record:
            filename = 'fr_temp_'
            make_audio_file('fr',record,filename,city,date)
        elif 'précipitations' in record:
            filename = 'fr_rainfall_'
            make_audio_file('fr',record,filename,city,date)
        else:
            filename = 'fr_wind_'
            make_audio_file('fr',record,filename,city,date)
    convert_mp3_to_wav()
    remove_audio_files()
    make_one_weatherforecast()
clear_converted_map()
make_filename()
