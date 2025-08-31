from pytube import Playlist

def get_playlist_thumbnail(playlist_url):
    pl = Playlist(playlist_url)
    first_video_url_id = pl.video_urls[0].split("=")[1]
    return f"https://img.youtube.com/vi/{first_video_url_id}/0.jpg", first_video_url_id
