import os
import time
import requests
import json


API_KEY = "tBpXw0JFJHFL5gbyB0h1WP6ax6ZpmtnjhsQrVXgf"  #задаем параметры
BASE_URL = "https://developers.ria.com/dom/info/"
list_ID_file = "All_ID_Dnipro"
save_folder = "All_apartment_Dnipro"
req_interval = 8

os.makedirs(save_folder,exist_ok=True)#создаем папку в репозитории

#пишем функцию для чтения айди из файла
def read_all_ID(file_path):
    try:
        with open(file_path,"r",encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error, not found file")
        return []
    except json.JSONDecodeError:
        print("Error, format file")
        return []

#функция запроса к апи
def api_request(object_ID):
    url = f"{BASE_URL}{object_ID}"
    params = {"api_key": API_KEY}

    try:
        response = requests.get(url,params=params,timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error is {object_ID}:{e}")
        return None

#функция saved json file
def save_json(data,index,object_ID):
    filename = f"{str(index).zfill(4)}_{object_ID}.json"
    file_path = os.path.join(save_folder,filename)

    with open(file_path,"w",encoding="utf-8") as f:
        json.dump(data,f,ensure_ascii=False,indent=4)

# main cycle
def main():
    object_ids = read_all_ID(list_ID_file)
    total_obj = len(object_ids)

    if not object_ids:
        print("Not ID. STOP ")
        return
    print(f"have {total_obj} ID. Start load file")

    for index, object_ID in enumerate(object_ids,start=1):
        print(f"[{index}/{total_obj}] Load for ID {object_ID}")

        data = api_request(object_ID)
        if data:
            save_json(data, index, object_ID)
            print(f"Data saved : {index:04d}_{object_ID}.json")
        else:
            print(f"Error request:{object_ID}")

        if index<total_obj:
            print(f"pause before next request")
            time.sleep(req_interval)
    print("All file is load")

if __name__ == "__main__":
    main()





