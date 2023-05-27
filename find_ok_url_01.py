'''
Программа запрашивает у пользователя начальное и конечное значение переменной части,
затем проходит по всем возможным значениям переменной, формирует ссылку и проверяет ее.
Если ссылка работает (HTTP-код ответа 200), то она выводится на экран и добавляется в список рабочих ссылок.

После завершения цикла программа выводит количество найденных рабочих ссылок и список всех рабочих ссылок на экран.
Затем программа сохраняет этот список в файл working_links.txt в текущей директории.
В конце работы программа выводит на экран путь к файлу со списком рабочих ссылок.

'''

import requests

start_val = int(input("Введите начальное значение переменной части: "))
end_val = int(input("Введите конечное значение переменной части: "))

url_prefix = "https://lk.neural-university.ru/learning-program-v2/"
working_links = []

for i in range(start_val, end_val+1):
    url = url_prefix + str(i)
    response = requests.get(url)
    if response.status_code == 200:
        print(f"Рабочая ссылка: {url}")
        working_links.append(url)

print(f"Найдено рабочих ссылок: {len(working_links)}")
print("Список всех найденных рабочих ссылок:")
for link in working_links:
    print(link)

# Сохранение списка рабочих ссылок в файл
with open("working_links.txt", "w") as file:
    for link in working_links:
        file.write(link + "\n")

print("Список всех найденных рабочих ссылок сохранен в файле working_links.txt")