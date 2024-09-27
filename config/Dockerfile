FROM node:lts-slim AS builder
RUN apt update && apt install python
ENV NODE_ENV production
WORKDIR /usr/src/server-api
COPY server .
RUN npm install && npm run build && npm run generate && npm run migrate
WORKDIR /usr/src
COPY copy-js.py .
RUN python copy-js.py

FROM node:lts-slim AS server-api
ENV NODE_ENV production
WORKDIR /usr/src/server-api
COPY --from builder /usr/src/server-api/dist/ .
