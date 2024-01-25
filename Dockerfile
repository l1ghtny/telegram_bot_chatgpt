FROM python:3

WORKDIR /home/tg-bot/
RUN mkdir logs

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY .env .
ADD etc ./etc
COPY main.py .
COPY credentials.py .

CMD [ "python", "main.py" ]