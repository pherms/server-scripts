FROM node:lts-slim AS builder
ENV NODE_ENV=develpment
WORKDIR /usr/src/server-api
RUN apt update && apt install -y openssl
COPY server .
RUN npm install && npm run generate && npm run migrate && npm run build 

FROM node:lts-slim AS server-api
WORKDIR /usr/src/server-api
COPY --from=builder /usr/src/server-api/package.json .
COPY --from=builder /usr/src/server-api/dist .
COPY --from=builder /usr/src/server-api/prisma ./prisma
COPY --from=builder /usr/src/server-api/src/utils/helperfunctions.js ./utils
COPY --from=builder /usr/src/server-api/src/middlewares ./middlewares
COPY --from=builder /usr/src/server-api/src/controllers/authorization.controller.js ./controllers
ENV NODE_ENV=development
RUN npm install @prisma/client prisma
RUN apt-get update && apt-get -y install openssl && rm -rf /var/lib/apt/lists/*
RUN npm install
ENV NODE_ENV=production
CMD [ "node", "index.js" ]