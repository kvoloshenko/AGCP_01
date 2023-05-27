'''
Напиши код на Python, код должен выполнять следующий сценарий:
Запросить у пользователя url для канала на youtube.com.
В цикле найти все ссылки на видео с этого канала с учетом того, что видео доступно только по ссылке.
Информацию о найденном видео, его url и описание вывести на экран и сохранить в файл с именем youtube_urls.txt
Покрой сгенерированный код комментариями.
----

Библиотека requests используется для получения содержимого страниц,
а библиотека BeautifulSoup - для разбора html-кода страницы и поиска нужных элементов.
Сначала мы запрашиваем у пользователя url канала на YouTube и создаем файл для записи найденных ссылок.
Затем мы получаем страницу канала, находим все ссылки на видео с помощью поиска элементов с определенным
классом yt-uix-tile-link.
Далее мы проходим циклом по списку найденных ссылок, получаем информацию о каждом видео
(его заголовок, url и описание) и выводим эту информацию на экран, и записываем
в созданный файл.
Если на данном канале нет видео, то выводим соответствующее сообщение.
'''
import requests
from bs4 import BeautifulSoup

# Запрашиваем у пользователя url канала на YouTube
channel_url = input("Введите url канала на YouTube: ")

# Создаем текстовый файл для записи ссылок
with open("youtube_urls.txt", "w") as file:
    # Получаем страницу канала
    r = requests.get(channel_url)
    soup = BeautifulSoup(r.content, "html.parser")

    # Находим все ссылки на видео с канала
    video_links = soup.find_all("a", {"class": "yt-uix-tile-link"})

    # Проверяем, что список ссылок не пустой
    if len(video_links) > 0:
        # Проходим циклом по списку ссылок на видео
        for video_link in video_links:
            # Получаем информацию о видео: его заголовок и описание
            video_title = video_link.get("title")
            video_url = "https://www.youtube.com" + video_link.get("href")
            video_r = requests.get(video_url)
            video_soup = BeautifulSoup(video_r.content, "html.parser")
            video_description = video_soup.find("p", {"id": "eow-description"}).text.strip()

            # Выводим информацию о найденном видео на экран
            print(f"{video_title} ({video_url})")
            print(f"    {video_description}")

            # Записываем информацию о найденном видео в текстовый файл
            file.write(f"{video_title} ({video_url})\n")
            file.write(f"    {video_description}\n")

    else:
        print("Видео на этом канале не найдено")



