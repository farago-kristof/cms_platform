FROM node:22-alpine AS builder

ENV APP_PATH=/app

RUN addgroup -g 11275 service && \
    adduser -u 11275 -G service -s /bin/sh -D service && \
    mkdir -p /app && chown -R service:service /app

WORKDIR ${APP_PATH}

COPY --chown=service:service web/src/package*.json ./

USER service

RUN npm install

COPY --chown=service:service web/src/ ./src/

COPY --chown=service:service  web/index.html web/vite.config.js ./

RUN npm run build


FROM nginx:1.27-alpine

ENV APP_PATH=/app

#RUN addgroup -g 11275 service && adduser -u 11275 -G service -s /bin/sh -D service
#
#RUN mkdir -p /var/cache/nginx/client_temp /var/cache/nginx/proxy_temp /var/cache/nginx/fastcgi_temp \
#    && chown -R service:service /var/cache/nginx
#
#RUN mkdir -p /run && chown service:service /run

RUN rm -rf /usr/share/nginx/html/*

COPY --from=builder --chown=service:service ${APP_PATH}/dist /usr/share/nginx/html

#USER service

CMD ["nginx", "-g", "daemon off;"]
