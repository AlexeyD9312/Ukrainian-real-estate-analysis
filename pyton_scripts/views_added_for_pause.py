import pandas as pd
import json
import os
import time
import threading
import random
from Lib.views_added_scrapp import start_index


from selenium import webdriver  # основной модуль управления браузером
from selenium.webdriver.chrome.service import Service  # запуск chrome webdriver
from selenium.webdriver.chrome.options import Options  # Настройка параметров браузера
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager  # Автоматическая установка драйверов на Хром
from bs4 import BeautifulSoup

BASE_URL = "https://dom.ria.com/uk/"
input_folder = "All_Apartment_Dnipro"
output_folder = "data"
output_filename = "views_added_2001_to_3000.csv"

start_number = 2001
end_number = 3000


class DomRiaScrapper:
    def __init__(self, headless=True):  # инициализация selenium  webdriver работы браузера в фоновом режиме
        options = Options()
        if headless:
            options.add_argument("--headless")  # без интерфейса
        options.add_argument("--disable-gpu")  # откл граф рендинга
        options.add_argument("--no-sandbox")  # откл песочницы
        options.add_argument("--disable-dev_shm-usage")  # оптимизация памяти

        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")  # Убираем флаг webdriver
        self.driver.set_page_load_timeout(20)
        self.driver.set_script_timeout(10)
        self.driver.implicitly_wait(5)
        self.errors_in_row = 0

    def restart_driver(self):
        print("Chrome restart")
        self.close()
        time.sleep(2)

        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")  # откл граф рендинга
        options.add_argument("--no-sandbox")  # откл песочницы
        options.add_argument("--disable-dev_shm-usage")  # оптимизация памяти

        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")  # Убираем флаг webdriver
        self.driver.set_page_load_timeout(20)
        self.driver.set_script_timeout(10)
        self.driver.implicitly_wait(5)


    def get_view_added(self, url, max_retries=2, timeouth = 10):
        retries = 0
        while retries < max_retries:
            try:
                self.driver.get(url)

                time.sleep(random.uniform(2,5))


                soup = BeautifulSoup(self.driver.page_source, "html.parser")

                views, added = "0", "0"

                for item in soup.find_all("li", class_="item"):
                    text = item.get_text(strip=True)
                    if "Переглядів" in text:
                        views = text.replace("Переглядів", "").strip()
                    elif "Збережень в обране" in text:
                        added = text.replace("Збережень в обране", "").strip()

                self.errors_in_row = 0
                return views, added

            except Exception as e:
                retries += 1
                self.errors_in_row +=1
                print(f"Error {url}, retri {retries}/{max_retries} - {e}")
                time.sleep(0.5)

               # if self.errors_in_row >=3:
                #    self.restart_driver()
                #    self.errors_in_row = 0

        print(f"Not Download {url} !!!!!!!!!!!")
        return "N/A", "N/A"

    def close(self):
        self.driver.quit()


class JSONProcessor:

    @staticmethod
    def load_json(file_path):  # параметр file_path путь к файлу
        with open(file_path, "r", encoding="utf-8") as file:  # читаем и возвращаем файл в виде словаря
            return json.load(file)

    def process_file(self, file_path, scraper):
        data = self.load_json(file_path)
        realty_id = data.get("realty_id")
        beautiful_url = data.get("beautiful_url")
        full_url = BASE_URL + beautiful_url if beautiful_url else "N/A"
        photos_count = len(data.get("photos", {}))
        created_at = data.get("created_at", "N/A")
        youtube_link = "YES" if data.get("youtube_link") else "NO"
        views, added = scraper.get_view_added(full_url) if beautiful_url else ("N/A", "N/A")

        return {
            "realty_id": realty_id,
            "beautiful_url": full_url,
            "photos_count": photos_count,
            "youtube_link": youtube_link,
            "created_at": created_at,
            "views": views,
            "added": added
        }


class DataSaved:
    @staticmethod
    def save_to_csv(data_list, output_folder, filename):
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        df = pd.DataFrame(data_list)
        output_file = os.path.join(output_folder, filename)

        if os.path.exists(output_file):
            df.to_csv(output_file, mode="a", index=False, encoding="utf-8-sig", header=False)
        else:
            df.to_csv(output_file, index=False, encoding="utf-8-sig")
        print(f"Download  {len(data_list)} in {output_file}")-


class GeneralLine:
    def __init__(self, input_folder, output_folder, start_number, end_number, filename):
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.filename = filename
        self.start_number = start_number
        self.scraper = DomRiaScrapper()
        self.processor = JSONProcessor()
        self.saver = DataSaved()
        self.end_number = end_number

    def process_files(self, files):
        results = []

        for file in files:

            print(f"Processing {file}")
            result = self.processor.process_file(file, self.scraper)
            results.append(result)

        if results:
            self.saver.save_to_csv(results, self.output_folder, self.filename)


    def run(self):
        files = sorted(
            [os.path.join(self.input_folder, file)
             for file in os.listdir(self.input_folder)
             if file.endswith(".json") and file[:4].isdigit()
             and self.start_number <= int(file[:4]) <= self.end_number])

        if not files:
            print(f"no Files {self.start_number} - {self.end_number} ")
            return

        print(f"procesing {len(files)} from {self.start_number} - {self.end_number} ")
        self.process_files(files)
        self.scraper.close()
        print("Processing Complete")


if __name__ == "__main__":
    start_number = 2001
    end_number = 3000
    output_filename = "views_added_2001_to_3000.csv"
    genline = GeneralLine(input_folder, output_folder,  start_number, end_number, output_filename)
    genline.run()
