ARG build_for=linux/amd64,linux/arm64
FROM alpine:latest as base

LABEL maintainer="imjoseangel"

# Packages to build image requirements
RUN apk add --no-cache \
    tcpdump

ENTRYPOINT [ "tcpdump" ]
CMD [ "-i", "eth0" ]
