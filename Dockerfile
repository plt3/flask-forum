FROM python:latest

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# copy project
COPY . .

RUN chmod +x start.sh

CMD ["./start.sh"]
