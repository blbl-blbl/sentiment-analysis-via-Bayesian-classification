from bs4 import BeautifulSoup
import re
import csv
import glob
import os

def html_proc(file_pattern=None):
    """
    Проходит по всем txt файлам и собирает нужную информацию
    :param file_pattern: путь к папке где хранятся txt файлы
    :return: csv файл
    """

    if file_pattern is None:
        file_pattern = "./htmls/*.txt"

    # Получаем список файлов, соответствующих шаблону
    files = glob.glob(file_pattern)



    # Читаем каждый файл
    for file_path in files:
        with open(file_path, "r", encoding="utf-8") as file:
            html_content = file.read()

            # Создание объекта BeautifulSoup
            soup = BeautifulSoup(html_content, "html.parser")

            # Название компании
            company_name = soup.find('h1', class_="orgpage-header-view__header").text.strip()

            # базовый путь
            path = soup.find("div", class_="card-reviews-view _wide")

            # Путь для сбора итогового рейтинга компании и числа оценок
            summary_rating_path = path.find("div", class_="business-summary-rating-badge-view__rating-and-stars")

            # Сбор итогового рейтинга
            try:
                summary_rating = summary_rating_path.find('div', class_='business-rating-badge-view__stars')
                rating_text = summary_rating.get('aria-label')
                rating_number = re.search(r'\d+\.\d+', rating_text).group()
                # rating_number = re.search(r'Оценка (\d+\.\d+) Из', rating_text)
            except:
                rating_number = None
                print(f"Рейтинг для компании {company_name} не найден")


            # Сбор количества оценок
            try:
                number_of_ratings = summary_rating_path.find('span', class_='business-rating-amount-view _summary').text.strip()
                number_of_ratings, _ = number_of_ratings.split(" ", 1)
            except:
                number_of_ratings = None
                print(f"Количество оценок для компании {company_name} не найдено")


            reviews_block = path.find('div', class_="business-reviews-card-view__reviews-container")
            reviews_block = reviews_block.find_all('div', class_="business-review-view")

            authors = []
            titles = []
            ratings = []
            reviews = []
            dates = []


            for i in reviews_block:
                try:
                    # Сбор имен авторов
                    name = i.find('span', itemprop='name').text

                    # Сбор "Рангов" авторов
                    title = i.find('div', class_="business-review-view__author-caption").text

                    # Сбор оценок в отзывах
                    rating = i.find('meta', {'itemprop': 'ratingValue'})
                    if rating:
                        rating = rating.get('content')

                    # Сбор дат когда был оставлен отзыв
                    date = i.find('span', class_="business-review-view__date").text

                    # Сбор текста отзыва
                    review = i.find('span', class_="spoiler-view__text-container").text

                    authors.append(name)
                    titles.append(title)
                    dates.append(date)
                    reviews.append(review)
                    ratings.append(rating)

                except:
                    continue

            # Проверяем, существует ли файл
            filename = "data.csv"
            file_exists = os.path.exists(filename)


            # Открываем файл в режиме добавления ('a') или записи ('w')
            with open('data.csv', 'a' if file_exists else 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                if file_exists:
                    for v1, v2, v3, v4, v5 in zip(authors, titles,dates, ratings, reviews):
                        writer.writerow([company_name, rating_number, number_of_ratings, v1, v2, v3, v4, v5])
                else:
                    writer.writerow([
                        "Компания",
                        "Итоговый рейтинг",
                        "Количество оценок",
                        "Имена авторов",
                        "Ранг автора",
                        "Дата отзыва",
                        "Рейтинг отзыва",
                        "Текст отзыва"
                    ])
                    for v1, v2, v3, v4, v5 in zip(authors, titles,dates, ratings, reviews):
                        writer.writerow([company_name, rating_number, number_of_ratings, v1, v2, v3, v4, v5])

