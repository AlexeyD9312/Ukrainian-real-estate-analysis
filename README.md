# Ukrainian-real-estate-analysis
Analysis of the real estate market of Ukraine based on data from the API site Domria
зберегти зміни 
URL = "https://developers.ria.com/dom/search"

params = {
    "api_key": API_KEY,
    "category":1,
    "operation":1,
    "stateID": 11,
    "city_id": 11,
    "page":0 #АПІ видає по 100ІД
}
response = requests.get(URL,params=params)
