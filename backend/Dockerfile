FROM python:3.9

RUN mkdir /app

COPY requirements.txt .

RUN python -m pip install --upgrade pip && pip3 install -r requirements.txt --no-cache-dir

COPY . /app

WORKDIR /app

CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8080" ]
