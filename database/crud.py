from fastapi import APIRouter, Query

from database.models import session, AllEvents
from database.forms import Event

router = APIRouter()


@router.post('/put_events/')
def put_events(event: Event):
    print(event.name, event.parser)

    new_event = AllEvents(
        name=event.name,
        link=event.link,
        parser=event.parser,
        date=event.date,
        venue=event.venue
    )
    session.add(new_event)
    session.commit()
