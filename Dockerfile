FROM debian:latest

RUN apt update && apt install -y icecast2 && rm -rf /var/lib/apt/lists/*

COPY icecast.xml /etc/icecast2/icecast.xml

CMD ["icecast2", "-c", "/etc/icecast2/icecast.xml"]
