#Dockerized Rubis Application

##Utilisation de l'application graphique Dockerisation.py
Pour l'utiliser avoir python d'installé.
Télécharger l'api docker pour python

    pip install docker-py

Ne pas oublier de la lancer en root

##Configure the simulation
The configuration file for the emulator is under client/emulator/rubis.properties. You can configure the simulation by playing around with the multiple features available.

##How to run the project
To use the default configuration of the project with a database (MySQL), a server (Apache/PHP), a load-balancer (Nginx) and a client (Java), run the following command after importing my bashrc file.

	dockup

If you want to use another Compose file :

	docker-compose -f [compose file you want to use] up

It creates 3 : a database (MySQL), a server (Apache/PHP), a load-balancer (Nginx). If you want to use Clif as a client simulator, just run Clif, right click on HighClient.ctp, Test Deployment, then Initialize and Start.

In order to use the load-balancer in order to automatically scale you application, run the script auto.sh.

	sh auto.sh 5 #launch the script with a maximum of 5 servers

The results can be found in the load_balancer/results directory.

To clean before another use, make sure you are using the functions of my bashrc file and type the following :
	
	doclean -c
	sh clean.sh

##Choose your compose file
Default configuration for a Dockerized Rubis Appplication. It launches the Rubis emulator.
	docker-compose.yml 

With more CPU allowed to the client and less to the server. You can modify the CPU quota within the file.
	docker-compose.yml.wq

With a client not Dockerized for better performances. You can use Clif, Siege or ApacheBenchmark to create trafic.
	docker-compose.yml.ndc

##Recreate the database
You have two different databases already built for you :
- strebern/mysqlmini is a small database with 10000 users and 600 items. 
- strebern/mysqlfull is bigger database with 100000 users and 7000 items.

But if you need a custom database your can recreate it by deploying by-hand the mysql empty container, the server and the loadbalancer and by de-commenting the 'make && make initDB PARAM=all' in the client Dockerfile.


