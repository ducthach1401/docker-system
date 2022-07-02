# Docker system run on Armbian

sudo certbot certonly --manual --preferred-challenges dns -d www.bighand.space

cp -r /etc/letsencrypt/live/www.bighand.space/* .

certbot renew
