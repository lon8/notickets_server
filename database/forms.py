from pydantic import BaseModel

class Event(BaseModel):
    name: str
    link: str
    parser: str
    date: str
    venue_id: int
    image_links: str

class EventResponse(BaseModel):
    id: int
    name: str
    link: str
    parser: str
    date: str
    venue_id: int
    image_links: list[str]

class RegionRequest(BaseModel):
    region: int

class VenuePayload(BaseModel):
    venue_id: int
    
class VenueRequest(BaseModel):
    venue: str

class Parser(BaseModel):
    parser: str
