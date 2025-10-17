import time
import undetected_chromedriver as uc
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


def parse(company_id, company_name=None):

    if company_name is None:
        company_name = company_id


    url = f"https://yandex.ru/maps/org/{company_id}/reviews/"
    driver = None

    while driver is None:
        try:
            time.sleep(2)
            driver = uc.Chrome()
            driver.get(url)
        except:
            print("Возникла проблема с подключением \n Выполняю повторное подключение")

    time.sleep(2)

    try:
        # Находим элемент, внутри которого будем прокручивать
        scrollable_element = driver.find_element(By.CSS_SELECTOR, "div.scroll__scrollbar._noprint")
        slider = scrollable_element.find_element(By.CSS_SELECTOR, "div.scroll__scrollbar-thumb")

        # Создаем цепочку действий
        actions = ActionChains(driver)

        # 1. Кликаем и удерживаем ползунок
        # 2. Перемещаем его на ... пикселей вниз (x=0, y=кол-во пикселей)
        # 3. Отпускаем
        actions.click_and_hold(slider).move_by_offset(0, 700).release().perform()
    except:
        print("Ползунок не найден")


    time.sleep(2)
    html_content = driver.page_source
    time.sleep(5)

    # Сохранить в файл
    folder_path = os.path.join(os.path.dirname(__file__), "htmls", f"page_content_{company_id}_{company_name}.txt")

    with open(folder_path, "w", encoding="utf-8") as file:
        file.write(html_content)


    driver.close()
    driver.quit()





