from fastapi import APIRouter, Query

from database.models import session, AllEvents

router = APIRouter()


@router.post('/put_events/')
def put_events(
        name: str = Query(None),
        link: str = Query(None),
        parser: str = Query(None),
        date: str = Query(None),
        venue: str = Query(None)
):

    new_event = AllEvents(
        name=name,
        link=link,
        parser=parser,
        date=date,
        venue=venue
    )
    session.add(new_event)
    session.commit()

