# Merge files in subdirectories
# Напиши код на Python, код должен выполнять следующий сценарий:
# Запросить у пользователя файловый каталог и имя выходного файла
# В цикле обойти все файлы в указанном файловом каталоге и подкаталогах. Для каждого файла:
# 	Если текущий файл имеет расширение из списка: .json, .proto, .sql, .xml – тогда пропусти этот файл.
# 	Для иных файлов:
# Открой текущий файл, запомни его имя и путь, определи кодировку файла.
# Сконвертируй в koi8 кодировку содержимое текущего файла и добавить это содержимое в выходной файл указав к комментарии имя и путь текущего файла.
# После окончания цикла закрой выходной файл и сообщи полный путь к нему.
# Покрой сгенерированный код комментариями.

import os
import codecs

# Пользователь указывает файловый каталог и имя выходного файла
directory = input("Введите файловый каталог: ")
output_file_name = input("Введите имя выходного файла: ")

# Список расширений файлов, которые нужно пропустить
skip_extensions = [".json", ".proto", ".sql", ".xml", ".desc"]

# Открываем выходной файл на запись
with open(output_file_name, "w") as output_file:
    # Обходим все файлы в указанном каталоге и подкаталогах
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Получаем полный путь к текущему файлу
            file_path = os.path.join(root, file)
            # Если текущий файл имеет расширение из списка skip_extensions, тогда пропускаем его
            if os.path.splitext(file_path)[1] in skip_extensions:
                continue

            # Открываем текущий файл
            with codecs.open(file_path, "r", encoding="utf-8", errors="ignore") as input_file:
                # Получаем содержимое текущего файла
                content = input_file.read()
                # Получаем имя текущего файла
                file_name = os.path.basename(file_path)
                # Конвертируем содержимое текущего файла в koi8 кодировку
                converted_content = content.encode("koi8-r", errors="ignore").decode("koi8-r", errors="ignore")
                # Добавляем содержимое в выходной файл
                output_file.write(f"# File name: {file_name}, Path: {file_path}\n")
                output_file.write(converted_content)
                output_file.write("\n\n")

# Выводим полный путь к выходному файлу
print(f"Выходной файл создан по пути: {os.path.abspath(output_file_name)}")

