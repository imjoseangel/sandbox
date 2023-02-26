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

RUN mkdir -p /usr/src/php/ext

# Install php-memcached
RUN cd /usr/src/php/ext \
    && curl -fsSL https://github.com/php-memcached-dev/php-memcached/archive/php7.tar.gz -o memcached.tar.gz \
    && mkdir -p memcached \
    && tar -xf memcached.tar.gz -C memcached --strip-components=1 \
    && rm memcached.tar.gz \
    && docker-php-ext-install memcached

# Install php-igbinary
RUN cd /usr/src/php/ext \
    && curl -fsSL https://github.com/igbinary/igbinary7/archive/master.tar.gz -o igbinary.tar.gz \
    && mkdir -p igbinary \
    && tar -xf igbinary.tar.gz -C igbinary --strip-components=1 \
    && rm igbinary.tar.gz \
    && docker-php-ext-install igbinary

RUN docker-php-ext-install calendar exif gd gettext intl mysqli pcntl pdo_mysql \
    readline shmop sockets sysvmsg sysvsem sysvshm wddx xsl

COPY hello.php /var/www/html/index.php
