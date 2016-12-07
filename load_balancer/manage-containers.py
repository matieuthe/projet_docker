#!/usr/bin/python

from docker import Client 	#Pour docker
from shutil import copyfile	#Pour copier des fichiers
import sys					#Pour recuperer le parametre d'appel
import os					#Pour les commandes systèmes


cli = Client(base_url='unix://var/run/docker.sock')

#********************************#
#   obtenir le nombre de noeud   #
#********************************#

#Recupere tous les conteneurs
conteneurs = cli.containers()

#Recupere tous les conteneurs
conteneurs = cli.containers()

compteur = 0
#On compte le nombre de conteneurs apache et on les mets dans Liste_id
for cont in conteneurs:
	if cont['Image']=="dockerizedrubis_apache":
		compteur+= 1

copyfile("./load_balancer/new.conf", "./load_balancer/nginx.conf")

if sys.argv[1] == "add":
	compteur += 1
	endIP = compteur + 3
	os.system("sed \"9i\\\nserver 172.17.0.$endIP:80 max_fails=3 fail_timeout=30s;\n\" ./load_balancer/nginx.conf > ./load_balancer/new.conf" )

elif sys.argv[1] == "remove":
	compteur -= 1	
	os.system("sed '9d' ./load_balancer/nginx.conf > ./load_balancer/new.conf")

else:
	print "Wrong parameter, try with 'add' or 'remove' ... "

#Tell Docker the new size of our server cluster
os.system("docker-compose scale apache="+compteur)
#Paste the new configuration file in the running container
os.system("docker cp ./load_balancer/new.conf $(docker ps -f \"name=dockerizedrubis_nginx\" -q ):/etc/nginx/nginx.conf")
#Graceful restart
os.system("docker exec $(docker ps -f \"name=dockerizedrubis_nginx\" -q) bash -c 'kill -HUP $(cat /run/nginx.pid)'")./load_balancer/