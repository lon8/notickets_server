from fastapi import APIRouter, Query
import requests

router = APIRouter()

@router.get('/event_info/')
def get_event_info(
        event_id: int = Query(None),
        user_token: str = Query(None)
    ):
    
    req = requests.post(f'https://tickets.afisha.ru/wl/402/api/events/info?lang=ru&event_id={event_id}&user_token={user_token}')
    
    return req.json()