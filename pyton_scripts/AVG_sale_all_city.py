import pandas as pd
import requests
import json
from  datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import time
import os


def resp_data(api_key, params):
    URL = "https://developers.ria.com/dom/average_price"
    params["api_key"] = api_key
    response = requests.get(URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error {response.status_code}")
        return None


def collect_one_city_data(city_id,api_key,squares,pause,start_date,end_date):
    data = []
    current_date = start_date
    while current_date < end_date:
        next_date = current_date + relativedelta(months=1)
        date_from_str = current_date.strftime("%Y-%m-%d")
        date_to_str = next_date.strftime("%Y-%m-%d")

        params = {

            "category": 1,
            "sub_category": 2,
            "operation": 1,
            "city_id": city_id,
            "date_from": date_from_str,
            "date_to": date_to_str
        }
        results = resp_data(api_key, params)
        time.sleep(pause)

        if results:
            count_apartments = results.get("total", 0)
            avg_apartment_price = results.get("arithmeticMean", 0)
            row = [date_from_str, date_to_str, count_apartments, avg_apartment_price]
            total_price_avg_sqm = 0

            for sqm in squares:
                params["square"] = sqm
                results = resp_data(api_key, params)
                time.sleep(pause)

                if results:
                    price_per_sqm = results.get("arithmeticMean", 0) / sqm
                else:
                    price_per_sqm = 0
                row.append(price_per_sqm)
                total_price_avg_sqm += price_per_sqm

            avg_sqm_price = total_price_avg_sqm / len(squares)
            row.append(avg_sqm_price)
            data.append(row)

            print(f"Закончена обработка {city_id} периода:{date_from_str} - {date_to_str}")
        else:
            print(f"NoN date for {city_id} периода:{date_from_str} - {date_to_str}")

        current_date = next_date
    return data


def collection_all_cities_data(api_key,city_ids,squares,pause,start_date,end_date):
    for city_id in city_ids:
        print(f"begin work with {city_id}")
        data = collect_one_city_data(city_id,api_key,squares,pause,start_date,end_date)
        os.makedirs("city_apart_price", exist_ok=True)
        file_name = f"city_apart_price/AVG_price_city_{city_id}.csv"
        columns = ["date_from","date_to","count","avg_price"] + [f"price_per_sqm_{sqm}" for sqm in squares] + ["avg_sqm_price"]
        df = pd.DataFrame(data, columns=columns)
        df.to_csv(file_name,encoding="utf-8", index=False)
        print(f"закончено обработку для города {city_id}")


api_key = "tBpXw0JFJHFL5gbyB0h1WP6ax6ZpmthsQrVXgf"
city_ids = [7,8,9,10,12,14,15,16,18,19,20,22,23,24,25]
start_date = datetime(2017,6,1)
end_date = datetime(2025,3,1)
squares = [40,50,60,70,80,90,100]
pause = 2.5

collection_all_cities_data(api_key, city_ids, squares, pause, start_date, end_date)



