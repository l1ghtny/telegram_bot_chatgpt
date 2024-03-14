FROM python:3.12-alpine

WORKDIR /home/tg-bot-gpt/
RUN mkdir logs

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY .env .
ADD src ./src
COPY main.py .
COPY credentials.py .

CMD [ "python", "main.py" ]