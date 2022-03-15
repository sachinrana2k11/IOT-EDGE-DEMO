FROM python:3.8-slim-buster
RUN apt-get update && apt-get -y install cmake
WORKDIR /app
COPY requirements.txt ./
RUN apt-get update && apt-get -qq install cmake
#RUN pip install -r requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .
CMD [ "python3", "-u", "./main.py" ]