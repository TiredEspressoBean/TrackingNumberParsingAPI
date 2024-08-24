from pydantic import BaseModel
from typing import List, Optional

class TrackingResponse(BaseModel):
    detail: str
    tracking_number: List[str]
    carriers: List[str]
    results: list
    trackingUrl: Optional[List[str]]

class StatusResponse(BaseModel):
    status: str
    version: str