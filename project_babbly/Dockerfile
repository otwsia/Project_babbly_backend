FROM python:3.9

ENV PYTHONBUFFERED=1

WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

#EXPOSE 8000
#
#CMD ["python", "manage.py", "runserver"]

CMD python manage.py runserver --bind 0.0.0.0:$PORT