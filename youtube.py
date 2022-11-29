from concurrent.futures import thread
import os
import threading
from time import sleep
from pytube import YouTube
from pymediainfo import MediaInfo
list_urls = []
def addToList(url):
    global list_urls
    list_urls.append(url)

def player():
    global list_urls
    duration = 0
    currentTime = 1
    while True:
        if currentTime < duration:
            sleep(1)
            currentTime += 1
            continue

        if len(list_urls)==0:
            sleep(1)
        else:
            yt = YouTube(list_urls[0]) #ссылка на видео.
            list_urls.pop(0)
            print(yt.streams.get_audio_only())
            stream = yt.streams.get_by_itag(139) #выбираем по тегу, в каком формате будем скачивать.
            stream.download() #загружаем видео.
            name = stream.title+".mp4"

            s = os.startfile(name)
            print(s)
            print(name)
            clip_info = MediaInfo.parse(name)
            duration_s = clip_info.tracks[0].duration/1000
            print(duration_s)
            currentTime = 0
            duration = duration_s
t = threading.Thread(target=player)
t.start()
