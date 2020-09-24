
FROM php:7.3-fpm

RUN set -xe; \
  apt-get update -yqq \
  && pecl channel-update pecl.php.net \
  && apt-get install -yqq \
    apt-utils \
    libzip-dev zip unzip \
  && docker-php-ext-configure zip \
  && docker-php-ext-install zip \
  && php -m | grep -q 'zip'

RUN pecl install -o -f redis \
  && rm -rf /tmp/pear \
  && docker-php-ext-enable redis;

RUN docker-php-ext-install sockets

RUN docker-php-ext-install mysqli

WORKDIR /var/www

CMD ["php-fpm"]

EXPOSE 9000