from pytube import YouTube
from pytube import Channel
import os
import requests
from mutagen.mp4 import MP4, MP4Cover
import logging
import time


def make_author_folder(channel_link):  # создаю подпапку с названием канала
    name = Channel(channel_link).channel_name  # удастся ли получить имя канала
    os.makedirs(f'/Users/evgeniy/Movies/Youtube/{name}', exist_ok=True)
    path = f'/Users/evgeniy/Movies/Youtube/{name}'
    return path


def thumb_downloader(thumb_link, path):  # скачиваю иконку и возвращаю путь к ней
    img = requests.get(thumb_link).content
    time.sleep(1)
    with open(os.path.join(path, 'thumb.jpg'), "wb") as tm_file:
        tm_file.write(img)
    # путь к файлу обложки
    thumb_path = f'{path}/thumb.jpg'
    return thumb_path


def add_cover(thumb_path, mp4_path):
    video = MP4(mp4_path)

    with open(thumb_path, "rb") as f:
        video["covr"] = [
            MP4Cover(f.read(), imageformat=MP4Cover.FORMAT_JPEG)
        ]

    video.save()


def abook_downloader(channel_link):
    c = Channel(channel_link)  # список со ссылками на видео
    path = make_author_folder(channel_link)
    print(f'на канале {len(c)} роликов')
    for i in range(671, len(c)):
        logging.basicConfig(
            level=logging.DEBUG,
            filename="mylog.log",
            format="%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s",
            datefmt='%H:%M:%S',
        )
        yt = YouTube(c[i])
        title = yt.title.replace('/', '')
        print(f"start download {title}")
        thumb_link = yt.thumbnail_url
        thumb_path = thumb_downloader(thumb_link, path)
        stream = yt.streams.get_by_itag(140)  # скачиваю с фильтром по тэгу - только аудио
        stream.download(path, f'{title}.mp4', skip_existing=True)
        mp4_path = f'{path}/{title}.mp4'  # путь к медиа файлу
        add_cover(thumb_path, mp4_path)
        with open(f"{path}/buldakov.txt", 'a') as log_file:
            log_file.write(f'{i} - {title}\n')
    print("download completed")


if __name__ == "__main__":
    channel_link = 'https://www.youtube.com/channel/UCxrrzmQZPeEHSCQmiR_BA-g'
    abook_downloader(channel_link)
