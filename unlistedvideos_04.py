'''
К сожалению, некоторые каналы YouTube могут ограничивать доступ к их unlisted видео только для определенных пользователей или групп пользователей. Если программа не может найти ни одной рабочей ссылки на unlisted видео, то это может быть связано с ограничениями доступа.
Однако, вы можете попробовать улучшить программу в части подбора ссылок, используя следующие методы:
Использование API. Вы можете использовать YouTube Data API, чтобы получить информацию об unlisted видео конкретного канала. Это может дать более точные и актуальные результаты, чем автоматическая генерация ссылок. Однако, для использования этого API требуется регистрация в Google Cloud Console и получение ключа API.
Изменение параметров поиска. Некоторые каналы могут использовать другие параметры для отображения своих unlisted видео вместо стандартных параметров, которые были использованы в первоначальной версии кода. Попробуйте изменять параметры запроса, такие как sort, shelf_id и view. Например, канал может использовать параметр shelf_id=4, чтобы отображать свои unlisted видео.
Изменение User-Agent. Некоторые каналы могут блокировать запросы от программных ботов, используя User-Agent в HTTP-запросе. Попробуйте изменить User-Agent на что-то другое, чтобы обойти это ограничение.
Вот пример кода, который использует YouTube Data API для поиска unlisted видео на заданном канале:
'''

import google.auth
from googleapiclient.discovery import build

# Установить параметры аутентификации
credentials, project = google.auth.default(
    scopes=['https://www.googleapis.com/auth/youtube.force-ssl'])

youtube = build('youtube', 'v3', credentials=credentials)

# Запросить у пользователя имя (или ID) канала на youtube.com.
channel_name = input("Введите имя или ID канала на YouTube: ")

# Получить информацию о канале
channel_request = youtube.channels().list(part='snippet,contentDetails', forUsername=channel_name)
response = channel_request.execute()

if len(response['items']) == 0:
    channel_request = youtube.channels().list(part='snippet,contentDetails', id=channel_name)
    response = channel_request.execute()

if len(response['items']) == 0:
    print("Канал не найден.")
else:
    channel = response['items'][0]
    channel_id = channel['id']

    # Получить все видео канала
    videos = []
    next_page_token = ''
    while next_page_token is not None:
        playlist_request = youtube.playlistItems().list(
            part="snippet",
            playlistId=channel['contentDetails']['relatedPlaylists']['uploads'],
            maxResults=50,
            pageToken=next_page_token
        )
        playlist_response = playlist_request.execute()

        for item in playlist_response['items']:
            videos.append(item)

        next_page_token = playlist_response.get('nextPageToken')

    # Получить информацию о каждом видео
    unlisted_videos = []
    for video in videos:
        video_id = video['snippet']['resourceId']['videoId']
        video_request = youtube.videos().list(
            part="snippet",
            id=video_id
        )
        video_response = video_request.execute()

        if len(video_response['items']) == 0:
            continue

        video_data = video_response['items'][0]['snippet']
        video_title = video_data['title'].replace('/', '-')
        video_link = 'https://youtu.be/' + video_id
        video_desc = video_data.get('description', '')

        if 'unlisted' in video_desc.lower():
            unlisted_videos.append((video_title, video_link, video_desc))

    # Вывести информацию о найденных unlisted видео
    for video in unlisted_videos:
        print(video_title, video_link, video_desc)