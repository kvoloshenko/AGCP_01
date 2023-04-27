# Merge files in subdirectories
# Напиши код на Python, код должен выполнять следующий сценарий:
# Запросить у пользователя файловый каталог,
# В цикле обойти все файлы в указанном файловом каталоге и подкаталогах. Для каждого файла:
# Открой текущий файл, запомни его имя и путь, определи кодировку файла.
# Сконвертируй в koi8 кодировку содержимое текущего файла и добавить это содержимое в выходной файл указав к комментарии имя и путь текущего файла.
# После окончания цикла вывести содержимое выходного файла.
import os
import codecs


def convert_file(input_file, output_file):
    # определяем кодировку
    with open(input_file, 'rb') as f:
        raw_data = f.read()
        encoding = 'utf-8'
        try:
            decoded_data = raw_data.decode('utf-8')
        except UnicodeDecodeError:
            encoding = 'windows-1251'
            decoded_data = raw_data.decode(encoding)
        except:
            print(f"Unable to decode {input_file}")
            return False

    # конвертируем в koi8
    koi8_data = codecs.encode(decoded_data, 'koi8-r')

    # добавляем в выходной файл с комментарием
    with open(output_file, 'ab') as f:
        f.write(b"# " + input_file.encode() + b"\n")
        f.write(koi8_data)

    return True


def process_dir(input_dir, output_file):
    for root, dirs, files in os.walk(input_dir):
        for file_name in files:
            input_file_path = os.path.join(root, file_name)
            if convert_file(input_file_path, output_file):
                print(f"Processed {input_file_path}")


if __name__ == '__main__':
    input_dir = input("Enter input directory: ")
    output_file = "output.koi"

    # создаем пустой выходной файл
    open(output_file, 'wb').close()

    process_dir(input_dir, output_file)

    # выводим содержимое выходного файла
    with open(output_file, 'rb') as f:
        print(f.read().decode('koi8-r'))
