FROM python:3.11-slim

WORKDIR /app

COPY ./requirements.txt .

RUN apt-get update && apt-get install -y git


RUN pip3 install -r ./requirements.txt --no-cache-dir

COPY ./locales ./locales
COPY ./logs ./logs
COPY ./src ./src


CMD ["python", "src/eng_converter_bot.py"]