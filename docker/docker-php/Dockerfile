FROM php:7.2.24-apache
LABEL maintainer="imjoseangel"

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    libicu-dev \
    libpng-dev \
    sendmail \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

RUN docker-php-ext-install exif gd gettext intl mysqli pcntl pdo_mysql readline \
    shmop sockets sysvmsg sysvsem sysvshm wddx xsl

COPY hello.php /var/www/html/index.php
