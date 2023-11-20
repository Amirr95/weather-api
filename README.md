# Introduction  
FastAPI app with endpoints for weather prediction, post/pre harvest advice (currently only for pistachio) and <a href="https://en.wikipedia.org/wiki/Foliar_feeding">Foliar feeding</a>.  
Data is produced in `geojson` format and loaded into a mongo database. The API queries the database for information regarding the location of the user.  
## API Endpoints  
- `/weather/daily`
- `/advice/sp`
- `/advice/pre-harvest`
- `/advice/post-harvest`


