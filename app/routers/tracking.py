from typing import List

from fastapi import HTTPException, APIRouter, Query

from app.models import TrackingResponse
from app.parser_manager import ParseManager

router = APIRouter()
parse_manager = ParseManager()


@router.post("/", response_model=TrackingResponse, tags=["Tracking"])
async def get_tracking_number(tracking_number: List[str] = Query(...)):
    """
    Parse and retrieve information from a given tracking number.

    - **tracking_number**: The tracking number to parse.

    Returns a list of TrackingResult objects containing:
    - **tracking_number**: The tracking number.
    - **carrier**: The carrier or carriers of the tracking number.
    - **results**: The full results of the tracking number parsing.
    """
    results = parse_manager.get_parsers(tracking_number)
    if len(results) == 0:
        raise HTTPException(status_code=404, detail="Tracking number not found")
    else:
        return {
            "detail": "Tracking number parsed successfully",
            "tracking_number": tracking_number,
            "carriers": [x["carrier"] for x in results],
            "results": results,
            "trackingUrl": [x["trackingUrl"] for x in results if "trackingUrl" in x]
        }
