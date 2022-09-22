FROM python:3.10-alpine

RUN apk update && apk add postgresql-dev gcc g++ python3-dev musl-dev bash git libffi-dev

WORKDIR /usr/src/app
COPY . .

RUN pip install -r requirements.txt
# RUN pip install --upgrade -e .

EXPOSE 5000

CMD [ "gunicorn", "app.run:application","-b", "0.0.0.0:5000" ]