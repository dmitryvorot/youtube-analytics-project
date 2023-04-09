import json
import os

from googleapiclient.discovery import build


class Channel:
    """
    Класс для ютуб-канала.
    """
    api_key = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """
        Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API.
        """
        self.__channel_id = channel_id
        self.get_attributes()

    def __str__(self):
        return f'{self.title} ({self.url})'

    @property
    def channel_id(self):
        """
        Возвращает id канала.
        """
        return self.__channel_id

    def print_info(self) -> None:
        """
        Выводит в консоль информацию о канале.
        """
        channel = self.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        """
        Возвращает объект для работы с YouTube API.
        """
        return cls.youtube

    def get_attributes(self):
        """
        Метод возвращает все необходимые атрибуты.
        """
        channel = self.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        json_str_data = json.dumps(channel, indent=2, ensure_ascii=False)
        py_dict_data = json.loads(json_str_data)

        self.__channel_id = py_dict_data['items'][0]['id']
        self.title = py_dict_data['items'][0]['snippet']['title']
        self.description = py_dict_data['items'][0]['snippet']['description']
        self.url = py_dict_data['items'][0]['snippet']['thumbnails']['default']['url']
        self.subscriberCount = int(py_dict_data['items'][0]['statistics']['subscriberCount'])
        self.video_count = int(py_dict_data['items'][0]['statistics']['videoCount'])
        self.viewCount = int(py_dict_data['items'][0]['statistics']['viewCount'])

        return self.__channel_id, self.title, self.description, self.url, self.subscriberCount, self.video_count, self.viewCount

    def to_json(self, file_name):
        """
        Метод сохраняет в file_name значение атрибутов экземпляра Channel.
        """
        with open(file_name, 'w') as file:
            json.dump(self.get_attributes(), file)

    def __add__(self, other) -> int:
        """
        Метод складывает количество подписчиков.
        """
        if isinstance(other, Channel):
            return self.subscriberCount + other.subscriberCount
        else:
            raise TypeError

    def __sub__(self, other) -> int:
        """
        Метод вычитает из количества подписчиков self количество подписчиков other.
        """
        if isinstance(other, Channel):
            return self.subscriberCount - other.subscriberCount
        else:
            raise TypeError

    def __gt__(self, other) -> bool:
        """
        Метод сравнивает количество подписчиков с помощью оператора ">"
        """
        if isinstance(other, Channel):
            return self.subscriberCount > other.subscriberCount
        else:
            raise TypeError

    def __ge__(self, other) -> bool:
        """
        Метод сравнивает количество подписчиков с помощью оператора ">="
        """
        if isinstance(other, Channel):
            return self.subscriberCount >= other.subscriberCount
        else:
            raise TypeError

    def __lt__(self, other) -> bool:
        """
        Метод сравнивает количество подписчиков с помощью оператора "<"
        """
        if isinstance(other, Channel):
            return self.subscriberCount < other.subscriberCount
        else:
            raise TypeError

    def __le__(self, other) -> bool:
        """
        Метод сравнивает количество подписчиков с помощью оператора "<="
        """
        if isinstance(other, Channel):
            return self.subscriberCount <= other.subscriberCount
        else:
            raise TypeError

    def __eq__(self, other) -> bool:
        """
        Метод сравнивает количество подписчиков с помощью оператора "=="
        """
        if isinstance(other, Channel):
            return self.subscriberCount <= other.subscriberCount
        else:
            raise TypeError

# id канала                        channel_id          id
# название канала                  title               title
# описание канала                  description         description
# ссылка на канал                  url                 url
# количество подписчиков           subscriberCount     subscriberCount
# количество видео                 video_count         videoCount
# общее количество просмотров      viewCount           viewCount
