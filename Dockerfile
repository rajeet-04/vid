FROM debian:latest

# Install Icecast
RUN apt update && apt install -y icecast2 && rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN useradd -m icecast
USER icecast

# Copy config file
COPY icecast.xml /etc/icecast2/icecast.xml

CMD ["icecast2", "-c", "/etc/icecast2/icecast.xml"]
