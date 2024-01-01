import requests

# req = requests.get('http://localhost:8000/event_info?event_id=676959&user_token=1702901399752-134904')
req = requests.get('http://localhost:8000/get_events/')

print(req.text)