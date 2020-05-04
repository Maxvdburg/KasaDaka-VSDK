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

name = 'Kita'
lat = '13.0349'
lon = '-9.4895'

def correct_time(unix):
    stamp = int(unix)
    return(datetime.utcfromtimestamp(stamp).strftime('%Y-%m-%d %H:%M:%S'))

def get_weather(api_key, lat, lon):
    url = "https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&units=metric&appid={}".format(lat, lon, api_key)
    r = requests.get(url)
    return r.json()

def make_audio_file(text,filename,city,date):
    language = 'en'
    tts = gTTS(text=text, lang=language, slow=False)
    file = (filename+city+date)
    tts.save(file+'.mp3')

def convert_mp3_to_wav():
    os.system("./mp3_to_wav.sh {}".format(script_filename))
    #os.system("sh ./mp3_to_wav.sh") # convert all .mp3 files to .wav files
    #os.system("sh ./convert_wav.sh") # convert all .wav files into wav files with sample rate 8KHz, 16 bit, mono, Codec: PCM 16 LE (s16l)

def remove_audio_files():
    os.system("sh ./remove_audio_files.sh") # remove all .mp3 and .wav files to clear diskspace

def make_one_file():
    os.system("./make_one_file.sh {}".format(script_filename))

def make_forecast(name, lat, lon):
    with open('database_kita.csv','a') as db:
        writer = csv.writer(db, delimiter=',')
        weather = get_weather(api_key, lat, lon)
        for i in range(len(weather)):
            writer.writerow(("Weather forecast in",name,"for",correct_time((weather['daily'][i]['dt']))))
            writer.writerow(("the expected maximum temperature is",weather['daily'][i]['temp']['max'],"celsius"))
            writer.writerow(("the expected sun intensity on UV scale is",weather['daily'][i]['uvi']))
            writer.writerow(("the expected windstrength is",weather['daily'][i]['wind_speed'],"kilometers"))
            if i >= 2: #haal dit weg om de gehele db te maken, heb dit puur gedaan om
                break  #ervoor te zorgen dat je niet ineens 1000 audio files maakt

make_forecast(name, lat, lon)

file = open('database_kita.csv', 'r') #open de database
def make_filename():
    city = '' #lege variabele die wordt gevuld indien nieuwe citynaam wordt gevonden
    date = '' #lege variabele die wordt gevuld indien nieuwe datum wordt gevonden
    for record in file:
        filename = ''
        if "forecast" in record:
            split_record_name = (record.split(','))
            city = (split_record_name[1]+"_")
            date = (split_record_name[3].split(' ')[0])
            filename = 'forecast_'
            make_audio_file(record,filename,city,date)
        elif 'maximum' in record:
            filename = 'maximum_temp_'
            make_audio_file(record,filename,city,date)
        elif 'sun' in record:
            filename = 'sun_intensity_'
            make_audio_file(record,filename,city,date)
        else:
            filename = 'wind_'
            make_audio_file(record,filename,city,date)
    convert_mp3_to_wav()
    remove_audio_files()
    make_one_file()
make_filename()
