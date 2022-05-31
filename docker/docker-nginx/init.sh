#!/bin/sh

ssh-keygen -A
/usr/sbin/sshd -e
exec nginx -g 'daemon off;'
