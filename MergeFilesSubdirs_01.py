# Merge files in subdirectories
# Напиши код на Python, код должен выполнять следующий сценарий:
# Запросить у пользователя файловый каталог,
# В цикле обойти все файлы в указанном файловом каталоге и подкаталогах.
# Для каждого файла добавить его содержимое в выходной файл указав к комментарии имя текущего файла.
# После окончания цикла вывести содержимое выходного файла.


import os

dir_path = input("Введите путь до файлового каталога: ")
output_file_path = "output.txt"

with open(output_file_path, "w") as output_file:
    for subdir, dirs, files in os.walk(dir_path):
        for file in files:
            file_path = os.path.join(subdir, file)
            with open(file_path, "r") as input_file:
                file_contents = input_file.read()
                output_file.write(f"=== {file_path} ===\n")
                output_file.write(file_contents + "\n")

with open(output_file_path, "r") as output_file:
    print(output_file.read())

# Пользователю предлагается ввести путь до файлового каталога. Затем используется функция os.walk для обхода всех файлов в указанном каталоге и подкаталогах. Для каждого файла открывается файловый поток на чтение, считывается содержимое файла, и имя файла добавляется в выходной файл в качестве комментария. После завершения цикла файлов выводится содержимое выходного файла на экран.
