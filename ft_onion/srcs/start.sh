#!/bin/sh

service ssh start
service tor start
cat /var/lib/tor/hidden_service/hostname > /tor-hostname
chmod 444 /tor-hostname

exec "$@"
