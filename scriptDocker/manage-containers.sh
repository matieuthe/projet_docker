#!/bin/bash

#Get the actual number of nodes
docker ps -f "name=dockerizedrubis_apache" -q > tmp.txt
compteur=$(wc -l tmp.txt)
compteur="$(echo $compteur | head -c 1)"

#Actualize the actual configuration
cat ../load_balancer/new.conf > ../load_balancer/nginx.conf

if [ "$1" = "add" ]
then
	#Increase node count
	compteur=$(($compteur+1))
	endIP=$(($compteur+3)) # +4 because to match the order of container creation

	#Create the new configuration file for nginx, adding a node to the 9th line of the file
	sed "9i\
			server 172.17.0.$endIP:80 max_fails=3 fail_timeout=30s;
	" ../load_balancer/nginx.conf > ../load_balancer/new.conf


elif [ "$1" = "remove" ]
then
	compteur=$(($compteur-1))
	#Delete the 9th line of the configuration file, corresponding to the last node created
	sed '9d' ../load_balancer/nginx.conf > ../load_balancer/new.conf

else
	echo "Wrong parameter, try with 'add' or 'remove' ... "
fi

#Tell Docker the new size of our server cluster
docker-compose scale apache=$compteur
#Paste the new configuration file in the running container
docker cp ../load_balancer/new.conf $(docker ps -f "name=dockerizedrubis_nginx" -q ):/etc/nginx/nginx.conf
#Graceful restart
docker exec $(docker ps -f "name=dockerizedrubis_nginx" -q) bash -c 'kill -HUP $(cat /run/nginx.pid)'

#Remove temporary files 
rm tmp.txt
