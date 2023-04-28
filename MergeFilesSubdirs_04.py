import os
import codecs
# Вывод инструкции для пользователя
print("Программа для конвертации текстовых файлов из кодировки utf-8 в кодировку koi8-r")
# Получение пути к папке с файлами от пользователя
directory = input("Введите путь к папке с файлами: ")
# Получение названия выходного файла от пользователя
output_file_name = input("Введите название выходного файла: ")
# Список расширений файлов, которые нужно пропустить
skip_extensions = [".json", ".proto", ".sql", ".xml", ".desc"]
# Открытие выходного файла для записи
with open(output_file_name, "w") as output_file:
    # Перебор всех файлов в папке
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Получение пути к файлу
            file_path = os.path.join(root, file)
            # Проверка расширения файла
            if os.path.splitext(file_path)[1] in skip_extensions:
                continue
            # Открытие файла для чтения
            with codecs.open(file_path, "r", encoding="utf-8", errors="ignore") as input_file:
                # Чтение содержимого файла
                content = input_file.read()
                # Получение имени файла
                file_name = os.path.basename(file_path)
                print(f"{file_path}\{file_name}")
                # Конвертация содержимого файла из utf-8 в koi8-r
                converted_content = content.encode("koi8-r", errors="ignore").decode("koi8-r", errors="ignore")
                # Запись в выходной файл
                output_file.write(f" File name: {file_name}, Path: {file_path}")
                output_file.write(converted_content)
                output_file.write("")
# Вывод пути к выходному файлу
print(f"Выходной файл создан по пути: {os.path.abspath(output_file_name)}")