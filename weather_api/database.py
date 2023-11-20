import pymongo
import os
import datetime as dt
import json

from .utils.logger import logger

class Database:
    def __init__(self) -> None:
        self.client = pymongo.MongoClient(os.environ["MONGODB_URI"])
        self.db = self.client["weatherAPI"]  # database name
        self.weather = self.db["weatherData"]
        self.sp = self.db["spData"]
        self.post = self.db["postHarvestData"]
        self.pre = self.db["preHarvestData"]
        
    def load_data(self, date: dt.datetime):
        file_names = [
            f"data/Iran{date.strftime('%Y%m%d')}_weather.geojson",
            f"data/Iran{date.strftime('%Y%m%d')}_AdviseSP.geojson",
            f"data/pesteh{date.strftime('%Y%m%d')}_Advise_Aft.geojson",
            f"data/pesteh{date.strftime('%Y%m%d')}_Advise_Bef.geojson",
        ]
        collections = [self.weather, self.sp, self.post, self.pre]
        for i, file in enumerate(file_names):
            try:
                with open(file, "r") as f:
                    data = json.load(f)
                features = data["features"]
                transformed_data = []
                
                for feature in features:
                    properties = feature["properties"]
                    location = {"location": feature["geometry"]}
                    time_properties = {key: properties[key] for key in properties.keys() if "Time=" in key}
                    timestamp = {"timestamp": date.strftime("%Y%m%d")}
                    entry = {**location, **timestamp, **time_properties}
                    transformed_data.append(entry)
                
                res = collections[i].insert_many(transformed_data)
                logger.info(f"inserted {len(res.inserted_ids)} from {file.split('_')[-1]}")
            except FileNotFoundError:
                logger.error(f"File not found: {file}")
        
    def query_weather(self, 
                      longitude: float, 
                      latitude: float, 
                      max_distance: float = 10000, 
                      date: str = dt.datetime.now().strftime("%Y%m%d")) -> dict:
        res = self.weather.find_one(
            {
                "location":
                    {
                        "$nearSphere":
                            {
                                "$geometry": {"type": "Point", "coordinates": [longitude, latitude]},
                                "$maxDistance": max_distance
                            }
                    },
                "timestamp": date
            }
        )
        if res:
            days = [key.split("=")[1] for key in list(res.keys())[:7] if "Time" in key]
            f_days = [dt.datetime.strptime(day, "%Y%m%d").strftime("%Y-%m-%d") for day in days]
            out = {
                "latitude": res.get("location", {}).get("coordinates")[1],
                "longitude": res.get("location", {}).get("coordinates")[0],
                "generation_date": dt.datetime.strptime(date, "%Y%m%d").strftime('%Y-%m-%d %H:%M'),
                "units": {
                    "max_temperature": "°C",
                    "min_temperature": "°C",
                    "relative_humidity": "%",
                    "precipitation_probability": "%",
                    "wind_speed": "km/h"
                },
                "daily_values": {
                    "dates": f_days,
                    "max_temperature": [res.get(key) for key in list(res.keys()) if key.startswith("tmax")],
                    "min_temperature": [res.get(key) for key in list(res.keys()) if key.startswith("tmin")],
                    "relative_humidity": [res.get(key) for key in list(res.keys()) if key.startswith("rh")],
                    "precipitation_probability": [res.get(key) for key in list(res.keys()) if key.startswith("rain")],
                    "wind_speed": [res.get(key) for key in list(res.keys()) if key.startswith("spd")]
                }
            }
            return out
        else:
            return {"msg": "weather data not found"}
        
    def query_sp(self, 
                      longitude: float, 
                      latitude: float, 
                      max_distance: float = 10000, 
                      date: str = dt.datetime.now().strftime("%Y%m%d")) -> dict:
        res = self.sp.find_one(
            {
                "location":
                    {
                        "$nearSphere":
                            {
                                "$geometry": {"type": "Point", "coordinates": [longitude, latitude]},
                                "$maxDistance": max_distance
                            }
                    },
                "timestamp": date
            }
        )
        if res:
            days = [key.split("=")[1] for key in list(res.keys()) if "Time" in key]
            f_days = [dt.datetime.strptime(day, "%Y%m%d").strftime("%Y-%m-%d") for day in days]
            out = {
                "latitude": res.get("location", {}).get("coordinates")[1],
                "longitude": res.get("location", {}).get("coordinates")[0],
                "generation_date": dt.datetime.strptime(date, "%Y%m%d").strftime('%Y-%m-%d %H:%M'),
                "sp_advice": {
                    "dates": f_days,
                    "advice": [res.get(key, "") for key in list(res.keys()) if key.startswith("Time")],
                }
            }
            return out
        else:
            return {"msg": "SP advice was not found"}

    def query_pre_harvest(self, 
                      longitude: float, 
                      latitude: float, 
                      max_distance: float = 10000, 
                      date: str = dt.datetime.now().strftime("%Y%m%d")) -> dict:
        res = self.pre.find_one(
            {
                "location":
                    {
                        "$nearSphere":
                            {
                                "$geometry": {"type": "Point", "coordinates": [longitude, latitude]},
                                "$maxDistance": max_distance
                            }
                    },
                "timestamp": date
            }
        )
        if res:
            days = [key.split("=")[1] for key in list(res.keys()) if "Time" in key]
            f_days = [dt.datetime.strptime(day, "%Y%m%d").strftime("%Y-%m-%d") for day in days]
            out = {
                "latitude": res.get("location", {}).get("coordinates")[1],
                "longitude": res.get("location", {}).get("coordinates")[0],
                "generation_date": dt.datetime.strptime(date, "%Y%m%d").strftime('%Y-%m-%d %H:%M'),
                "pre_harvest_advice": {
                    "dates": f_days,
                    "advice": [res.get(key, "") for key in list(res.keys()) if key.startswith("Time")],
                }
            }
            return out
        else:
            return {"msg": "pre-harvest advice was not found"}
        
    def query_post_harvest(self, 
                      longitude: float, 
                      latitude: float, 
                      max_distance: float = 10000, 
                      date: str = dt.datetime.now().strftime("%Y%m%d")) -> dict:
        res = self.post.find_one(
            {
                "location":
                    {
                        "$nearSphere":
                            {
                                "$geometry": {"type": "Point", "coordinates": [longitude, latitude]},
                                "$maxDistance": max_distance
                            }
                    },
                "timestamp": date
            }
        )
        if res:
            days = [key.split("=")[1] for key in list(res.keys()) if "Time" in key]
            f_days = [dt.datetime.strptime(day, "%Y%m%d").strftime("%Y-%m-%d") for day in days]
            out = {
                "latitude": res.get("location", {}).get("coordinates")[1],
                "longitude": res.get("location", {}).get("coordinates")[0],
                "generation_date": dt.datetime.strptime(date, "%Y%m%d").strftime('%Y-%m-%d %H:%M'),
                "post_harvest_advice": {
                    "dates": f_days,
                    "advice": [res.get(key, "") for key in list(res.keys()) if key.startswith("Time")],
                }
            }
            return out
        else:
            return {"msg": "post-harvest advice was not found"}

if __name__=="__main__":
    db = Database()
    date = dt.date(2023, 10, 17)
    date = dt.datetime.now()
    db.load_data(date)
        
        
   
        
        