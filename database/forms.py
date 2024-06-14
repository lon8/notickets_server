from pydantic import BaseModel

class Event(BaseModel):
    name: str
    link: str
    parser: str
    date: str
    venue_id: int

class EventResponse(BaseModel):
    name: str
    link: str
    parser: str
    date: str
    venue: str

class RegionRequest(BaseModel):
    region: int

class VenuePayload(BaseModel):
    venue_id: int
    
class VenueRequest(BaseModel):
    venue: str

class Parser(BaseModel):
    parser: str