import pandas as pd
import json
import os


def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:  #читаем и возвращаем файл
        return json.load(file)

def process_one_file(file_path):
    data = load_json(file_path)  #обрабатываем один файл и возвращаем словарь с нужными полями
    realty_type_ID = data.get("characteristics_values",{}).get("1437","N/A")

    total_price_USD = data.get("priceArr",{}).get("2","N/A")
    square_meter_price_USD = data.get("priceItemArr",{}).get("2","N/A")
    characteristics_values = data.get("characteristics_values", {})
    credit = "YES" if "274" in characteristics_values else "NO"
    E_oselya = "YES" if "2001" in characteristics_values else "NO"
    #original_or_copy = "original" \
    if data.get("duplicate_copy"):
        original_or_copy = "original"
    elif data.get("duplicate_original"):
        original_or_copy ="copy"
    else:
        original_or_copy = "original"

    link_original_ID = data.get("duplicate_original"," ")

    return {
                 "realty_id": data.get("realty_id"),
                 "realty_type_ID" : realty_type_ID,
                 "original_or_copy" : original_or_copy,
                 "link_original_ID" : link_original_ID,
                 "total_price_USD" : total_price_USD,
                 "square_meter_price_USD" : square_meter_price_USD,
                 "credit" : credit,
                 "E_oselya" : E_oselya
            }

def process_all_files(input_folder):
    data_list = []
    for file in os.listdir(input_folder):  #формируем список названий из папки и если файл подходит под
        if file.endswith(".json"):       #json формат - выполняется ф-я process_one_file и данные добавляются
            file_path = os.path.join(input_folder, file)    # к data_list
            data_list.append(process_one_file(file_path))
    return data_list

def save_to_csv(data_list,output_folder, filename = "general_characteristics.csv"):
    if not os.path.exists(output_folder):   #переводим список в датафрейм и сохраняем без индекса
        os.makedirs(output_folder)
    df = pd.DataFrame(data_list)
    df.to_csv(os.path.join(output_folder,filename), index=False, encoding="utf-8-sig")

input_folder = "All_Apartment_Dnipro"
output_folder = "data"

data_list = process_all_files(input_folder)
save_to_csv(data_list, output_folder)