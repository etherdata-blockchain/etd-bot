FROM python:alpine3.13

WORKDIR /app
COPY . .
RUN pip3 install -r requirements.txt
CMD ["python3", "bot.py"]