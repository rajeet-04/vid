FROM debian:latest

# Install Icecast
RUN apt update && apt install -y icecast2 && rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN useradd -m -g icecast icecast

USER icecast

# Copy config file
COPY icecast.xml /etc/icecast2/icecast.xml

RUN mkdir -p /usr/local/icecast/logs
CMD ["icecast2", "-c", "/etc/icecast2/icecast.xml"]

COPY mime.types /etc/mime.types

