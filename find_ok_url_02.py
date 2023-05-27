"""
При запуске программы пользователь должен будет ввести начальное и конечное значения переменной части.
Затем программа будет проходить в цикле по всем значениям переменной части,
формировать ссылки и отправлять GET запросы с данными для авторизации.
Если полученный ответ имеет статус код 200 и не содержит текста "error 404",
то ссылка считается рабочей и добавляется в список.
В конце работы программа выводит список всех найденных рабочих ссылок и сохраняет его в файл 'working_links.txt'.
"""
import requests

# задаем начальное и конечное значения переменной части
start_value = int(input("Введите начальное значение: "))
end_value = int(input("Введите конечное значение: "))

# задаем постоянную часть ссылки
base_url = "https://lk.neural-university.ru/learning-program-v2/"

# задаем данные для авторизации
login_name = "change_name"
password = "12345"


# список для хранения рабочих ссылок
working_links = []

# проходим в цикле по всем значениям переменной части
for i in range(start_value, end_value + 1):
    # формируем ссылку
    url = base_url + str(i)

    # отправляем GET запрос с данными для авторизации
    response = requests.get(url, auth=(login_name, password))
    print(response.text)

    # проверяем, что ответ получен успешно и в теле страницы нет текста "error 404"
    if response.status_code == 200 and "error 404" not in response.text:
        # добавляем рабочую ссылку в список
        working_links.append(url)

        # выводим рабочую ссылку на экран
        print("Рабочая ссылка:", url)

# выводим список всех найденных рабочих ссылок
print("Все рабочие ссылки:")
for link in working_links:
    print(link)

# сохраняем список рабочих ссылок в файл
with open("working_links.txt", "w") as file:
    for link in working_links:
        file.write(link + "\n")
print("Список рабочих ссылок сохранен в файле 'working_links.txt'")