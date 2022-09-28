from pytube import YouTube
from pytube import Playlist
import os
import requests
from mutagen.mp4 import MP4, MP4Cover
import logging
import time
from pathlib import Path


way = (Path.home() / "Movies" / "Youtube")


def make_author_folder(playlist_link):  # создаю подпапку с названием канала
    name = Playlist(playlist_link).title  # удастся ли получить имя канала
    os.makedirs(f'{way}/{name}', exist_ok=True)
    path = f'{way}/{name}'
    return path


def thumb_downloader(thumb_link, path):  # скачиваю иконку и возвращаю путь к ней
    img = requests.get(thumb_link).content
    time.sleep(1)
    with open(os.path.join(path, 'thumb.jpg'), "wb") as tm_file:
        tm_file.write(img)
    # путь к файлу обложки
    thumb_path = f'{path}/thumb.jpg'
    return thumb_path


def add_cover(thumb_path, mp4_path, tags):
    video = MP4(mp4_path)

    with open(thumb_path, "rb") as f:
        video["covr"] = [
            MP4Cover(f.read(), imageformat=MP4Cover.FORMAT_JPEG)
        ]
        video['\xa9nam'] = tags[2]
        video['\xa9ART'] = tags[0]
        video['\xa9alb'] = tags[1]

    video.save()


def music_downloader(playlist_link):
    p = Playlist(playlist_link)  # список со ссылками на видео
    print(p)
    path = make_author_folder(playlist_link)
    print(f'на канале {len(p)} роликов')
    for i in range(len(p)):
        logging.basicConfig(
            level=logging.DEBUG,
            filename="mylog.log",
            format="%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s",
            datefmt='%H:%M:%S',
        )
        yt = YouTube(p[i])
        title = yt.title.replace('/', '')
        print(f"start download {title}")
        thumb_link = yt.thumbnail_url
        tags = yt.keywords
        thumb_path = thumb_downloader(thumb_link, path)

        stream = yt.streams.get_by_itag(140)  # скачиваю с фильтром по тэгу - только аудио
        stream.download(path, f'{title}.mp4', skip_existing=True)
        mp4_path = f'{path}/{title}.mp4'  # путь к медиа файлу
        add_cover(thumb_path, mp4_path, tags)
        with open(f"{path}/{tags[0]} - {tags[1]}.txt", 'a') as log_file:
            log_file.write(f'{i} - {title}\n')
    print("download completed")


if __name__ == "__main__":
    playlist_link = 'https://youtube.com/playlist?list=PLv6k_E5x1Ddb-niDWSIY0gWqNQielehyP'
    music_downloader(playlist_link)
