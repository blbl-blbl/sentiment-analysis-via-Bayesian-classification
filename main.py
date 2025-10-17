from html_processing import html_proc
from get_html import parse



def main():
    file_path = 'input.txt' # путь к файлу откуда будут считываеться id компаний
    with open(file_path, 'r') as file:
        ids = [line.strip() for line in file if line.strip()]  # убираем пробелы и пустые строки

    for id in ids:
        parse(id)

    html_proc()
    print("Процесс завершен")


if __name__=='__main__':
    main()
