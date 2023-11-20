from fastapi import FastAPI, HTTPException, status, Depends, Query
from .database import Database

app = FastAPI(title="Infortech Weather API",
            #   contact={
            #       "name": "AmirRezvanian", 
            #       "url": "https://github.com/amirr95",
            #       "email": "a.rezvanian@bontech.ir"}
            )

def get_db():
    try:
        db = Database()
        yield db
    finally:
        db.client.close()


@app.get("/")
async def home():
    return {"available endpoints": ["/weather/daily", "advice/sp", "advice/pre-harvest", "advice/post-harvest"]}

@app.get("/weather/daily")
async def get_daily_weather(
    long: float = Query(..., description="مقدار طول جغرافیایی نقطه مورد نظر", ge=-180, le=180),
    lat: float = Query(..., description="مقدار عرض جغرافیایی نقطه مورد نظر", ge=-90, le=90),
    # date: str = Query(..., description="تاریخ مورد نظر. باید مانند 20231120 وارد شود."),
    db: Database = Depends(get_db)
):
    res = db.query_weather(longitude=long, latitude=lat)
    if not res:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Data not found for the specified location."
        )
    else:
        return res


@app.get("/advice/sp")
async def get_sp_advice(
    long: float = Query(..., description="مقدار طول جغرافیایی نقطه مورد نظر", ge=-180, le=180),
    lat: float = Query(..., description="مقدار عرض جغرافیایی نقطه مورد نظر", ge=-90, le=90),
    # date: str = Query(..., description="تاریخ مورد نظر. باید مانند 20231120 وارد شود."),
    db: Database = Depends(get_db)
):
    res = db.query_sp(longitude=long, latitude=lat)
    if not res:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Data not found for the specified location."
        )
    else:
        return res

@app.get("/advice/pre-harvest")
async def get_pre_harvest_advice(
    long: float = Query(..., description="مقدار طول جغرافیایی نقطه مورد نظر", ge=-180, le=180),
    lat: float = Query(..., description="مقدار عرض جغرافیایی نقطه مورد نظر", ge=-90, le=90),
    # date: str = Query(..., description="تاریخ مورد نظر. باید مانند 20231120 وارد شود."),
    db: Database = Depends(get_db)
):
    res = db.query_pre_harvest(longitude=long, latitude=lat)
    if not res:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Data not found for the specified location."
        )
    else:
        return res

@app.get("/advice/post-harvest")
async def get_post_harvest_advice(
    long: float = Query(..., description="مقدار طول جغرافیایی نقطه مورد نظر", ge=-180, le=180),
    lat: float = Query(..., description="مقدار عرض جغرافیایی نقطه مورد نظر", ge=-90, le=90),
    # date: str = Query(..., description="تاریخ مورد نظر. باید مانند 20231120 وارد شود."),
    db: Database = Depends(get_db)
):
    res = db.query_post_harvest(longitude=long, latitude=lat)
    if not res:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Data not found for the specified location."
        )
    else:
        return res
    