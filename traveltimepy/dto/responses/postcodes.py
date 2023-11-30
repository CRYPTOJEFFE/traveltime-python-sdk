from typing import List, Optional

from pydantic import BaseModel


class Property(BaseModel):
    travel_time: Optional[int] = None
    distance: Optional[int] = None


class Postcode(BaseModel):
    code: str
    properties: List[Property]


class PostcodesResult(BaseModel):
    search_id: str
    postcodes: List[Postcode]


class PostcodesResponse(BaseModel):
    results: List[PostcodesResult]
