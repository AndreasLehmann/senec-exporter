#/bin/zsh

#DATA="{\"WIZARD\":{}}"
#DATA="{\"STATISTIC\":{}}"
#DATA="{\"ENERGY\":{}}"
#DATA="{\"PV1\":{}}"
DATA="{\"PM1OBJ1\":{}}"

IP=192.168.9.91

curl -X POST http://$IP/lala.cgi -d $DATA


