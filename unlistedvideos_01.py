'''
Напиши код на Python, код должен выполнять следующий сценарий:
Запросить у пользователя url для канала на youtube.com.
Найти на указанном канале все unlisted videos.
Информацию о найденном видео, его url и описание вывести на экран и сохранить в файл с именем unlistedvideos.txt
Покрой сгенерированный код комментариями.
'''
# Импортируем необходимые библиотеки
import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

# Спрашиваем у пользователя url канала
url = input("Введите url канала на Youtube: ")

# Устанавливаем переменные среды
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

# Определяем области, которые нужно получить от API
scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

# Запускаем авторизацию и создаем объект api
api_service_name = "youtube"
api_version = "v3"
client_secrets_file = "client_secret.json"

# Авторизуемся и создаем объект api
flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    client_secrets_file, scopes)
credentials = flow.run_console()
youtube = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)

# Определяем запрос для получения всех видео на канале
request = youtube.channels().list(
        part="contentDetails",
        id=url.split("/")[-1],
        maxResults=1
    )

# Получаем идентификатор списка видео из ответа на запрос
response = request.execute()
playlist_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

# Определяем запрос для получения всех видео на канале
next_page_token = None
videos = []
while True:
    request = youtube.playlistItems().list(
            part="snippet",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        )
    response = request.execute()

    # Проверка наличия видео с ограниченным доступом
    for video in response['items']:
        if video['snippet']['title'].startswith("Private video") \
                or video['snippet']['privacyStatus'] == "unlisted":

            # Выводим информацию о видео на экран
            print(video['snippet']['title'])
            print("https://www.youtube.com/watch?v=" + video['snippet']['resourceId']['videoId'])
            print(video['snippet']['description'])

            # Добавляем информацию в список
            videos.append({
                'title': video['snippet']['title'],
                'url': "https://www.youtube.com/watch?v=" + video['snippet']['resourceId']['videoId'],
                'description': video['snippet']['description']
            })

    # Если больше нет видео, то выходим из цикла
    if 'nextPageToken' not in response:
        break

    next_page_token = response['nextPageToken']

# Сохраняем информацию о видео в файл
with open("unlistedvideos.txt", "w", encoding="utf-8") as f:
    for video in videos:
        f.write(video['title'] + "\n")
        f.write(video['url'] + "\n")
        f.write(video['description'] + "\n\n")

# Выводим сообщение об успешном сохранении информации в файл
print("Информация сохранена в файл unlistedvideos.txt")
