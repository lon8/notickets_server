from pydantic import BaseModel

class Event(BaseModel):
    name: str
    link: str
    parser: str
    date: str
    venue: str

class Parser(BaseModel):
    parser: str