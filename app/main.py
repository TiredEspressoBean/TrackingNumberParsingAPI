import pkgutil
from fastapi import FastAPI
from app.routers import tracking

app = FastAPI(version="v0.1")

@app.get("/status")
async def status():
    """
    Endpoint to check the status of the API.

    - **results** A JSON object containing the version of the application and its operational status.
    Example response:
    {
        "version": "1.0.0",
        "status": true
    }
    """
    return {
        "version": app.version,
        "status": True,
    }


@app.get("/carriers")
async def carriers():
    """
    Endpoint to retrieve the list of all carriers that currently have their own parsers and are supported.

    - **results** A list of strings representing the names of all carriers with implemented parsers.
    Example response:
    [
        "FedEx",
        "OnTrac",
        "UPS"
    ]
    """
    ret = []
    for finder, name, ispkg in pkgutil.iter_modules(['app/parsers']):
        if name != 'base_parser' and name != 'BaseParser':
            ret.append(name)
    return ret


app.include_router(tracking.router, prefix="/track", tags=["Tracking"])
