FROM debian:latest

# Install Icecast (Silent Mode)
RUN DEBIAN_FRONTEND=noninteractive apt update && apt install -y icecast2 && rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN useradd -m -g icecast icecast

# Set up writable log directory
RUN mkdir -p /var/log/icecast && chown -R icecast:icecast /var/log/icecast

# Copy Icecast config
COPY icecast.xml /etc/icecast2/icecast.xml

# Switch to non-root user
USER icecast

# Start Icecast
CMD ["icecast2", "-c", "/etc/icecast2/icecast.xml"]
