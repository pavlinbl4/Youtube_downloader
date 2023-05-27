from pytube import YouTube

def get_title(link):
    yt = YouTube(link)
    print(yt.keywords)
    print(yt.title)



if __name__ == '__main__':
    get_title("https://www.youtube.com/watch?v=d0ZuRK7Vg1U")
