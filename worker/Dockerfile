FROM python:3.10-bullseye

WORKDIR /worker
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
