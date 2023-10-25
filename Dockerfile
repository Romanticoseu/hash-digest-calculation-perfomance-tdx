FROM python:3.8

ARG http_proxy
ARG https_proxy


# Set the working directory
WORKDIR /app

COPY ./client/client.py .
COPY ./server/server.py .
COPY entrypoint.sh .

RUN chmod +x entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]