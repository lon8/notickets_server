import requests

headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "ru,en;q=0.9",
    "content-type": "application/x-www-form-urlencoded",
    "sec-ch-ua": "\"Chromium\";v=\"118\", \"YaBrowser\";v=\"23.11\", \"Not=A?Brand\";v=\"99\", \"Yowser\";v=\"2.5\"",
    "referrer": "https://tickets.afisha.ru/wl/402/api?gclid=1194183352.1702901357&document_referrer=https%3A%2F%2Fyandex.ru%2F&site=alexandrinsky.ru&cat_id=undefined&building_id=undefined",
    "referrerPolicy": "strict-origin-when-cross-origin",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin", 
    "x-xsrf-token": "eyJpdiI6IktKS3poUEVMWndVVUR1a1RDVE5XRXc9PSIsInZhbHVlIjoiVjc1NjV6WTR0WEM3cWpCb1Zydkc2SElEQytMTG85SjJnQUo3ZU5rRnMyVVNNbzlkUHphVWduaG9yT0FBUVAyQnJ2SlArVXlhZ2N1K2VMZUhEaXdJTXc9PSIsIm1hYyI6IjZkMmViN2JkOTIzNTYxOTZlZDFlYzZkMzA5NTUyZGYyMzQ4ODYyMWIzOTRjYmRjOTdhYjIxMWIzYjU4ODc2ZDQifQ=="
},

response = requests.post("https://tickets.afisha.ru/wl/402/api/events/info?lang=ru&event_id=676959&user_token=1702901399752-134904")



with open('result.txt', 'w', encoding='utf-8') as file:
    file.write(response.text)