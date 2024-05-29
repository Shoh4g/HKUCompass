FROM python:3.9

ENV PIP_ROOT_USER_ACTION=ignore

WORKDIR /build

COPY .env /build/.env

COPY ./requirements.txt /build/requirements.txt

COPY ./setup.py /build/setup.py

RUN pip install --upgrade pip

RUN pip install --no-cache-dir --upgrade -r /build/requirements.txt

RUN python /build/setup.py

COPY ./app /build/app

EXPOSE 80

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]