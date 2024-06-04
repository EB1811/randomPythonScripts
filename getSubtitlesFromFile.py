import requests
import openai
import os
import subprocess

openai.api_key = ""

def get_subtitles(file, subtitle_format='srt', **kwargs):
    url = 'https://api.openai.com/v1/audio/transcriptions'
    headers = {
        'Authorization': f'Bearer {openai.api_key}',
    }
    data = {
        'model': 'whisper-1',
        'response_format': subtitle_format,
        #'response_format':"verbose_json",
        #'timestamp_granularities':["word"],
    }
    data.update(kwargs)
    files = {
        'file': (file, open(file, 'rb'))
    }

    response = requests.post(url, headers=headers, data=data, files=files)
    return response.text

def convert_to_ogg(filenames):
    for filename in filenames:
        command = f'ffmpeg -i "{filename}.mp4" -vn -map_metadata -1 -ac 1 -c:a libopus -b:a 12k -application voip "{filename}.ogg"'
        print("command", command)
        subprocess.run(command, shell=True)


def create_subtitles(filenames):
    for filename in filenames:
        subtitles = get_subtitles(filename + ".ogg")
        print(subtitles)

        with open(filename + '.srt', 'w', encoding="utf-8") as f:
            f.write(subtitles)


def create_subs_from_mp4(filenames):
    convert_to_ogg(filenames)
    create_subtitles(filenames)
