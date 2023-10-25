import os
import codecs
# Вывод инструкции для пользователя
print("Программа для конвертации текстовых файлов из кодировки utf-8 в кодировку koi8-r")
# Получение пути к папке с файлами от пользователя
directory = input("Введите путь к папке с файлами: ")
# Получение названия выходного файла от пользователя
output_file_name = input("Введите название выходного файла: ")
# Список расширений файлов, которые нужно пропустить
# skip_extensions = [".json", ".proto", ".sql", ".xml", ".desc"]
skip_extensions = [".proto", ".PNG", ".png", ".eot", ".xls"]

with open(output_file_name, "w") as output_file:
    for root, dirs, files in os.walk(directory):
        print(f'root={root}, dirs={dirs}, files={files}')
        for file in files:

            file_path = os.path.join(root, file)

            if os.path.splitext(file_path)[1] in skip_extensions:
                continue

            with codecs.open(file_path, "r", encoding="utf-8", errors="ignore") as input_file:

                content = input_file.read()

                file_name = os.path.basename(file_path)
                print(f"{file_path}\{file_name}")
                # utf - 8
                # koi8 - r
            converted_content = content.encode("koi8-r", errors="ignore").decode("koi8-r", errors="ignore")

            output_file.write(f" File name: {file_name}, Path: {file_path}")
            output_file.write(converted_content)
            output_file.write("")

# Вывод пути к выходному файлу
print(f"Выходной файл создан по пути: {os.path.abspath(output_file_name)}")