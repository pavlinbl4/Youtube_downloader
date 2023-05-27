from pytube import Playlist


def playlists_links(playlist):
    links = Playlist(playlist)
    return links


if __name__ == '__main__':
    # playlist = 'https://youtube.com/playlist?list=PL65ijVzWl9ksD5m5fRrFIlbWX2fGD-wYg'
    my_playlist = 'https://music.youtube.com/playlist?list=PLA3BruVN0VUKZquOkBSwRpcCo36gh6ol8&feature=share'
    print(playlists_links(my_playlist))
