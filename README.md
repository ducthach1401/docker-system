# Docker system run on Armbian

sudo certbot certonly --manual --preferred-challenges dns -d www.bighand.asia

certbot renew

'overwriteprotocol' => 'https',
'overwritehost' => 'bighand.asia',
