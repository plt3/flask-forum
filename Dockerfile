FROM python:latest

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# copy project
COPY . .

# only run this if you want this app to run as its own container without docker-compose
# CMD ["python3", "runIt.py"]
