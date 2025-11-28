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

ARG VUE_APP_version
ENV VUE_APP_version=${VUE_APP_version}

RUN npm run build

FROM nginx:mainline-alpine3.22 AS runtime

COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]