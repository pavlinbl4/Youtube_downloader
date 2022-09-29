from pytube import YouTube
from pytube import Playlist
import os
import requests
from mutagen.mp4 import MP4, MP4Cover
import logging
import time
from check_file_exist import check_file


def make_author_folder(channel_link):  # создаю подпапку с названием канала
    channel_author = Playlist(channel_link).owner  # удастся ли получить имя канала
    os.makedirs(f'/Users/evgeniy/Movies/Youtube/{channel_author}', exist_ok=True)
    path = f'/Users/evgeniy/Movies/Youtube/{channel_author}'
    return path


def thumb_downloader(thumb_link, path):  # скачиваю иконку и возвращаю путь к ней
    img = requests.get(thumb_link).content
    time.sleep(1)
    with open(os.path.join(path, 'thumb.jpg'), "wb") as tm_file:
        tm_file.write(img)
    thumb_path = f'{path}/thumb.jpg'
    return thumb_path


def add_cover(thumb_path, mp4_path):
    video = MP4(mp4_path)

    with open(thumb_path, "rb") as f:
        video["covr"] = [
            MP4Cover(f.read(), imageformat=MP4Cover.FORMAT_JPEG)
        ]

    video.save()


def abook_downloader(playlist_link):
    list_of_videos = Playlist(playlist_link)  # список со ссылками на видео
    path = make_author_folder(playlist_link)
    print(f'на канале {len(list_of_videos)} роликов')
    for i in range(len(list_of_videos)):
        # logging.basicConfig(
        #     level=logging.DEBUG,
        #     filename="mylog.log",
        #     format="%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s",
        #     datefmt='%H:%M:%S',
        # )
        yt = YouTube(list_of_videos[i])
        title = yt.title.replace('/', '')
        if check_file(f'{path}/{title}.mp4'):
            print("This file was downloaded")
        else:
            print(f"start download {title}")
            thumb_link = yt.thumbnail_url
            thumb_path = thumb_downloader(thumb_link, path)
            stream = yt.streams.get_by_itag(140)  # скачиваю с фильтром по тэгу - только аудио
            stream.download(path, f'{title}.mp4', skip_existing=True)
            mp4_path = f'{path}/{title}.mp4'  # путь к медиа файлу
            add_cover(thumb_path, mp4_path)
            with open(f"{path}/playlist.txt", 'a') as log_file:
                log_file.write(f'{i} - {title}\n')
    print("download completed")


if __name__ == "__main__":
    playlist_link = 'https://youtube.com/playlist?list=PL65ijVzWl9ksD5m5fRrFIlbWX2fGD-wYg'
    abook_downloader(playlist_link)
