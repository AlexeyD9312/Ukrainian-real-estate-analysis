# Аналіз ринку нерухомості України
## Цілі проекту
Аналіз  риноку житлової нерухомості України. Дослідити динаміку цін та кількості пропозицій на ринку за останні 7 років. Оцінити стан ринку на даний момент. Розглянути інвестиційну привабливість нерухомості в Украіні. Дослідити, на прикладі м.Дніпро, яка саме нерухомість найбільш цікава покупцям на даний момент.

## Опис проекту
Основним джерелом данних для нас буде слугувати найбільший та найпоширеніший сайт з продажу нерухомості в Україні - DIM.RIA. Використовуючи API сайту, та  парсинг HTML сторінки, будемо проводити збір та очищення данних  за допомогою Python. Зберігання та сортування данних буде проходити у реляційній базі даних MySQL, візуалізація та аналіз у PowerBi.
## Структура проекту
В основному описі проекту для прикладу будуть наведені  частини скриптів, JSON файлів та інших даних, які будуть посилатись на файли всередині репозиторію. Для більш детального розбору коду,змісту та структури файлу, можна буде перейти за посилянням.
## Збір даних.
Перша частина нашої роботи передбачає обробку середньої ціни нерухомості по містам України. Витягувати ці дані ми будемо за допомогою API DIM.RIA, використовуючі Python, бібліотеку Request. Обов'язково ознайомлюємося з документацією АПІ, обираємо потрібні нам параметри та робимо запит. Наведемо приклад. [Основний код](./pyton_scripts/AVG_sale_all_city.py)
```python URL = "https://developers.ria.com/dom/average_price"
    params["api_key"] = api_key
    params = {

            "category": 1,
            "sub_category": 2,
            "operation": 1,  #3 rent
            "city_id": city_id,
            "date_from": date_from_str,
            "date_to": date_to_str
        }
    city_ids = [1,2,3,4,5,6,7,8,9,10,12,14,15,16,18,19,20,22,23,24,25]
    start_date = datetime(2017,6,1)
    end_date = datetime(2025,3,1)
    squares = [40,50,60,70,80,90,100]
    pause = 2.5
```

Це частина стандартнго запиту, в якому вказані параметри, ключ та URL. Відповідь буде дана у вигляді JSON файлу, з зазначеною вартістю нерухомості та кількістю об'єктів. Це корисна інформація, але для оцінку вартості нерухомості дуже важливо мати ціну за 1 квадратний метр. Тому ми будемо окремо робити запити на кожну задану площу(була взята вибірка найбільш популярних площ квартир).У подальшому отримана ціна  буде поділена на площу вказану у запиті. Це дозволить в кінці вирахувати середню вартість за метр, по кожному місту, в діапазоні заданих дат. Категорії відповідають за тип нерухомості - це житлова нерухомість, саме квартири.
Операція - продаж. Також додаємо дату початку та дату кінця дослідження, інтервал запиту - 1 місяць. Формуємо список з ID міст.  Та не забуваємо про паузи між запитами, адже даний сервіс має обмеження в 2000 запитів на годину.
В кінці, за допомогою бібліотеки Pandas, ми отримаємо наступний CSV файл по кожному місту.[Приклад файлу](./data/AVG_price_city_Kiyiv.csv)
```md
date_from,date_to,count,avg_price,price_per_sqm_40,price_per_sqm_50,price_per_sqm_60,price_per_sqm_70,price_per_sqm_80,price_per_sqm_90,price_per_sqm_100,avg_sqm_price
2017-06-01,2017-07-01,8284,1672774.839,24214.65925,28272.2508,26614.31016666667,27673.896285714287,29450.26125,31995.345555555556,34031.413,28893.162329705217
2017-07-01,2017-08-01,9492,1731265.93,24547.8005,26873.3816,27993.105833333335,27673.896285714287,33704.187875,31995.345555555556,35917.3081,29815.003678514742
2017-08-01,2017-09-01,9594,1679586.35,24547.8005,26455.03,28105.902250000003,27316.34942857143,33168.7585625,38759.685,39417.9947,31110.217205867346
2017-09-01,2017-10-01,8913,1617250.8,24140.214874999998,26415.096400000002,27777.7815,26077.101000000002,33876.788062499996,39682.545000000006,36772.4917,30677.43121964286
2017-10-01,2017-11-01,4417,1617250.8,23584.9075,25471.7001,26504.94366666667,26184.06057142857,34366.5795,36238.39755555556,34097.0377,29492.518084807256
2017-11-01,2017-12-01,5473,1532033.25,26462.392499999998,28969.355999999996,25301.761249999996,25069.635,33600.274687499994,27700.399166666666,36944.285445,29149.729149880954
```

Такий самий запит повторимо і по аренді, але без запитів по квадратних метрах. Для нашого дослідження цього буде достатньо. Також додатково додаємо дані курсу валют, а саме гривні до доллару, за весь період дослідження, для відображення цін на графіку. 
Отримані дані завантажуємо до Pover Bi, де ми і будемо робити візуалізацію та аналіз середньої вартості житлової нерухомості.

## Візуалізація та аналіз
---

![image Alt Text](./vizualization/images_2.bmp)
---

Для візуалізації даних застосовуємо лінійно - стовпчатий графік. Лінійний графік відображає ціну, стовпчатий - кількість пропозицій на ринку.
Одразу кидається в очі розрив у графіку на початку 2022 року, це пов'язано з початком бойових дій на территорії України, та згортання ринку нерухомості через закриття реєстрів нерухомості. Після відновлення роботи реєстрів,  ми спостерігаємо невелику анамомалію у вигляді стрибка цін на короткий період. Це було викликано штучно, через "надування" цін у деяких містах, але ринок це швидко виправляє і на початку осені 2022 року ми бачимо нормалізацію ринку і цін.
Далі до весни 2024 року ми бачимо постійне зростання цін, майже на 30%, і корельване зростання кількості пропозицій. Зростання кількості пропозицій я пов'язую з міграційним фактором, адже багато людей покинули територію України, та вирішили продати своє житло. Також хочу акцентувати увагу, що уількість пропозицій - це не кількість реальних угод, інформації по кількості угод немає у відкритому доступі, цю проблему ми будемо намагатися мінімізувати у майбутньому.   

А от зростанням ціни - питання більш складне. Лідируючий сегмент у формуванні цін на ринку нерухомості - ринок первинного житла. За останні 3 роки ми можемо спостерігати постійне зростання цін на сировину та будівельні матеріали, в залежності від сегменту, від 40 до 80 %. Цей фактор змушує забудовників збільшувати ціну за свої об'єкти, тягнучи за собою весь ринок. У якості експеременту додамо графік вартості нерухомості у еквіваленті золота, адже відсоткове здорожчання золота добре корелює зі здорожченням вартості будівельних матеріалів.

![image Alt Text](./vizualization/images_3.bmp)
---

Тобто покупці спостерігають зростання цін на нерухомості у долларі. Продавці, в свою чергу, розуміючи реальну собіварть об'єктів, відмовляються стримувати зростання цін, що призводить до різкого скорочення кількості нових об'єктів,вимушене зниження цін, та стагнації ринку уцілому.





