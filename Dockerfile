FROM python:3.11-alpine3.18

RUN apk update && \
    apk add --no-cache python3-dev mariadb-dev build-base

COPY ./requirements.txt /app/requirements.txt

RUN echo 'export PATH="/usr/local/opt/mysql-client/bin:$PATH"' >> ~/.zshrc

RUN pip install -r /app/requirements.txt

COPY ./flaskr ./app/flaskr

WORKDIR /app/flaskr/

ENTRYPOINT [ "python" ]

CMD ["app.py" ]