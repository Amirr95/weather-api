import pymongo
import os
import datetime as dt
import json

from utils.logger import logger

class Database:
    def __init__(self) -> None:
        self.client = pymongo.MongoClient(os.environ["MONGODB_URI"])
        self.db = self.client["weatherAPI"]  # database name
        self.weather = self.db["weatherData"]
        self.sp = self.db["spData"]
        self.post = self.db["postHarvestData"]
        self.pre = self.db["preHarvestData"]
        
    def load_weather(self, date: dt.datetime):
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
                    location = {"geometry": feature["geometry"]}
                    time_properties = {key: properties[key] for key in properties.keys() if "Time=" in key}
                    timestamp = {"timestamp": date.strftime("%Y%m%d")}
                    entry = {**location, **timestamp, **time_properties}
                    transformed_data.append(entry)
                
                res = collections[i].insert_many(transformed_data)
                logger.info(f"inserted {len(res.inserted_ids)} from {file.split('_')[-1]}")
            except FileNotFoundError:
                logger.error(f"File not found: {file}")
        

if __name__=="__main__":
    db = Database()
    date = dt.date(2023, 10, 17)
    db.load_weather(date)
        
        
   
        
        