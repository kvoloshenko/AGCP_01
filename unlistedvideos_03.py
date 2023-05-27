'''

В этой версии кода мы заменили ссылку на страницу видеофайлов на YouTube канале
на https://www.youtube.com/videos/unlisted, которая показывает только unlisted видео.
Мы также изменили генерацию ссылки для каждого видео на формат https://youtu.be/{video_id},
используя уникальный идентификатор видео, который можно получить из URL-адреса на YouTube.

'''
import requests
from bs4 import BeautifulSoup

# Запросить у пользователя url для канала на youtube.com.
channel_url = input("Введите URL канала на YouTube: ")

# Найти на указанном канале все unlisted videos используюя автогенерацию и подбор ссылки.
unlisted_videos = []
for i in range(1, 1000):
    # Генерируем ссылку на следующий видеофайл
    video_url = channel_url + "/videos?view=46&sort=dd&shelf_id=3&page=" + str(i)

    # Попытка получить страницу
    try:
        page = requests.get(video_url)
    except:
        print("Не удалось получить доступ к странице: " + video_url)
        continue

    if page.status_code == 200:
        soup = BeautifulSoup(page.content, 'html.parser')

        # Поиск всех видео на странице
        videos = soup.find_all('a', {'class': 'yt-simple-endpoint style-scope ytd-grid-video-renderer'})

        # Выход из цикла, если на странице нет видео
        if len(videos) == 0:
            break

        # Проверка каждого видео на unlisted статус
        for video in videos:
            video_title = video.get('aria-label').replace('/', '-')
            video_link = 'https://youtu.be/' + video.get('href').split('=')[-1]
            video_info = video.find_next('yt-formatted-string', {'class': 'style-scope ytd-video-renderer'})
            video_desc = video_info.get_text().replace('\n', '').replace('|', '')

            if 'unlisted' in video_desc.lower():
                unlisted_videos.append((video_title, video_link, video_desc))

    else:
        print("Страница недоступна: " + video_url)

# Информацию о найденном видео, его url и описание вывести на экран
for video in unlisted_videos:
    print("Заголовок: " + video[0])
    print("Ссылка: " + video[1])
    print("Описание: " + video[2])
    print("")

# Сохранить информацию в файл с именем unlistedvideos.txt
with open('unlistedvideos.txt', 'w') as f:
    for video in unlisted_videos:
        f.write(video[0] + '\n')
        f.write(video[1] + '\n')
        f.write(video[2] + '\n\n')