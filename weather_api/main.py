from fastapi import FastAPI, Depends, Query
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
    finally:
        db.client.close()


@app.get("/")
async def home():
    return {"available endpoints": ["/weather/daily", "advice/sp", "advice/pre-harvest", "advice/post-harvest"]}

@app.get("/weather/daily")
async def get_daily_weather(
    long: float = Query(..., description="مقدار طول جغرافیایی نقطه مورد نظر"),
    lat: float = Query(..., description="مقدار عرض جغرافیایی نقطه مورد نظر"),
    date: str = Query(..., description="تاریخ مورد نظر. باید مانند 20231120 وارد شود."),
    db: Database = Depends(Database)
):
    return db.query_weather(longitude=long, latitude=lat, date=date)

@app.get("/advice/sp")
async def get_sp_advice(
    long: float = Query(..., description="مقدار طول جغرافیایی نقطه مورد نظر"),
    lat: float = Query(..., description="مقدار عرض جغرافیایی نقطه مورد نظر"),
    date: str = Query(..., description="تاریخ مورد نظر. باید مانند 20231120 وارد شود."),
    db: Database = Depends(Database)
):
    return db.query_sp(longitude=long, latitude=lat, date=date)

@app.get("/advice/pre-harvest")
async def get_pre_harvest_advice(
    long: float = Query(..., description="مقدار طول جغرافیایی نقطه مورد نظر"),
    lat: float = Query(..., description="مقدار عرض جغرافیایی نقطه مورد نظر"),
    date: str = Query(..., description="تاریخ مورد نظر. باید مانند 20231120 وارد شود."),
    db: Database = Depends(Database)
):
    return db.query_pre_harvest(longitude=long, latitude=lat, date=date)

@app.get("/advice/post-harvest")
async def get_post_harvest_advice(
    long: float = Query(..., description="مقدار طول جغرافیایی نقطه مورد نظر"),
    lat: float = Query(..., description="مقدار عرض جغرافیایی نقطه مورد نظر"),
    date: str = Query(..., description="تاریخ مورد نظر. باید مانند 20231120 وارد شود."),
    db: Database = Depends(Database)
):
    return db.query_post_harvest(longitude=long, latitude=lat, date=date)