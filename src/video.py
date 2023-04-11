import os

from googleapiclient.discovery import build


class Video:
    api_key = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, video_id):
        """
        Экземпляр инициализируется по id видео. Дальше все данные будут подтягиваться по API.
        """
        self.video_id = video_id
        self.title, self.url, self.view_count, self.like_count = self.get_attributes()

    def __str__(self):
        return self.title

    def get_attributes(self):
        """
        Метод возвращает все необходимые атрибуты.
        """
        video = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                           id=self.video_id).execute()

        self.title = video['items'][0]['snippet']['title']
        self.url = video['items'][0]['snippet']['thumbnails']['default']['url']
        self.view_count = video['items'][0]['statistics']['viewCount']
        self.like_count = video['items'][0]['statistics']['likeCount']

        return self.title, self.url, self.view_count, self.like_count


class PLVideo:
    api_key = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, video_id, playlist_id):
        """
        Экземпляр инициализируется по id видео и id плейлиста. Дальше все данные будут подтягиваться по API.
        """
        self.video_id = video_id
        self.playlist_id = playlist_id
        self.title, self.url, self.view_count, self.like_count = self.get_attributes()

    def __str__(self):
        return self.title

    def get_attributes(self):
        """
        Находит плейлист по playlist_id, если в нем есть видео с необходимым video_id -> необходимые атрибуты.
        """
        video_playlist = self.youtube.playlistItems().list(playlistId=self.playlist_id,
                                                           part='contentDetails',
                                                           maxResults=50,
                                                           ).execute()

        video = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                           id=self.video_id).execute()

        for i in video_playlist['items']:
            if i['contentDetails']['videoId'] == self.video_id:
                self.title = video['items'][0]['snippet']['title']
                self.url = video['items'][0]['snippet']['thumbnails']['default']['url']
                self.view_count = video['items'][0]['statistics']['viewCount']
                self.like_count = video['items'][0]['statistics']['likeCount']

                return self.title, self.url, self.view_count, self.like_count
