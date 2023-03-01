FROM php:7.2.24-apache
LABEL maintainer="imjoseangel"

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    libicu-dev \
    libpng-dev \
    libedit-dev \
    libmemcached-dev \
    libreadline-dev \
    libxml2-dev \
    libxslt-dev \
    sendmail \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Install php-pecl
RUN pecl install igbinary memcached msgpack

RUN docker-php-ext-install calendar exif gd gettext intl mysqli pcntl \
    pdo_mysql readline shmop sockets sysvmsg sysvsem sysvshm wddx xsl \
    opcache

RUN docker-php-ext-enable igbinary memcached msgpack

COPY hello.php /var/www/html/index.php
