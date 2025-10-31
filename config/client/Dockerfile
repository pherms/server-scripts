FROM node:22-alpine AS build
WORKDIR /app

ARG NODE_ENV=production
ENV NODE_ENV=${NODE_ENV}

COPY package*.json ./
RUN npm install --production

COPY . .

ARG VUE_APP_apiserver
ENV VUE_APP_apiserver=${VUE_APP_apiserver}

RUN npm run build

FROM nginx:stable-alpine AS runtime

COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]