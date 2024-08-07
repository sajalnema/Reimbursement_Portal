
FROM python

WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y default-libmysqlclient-dev

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install Pillow

COPY . .

CMD ["python", "manage.py", "migrate"]

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
