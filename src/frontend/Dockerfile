
# ─────────────────────────────────────────────
# VaultRewards Frontend — Dockerfile
# ─────────────────────────────────────────────

# nginx:alpine is a minimal nginx web server
# alpine = a tiny Linux distribution, only 5MB
# perfect for serving static files
# no Python, no Node, nothing extra
FROM nginx:alpine

# Remove the default nginx welcome page
# nginx comes with a placeholder HTML file
# we do not want that — we want our own
RUN rm -rf /usr/share/nginx/html/*

# Copy our frontend files into the directory
# nginx serves from /usr/share/nginx/html/ by default
# anything placed here gets served to browsers
COPY index.html /usr/share/nginx/html/index.html

# Document that nginx listens on port 80
# nginx always listens on port 80 by default
# HTTP standard port
EXPOSE 80

# nginx:alpine already has a CMD built in
# it starts nginx automatically when the container starts
# we do not need to write our own CMD here
# the base image handles it
