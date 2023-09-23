from pytube import YouTube
from pytube import Playlist
import os

from mutagen.mp4 import MP4, MP4Cover
import logging

from pathlib import Path

from get_thumb import thumb_downloader

way = (Path.home() / "Movies" / "Youtube")


def make_author_folder(playlist_link):  # создаю подпапку с названием канала
    name = Playlist(playlist_link).title  # удастся ли получить имя канала
    os.makedirs(f'{way}/{name}', exist_ok=True)
    path = f'{way}/{name}'
    return path





def add_cover(thumb_path, mp4_path, tags):
    video = MP4(mp4_path)

# open downloaded thumbs to video
    with open(thumb_path, "rb") as f:
        video["covr"] = [
            MP4Cover(f.read(), imageformat=MP4Cover.FORMAT_JPEG)
        ]
        # video['\xa9nam'] = tags[2]  # This assigns the 3rd element of the tags list to the "\xa9nam" (track name) key in video. \xa9 is the unicode character for copyright symbol.
        # video['\xa9ART'] = tags[0]  # this assigns the 1st element of tags to "\xa9ART" (artist name).
        # video['\xa9alb'] = tags[1]  # this assigns the 2nd element to "\xa9alb" (album name).

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

        # download thumb
        thumb_path = thumb_downloader(p[i], path)

        tags = yt.keywords


        stream = yt.streams.get_by_itag(140)  # скачиваю с фильтром по тэгу - только аудио
        stream.download(path, f'{title}.mp4', skip_existing=True)
        mp4_path = f'{path}/{title}.mp4'  # путь к медиа файлу
        add_cover(thumb_path, mp4_path, tags)
        # with open(f"{path}/{tags[0]} - {tags[1]}.txt", 'a') as log_file:
        #     log_file.write(f'{i} - {title}\n')
    print("download completed")


if __name__ == "__main__":

    # music_downloader('https://music.youtube.com/playlist?list=PLA3BruVN0VUKZquOkBSwRpcCo36gh6ol8&feature=share')
    music_downloader('https://music.youtube.com/playlist?list=OLAK5uy_ml0VwWt_W2CmyVfC1s2zDAtQNszCUf_CM')
