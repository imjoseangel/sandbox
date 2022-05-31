ARG build_for=linux/amd64
# build environment
FROM node:lts-alpine as build

# set working directory
WORKDIR /app

# add `/app/node_modules/.bin` to $PATH
ENV PATH /app/node_modules/.bin:$PATH

# install app dependencies
COPY package.json ./
COPY package-lock.json ./
RUN npm install --silent
RUN npm install react-scripts@5.0.1 -g --silent

# add app
COPY . ./

RUN npm run build

# production environment
FROM nginx:stable-alpine
COPY --from=build /app/build /usr/share/nginx/html

RUN apk add --no-cache openssh
COPY sshd_config /etc/ssh/sshd_config
RUN echo -n 'root:Docker!' | chpasswd

COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf
COPY init.sh /usr/local/bin/init.sh
RUN chmod u+x /usr/local/bin/init.sh

EXPOSE 80 2222
ENTRYPOINT ["init.sh"]
