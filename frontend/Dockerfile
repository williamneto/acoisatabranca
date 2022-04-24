FROM node:14.18.2-slim

RUN DEBIAN_FRONTEND="noninteractive" apt update && \
    DEBIAN_FRONTEND="noninteractive" apt install -y build-essential git python3

COPY ./package.json /app/package.json
RUN chmod -R 777 /app
WORKDIR /app

# Production
# RUN yarn install && \
#     yarn build && \
#     yarn global add serve
RUN npm install 

RUN DEBIAN_FRONTEND="noninteractive" apt autoremove

COPY ./public/ /app/public

COPY ./src/ /app/src

RUN npm run build

FROM nginx:1.16.0-alpine
COPY --from=builder /build /usr/share/nginx/html
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx/nginx.conf /etc/nginx/conf.d
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]