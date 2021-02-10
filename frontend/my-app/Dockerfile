# build environment
FROM node:12.16.1-alpine AS builder
WORKDIR /app
# COPY package.json package-lock.json ./
COPY /frontend/my-app .
RUN apk upgrade --update
# for node version 10.x
# RUN curl -sL https://rpm.nodesource.com/setup_10.x | bash -
# optional to check that it worked
RUN node --version
RUN npm --version 
RUN npm i
RUN npm run build

# production environment
FROM nginx:1.19.6-alpine
COPY --from=builder /app/dist/my-app /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]

