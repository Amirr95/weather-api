FROM python:3.10.6-slim

WORKDIR /weather-api

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /weather-api

# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--reload"]