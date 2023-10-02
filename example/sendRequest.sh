#/bin/zsh

#DATA="{\"WIZARD\":{}}"
DATA="{\"STATISTIC\":{}}"
#DATA="{\"ENERGY\":{}}"
#DATA="{\"PV1\":{}}"
#DATA="{\"PM1OBJ1\":{}}"

IP=192.168.15.58

# Senec SSL certificate is invalid :-(

curl --insecure -X POST https://$IP/lala.cgi -d $DATA


