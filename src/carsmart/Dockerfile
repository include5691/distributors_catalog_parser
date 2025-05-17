FROM python:3

WORKDIR /app

ENV PYTHONUNBUFFERED=1

COPY /au_b24 /app/au_b24
COPY /e5nlp /app/e5nlp

COPY /distributors_catalog_parser/src  /app/src
COPY /distributors_catalog_parser/requirements.txt /distributors_catalog_parser/.env /app/

RUN pip install ./au_b24
RUN pip install ./e5nlp
RUN pip install -r requirements.txt

RUN ln -fs /usr/share/zoneinfo/Asia/Yekaterinburg /etc/localtime \
    && dpkg-reconfigure -f noninteractive tzdata

ENTRYPOINT ["python3", "-m", "src.carsmart.parse"]