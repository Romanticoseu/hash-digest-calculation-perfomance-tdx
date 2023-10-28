FROM python:3.8

ARG http_proxy
ARG https_proxy


# Set the working directory
WORKDIR /app

# make log directory
RUN mkdir log

COPY ./client/client.py .
COPY ./server/server.py .
COPY entrypoint.sh .
COPY generate.sh .

RUN mkdir log && \
    chmod +x entrypoint.sh && \
    chmod +x generate.sh
    

ENTRYPOINT ["/app/entrypoint.sh"]