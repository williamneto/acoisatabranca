FROM node:14.18.2-slim

RUN DEBIAN_FRONTEND="noninteractive" apt update && \
    DEBIAN_FRONTEND="noninteractive" apt install -y build-essential git python3

COPY ./package.json /app/package.json

WORKDIR /app

# Production
# RUN yarn install && \
#     yarn build && \
#     yarn global add serve
RUN npm install 

RUN DEBIAN_FRONTEND="noninteractive" apt autoremove

COPY ./public/ /app/public

COPY ./src/ /app/src

EXPOSE 3000

# CMD serve -s build
CMD npm start