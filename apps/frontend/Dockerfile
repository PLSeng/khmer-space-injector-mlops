FROM node:20-alpine AS build
WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

# Keep container alive only to provide /dist to nginx via volume copy (compose will use it)
CMD ["sh", "-c", "cp -r /app/dist/* /dist && tail -f /dev/null"]