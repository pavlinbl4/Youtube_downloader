from pathlib import Path


def check_file(file):
    return Path(file).exists()


if __name__ == '__main__':
    file = '/Volumes/big4photo/Movies/YouTube/Roald Dahl Collection/Roald Dahl_Skin(Lewis Kirk).mp4'
    print(check_file(file))
