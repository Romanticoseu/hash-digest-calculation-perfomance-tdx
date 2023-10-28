FROM python:3.8

ARG http_proxy
ARG https_proxy


# Set the working directory
WORKDIR /app


COPY ./client/client.py .
COPY ./client/config.yaml .
COPY ./server/server.py .
COPY entrypoint.sh .
COPY generate.sh .

RUN mkdir log && \
    pip install pyyaml && \
    chmod +x entrypoint.sh && \
    chmod +x generate.sh
    

ENTRYPOINT ["/app/entrypoint.sh"]