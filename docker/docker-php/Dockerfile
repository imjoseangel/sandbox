FROM php:7.4-fpm
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

# Install php-ext
RUN docker-php-ext-install calendar exif gd gettext intl mysqli pcntl \
    pdo_mysql shmop sockets sysvmsg sysvsem sysvshm xsl \
    opcache

# Enable php-ext
RUN docker-php-ext-enable igbinary memcached msgpack

# Add PHP Composer
# COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

# Add nginx user
# RUN groupadd -g 1000 nginx && \
#     useradd -r -u 1000 -g nginx -d /var/www nginx

# WORKDIR /app

# COPY . .

# RUN composer update && composer install --no-dev && composer dump-autoload
