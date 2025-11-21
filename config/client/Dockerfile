FROM node:22-alpine AS build

RUN npm install -g @vue/cli@3
RUN mkdir -p /app

ARG NODE_ENV=production
ENV NODE_ENV=${NODE_ENV}

COPY config/client/. ./app/
WORKDIR /app

RUN npm ci --include=dev

ARG VUE_APP_apiserver
ENV VUE_APP_apiserver=${VUE_APP_apiserver}

RUN npm run build

FROM nginx:mainline-alpine3.22 AS runtime

COPY --from=build /app/docker-entrypoint.sh /docker-entrypoint.sh
COPY --from=build /app/config.template.js /usr/share/nginx/html/config.template.js

COPY --from=build /app/dist /usr/share/nginx/html

RUN apk add --no-cache gettext \
    && chmod +x /docker-entrypoint.sh

EXPOSE 80
ENTRYPOINT [ "/docker-entrypoint.sh" ]
CMD ["nginx", "-g", "daemon off;"]