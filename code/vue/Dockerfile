# base image
FROM node:15.3.0-alpine

# set working directory
WORKDIR /vue/app

# add `/app/node_modules/.bin` to $PATH
#ENV PATH /app/node_modules/.bin:$PATH

# install and cache app dependencies
COPY ./app/package.json /vue/app/package.json
RUN npm install
RUN npm install @vue/cli@4.5.9 -g
RUN npm install json-server -g 

# start app
CMD ["npm", "run", "serve"]


