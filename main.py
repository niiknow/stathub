from datetime import date, datetime

from fastapi import FastAPI

app = FastAPI()


@app.get("/healthcheck")
async def healthcheck():
    """healthcheck endpoint

    Returns:
        string: OK
    """
    return "OK"


@app.get("/statcount/{tenant}/{key}")
async def getStatCount(tenant: str, key: str, start: date = date.today()):
    """Get the summation of stat count

    Args:
        tenant (str): tenant code
        key (str): stat key
        start (datetime.date, optional): start date. Defaults to datetime.date.today().

    Returns:
        int: summation of stat count
    """
    return {"message": "Hello World"}


@app.get("/statdata/{tenant}/{key}")
async def getStat(tenant: str, key: str, start: date = date.today()):
    """Get formatted stat data in json

    Args:
        tenant (str): tenant code
        key (str): stat key
        start (datetime.date, optional): start date. Defaults to datetime.date.today().

    Returns:
        json: formatted stat data in json
    """
    return {"message": "Hello World"}


@app.get("/rawlog/{tenant}/{key}")
async def getRawLog(tenant: str, key: str, start: date = date.today()):
    """Get raw log data, which can be in tsv or json

    Args:
        tenant (str): tenant code
        key (str): stat key
        start (datetime.date, optional): start date. Defaults to datetime.date.today().

    Returns:
        str: raw log data, which can be in tsv or json
    """
    return {"message": "Hello World"}
