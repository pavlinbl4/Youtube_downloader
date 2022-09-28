# add cover to mp4 file

from mutagen.mp4 import MP4, MP4Cover


def add_cover_to_file(path_to_mp4_file, path_to_image):
    video = MP4(path_to_mp4_file)

    with open(path_to_image, "rb") as f:
        video["covr"] = [
            MP4Cover(f.read(), imageformat=MP4Cover.FORMAT_JPEG)
        ]

    video.save()


if __name__ == '__main__':
    path_to_mp4_file = "/Users/evgeniy/Movies/Youtube/Dodkin's Job 1959 Джек Вэнс аудиокнига фантастика антиутопия юмор сатира рассказ будущее.mp4"
    path_to_image = "/Users/evgeniy/Downloads/KSP_016683_00015_1h.jpg"
    add_cover_to_file(path_to_mp4_file, path_to_image)
