FROM nginx:alpine

RUN apk update \
    && apk upgrade \
    && apk add --no-cache openssl \
    && apk add --no-cache bash \
    && set -ex \
    && apk --no-cache add sudo \
    && adduser -D -H -u 1000 -s /bin/bash www-data -G www-data

#remove the default conf
RUN rm /etc/nginx/conf.d/default.conf

CMD ["nginx"]

EXPOSE 8888 443
