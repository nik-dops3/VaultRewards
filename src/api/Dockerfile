# ─────────────────────────────────────────────
# VaultRewards API — Dockerfile
# ─────────────────────────────────────────────

# Start from the official Python 3.11 slim image
# slim = minimal Ubuntu with Python installed
# no extra tools, smaller image, less attack surface
FROM python:3.11-slim

# Set who maintains this image
# Not required but good practice — shows ownership
LABEL maintainer="nik.dops3@gmail.com"
LABEL project="vaultrewards"
LABEL component="api"

# Set environment variables inside the container
# PYTHONDONTWRITEBYTECODE=1 — stops Python writing .pyc cache files
# we do not want compiled bytecode cluttering the container
# PYTHONUNBUFFERED=1 — forces Python to print output immediately
# without this, logs appear delayed or not at all
# critical for seeing logs in CloudWatch and kubectl logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
# all following commands run from here
# your files will live at /app inside the container
WORKDIR /app

# Copy requirements FIRST — before copying application code
# this is the layer caching trick:
# requirements.txt changes rarely
# application code changes constantly
# by copying requirements first — pip install is cached
# and only reruns when requirements.txt actually changes
COPY requirements.txt .

# Install Python dependencies
# --no-cache-dir — do not store the pip download cache
# we do not need it after installation
# keeping it just makes the image bigger
RUN pip install --no-cache-dir -r requirements.txt

# Now copy the rest of the application code
# this layer rebuilds on every code change
# but that is fine — it is just a file copy, very fast
# dependencies are already cached from the step above
COPY . .

# Create a non-root user to run the application
# by default Docker containers run as root
# running as root inside a container is a security risk
# if an attacker breaks into the container — they get root
# this creates a user called 'vaultrewards' with no special privileges
RUN useradd --create-home --shell /bin/bash vaultrewards

# Switch to the non-root user
# everything from here runs as 'vaultrewards' not root
USER vaultrewards

# Document that this container listens on port 5000
# this is documentation only — does not actually open the port
# the actual port mapping happens with -p when running the container
EXPOSE 5000

# The command that runs when a container starts
# gunicorn is a production web server — handles real traffic
# --workers 2 — run 2 worker processes to handle requests in parallel
# --bind 0.0.0.0:5000 — listen on all network interfaces on port 5000
# 0.0.0.0 means accept connections from anywhere
# 127.0.0.1 would mean only from inside the container — useless
# app:app — the first 'app' is the filename (app.py)
#           the second 'app' is the Flask application object inside it
CMD ["gunicorn", "--workers", "2", "--bind", "0.0.0.0:5000", "app:app"]