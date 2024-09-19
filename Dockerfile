FROM python:3.11

WORKDIR /app


COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=core/server.py

EXPOSE 5000

CMD ["flask", "run"]

