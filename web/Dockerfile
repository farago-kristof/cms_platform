FROM node:22-alpine AS builder

ARG VITE_API_BASE_URL
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL
ENV APP_PATH=/app

RUN addgroup -g 11275 service && \
    adduser -u 11275 -G service -s /bin/sh -D service && \
    mkdir -p /app && chown -R service:service /app

WORKDIR ${APP_PATH}

COPY --chown=service:service src/package*.json ./

USER service

RUN npm install

COPY --chown=service:service src/ ./src/

COPY --chown=service:service  index.html vite.config.js ./

RUN npm run build


FROM nginx:1.27-alpine

ENV APP_PATH=/app

RUN rm -rf /usr/share/nginx/html/*

COPY --from=builder --chown=service:service ${APP_PATH}/dist /usr/share/nginx/html

CMD ["nginx", "-g", "daemon off;"]
