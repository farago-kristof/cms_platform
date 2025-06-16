FROM nginx:alpine3.18-slim

# Install OpenSSL to generate SSL certificates
RUN apk update && apk add openssl bash

# Create the necessary directory for SSL certificates
RUN mkdir -p /etc/nginx/ssl

# Generate dhparam.pem
RUN openssl dhparam -out /etc/nginx/ssl/dhparam.pem 2048

# Generate the SSL certificate if it doesn't exist
RUN openssl genpkey -algorithm RSA -out /etc/nginx/ssl/server.key \
    && openssl req -new -key /etc/nginx/ssl/server.key -out /etc/nginx/ssl/server.csr -subj "/CN=localhost" \
    && openssl x509 -req -days 365 -in /etc/nginx/ssl/server.csr -signkey /etc/nginx/ssl/server.key -out /etc/nginx/ssl/server.crt

# Remove OpenSSL after certificate generation
RUN apk del --purge openssl