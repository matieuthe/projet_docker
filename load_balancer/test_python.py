#!/usr/bin/python

import time			#Pour recuperer la date et l'heure
import os.path			#Pour la manipulation de fichier
import re			#Pour les expressions regulieres
from shutil import copyfile	#Pour copier des fichiers
from docker import Client 	#Pour docker


cli = Client(base_url='unix://var/run/docker.sock')

#verification de la presence du fichier de conf
if os.path.isfile("nginx.conf.old"):
	os.rename("nginx.conf.old", "nginx.conf")

copyfile("nginx.conf", "nginx.conf.old")
copyfile("nginx.conf", "new.conf")

#Temps de debut du programme
temps = time.time()

#Creation du fichier de sauvegarde
sauvegarde = open("results/"+str(round(temps))+".csv","w")
sauvegarde.write("temps;charge;nb_conteneur\n")
sauvegarde.close()

#Boucle infinie
while True:
	#Recupere tous les conteneurs
	conteneurs = cli.containers()

	#Dans l'ideal il faudrait recuperer seulement la valeur du CPU pour chaque conteneur
	#comme pour le premier noeud 
	os.system("docker stats --no-stream > log.txt")
	
	#Tableau contenant l'id des conteneurs 
	Liste_id = []
	
	#On recupere l'id des conteneurs apache et on les mets dans Liste_id
	for cont in conteneurs:
		if cont['Image']=="dockerizedrubis_apache":
			Liste_id.append(cont['Id'])

	#Creation du tableau avec les valeurs de cpu
	Liste_cpu = []

	#Recupere la puissance cpu necessaire au fonctionnement de chaque conteneur apache
	for ligne in Liste_id:

		fichier_CPU = open("log.txt","r")

		#Recupere seulement les premiers caracteres de l'id du conteneur
		debut_ligne = re.sub(r".{56}$","", ligne)
	
		for valeur in fichier_CPU:
			#Si l'id du conteneur est dans la ligne on recupere la charge du cpu
			if re.match(debut_ligne, valeur) is not None:
    				cpu_deb = re.sub(r"^.{12}[ 	]+","",valeur)
				cpu_fin = re.sub(r"[^%]+$","",cpu_deb)
				cpu_re = re.sub(r"%$","",cpu_fin)
				cpu = re.sub(r"%[^%]+$","",cpu_re)
				Liste_cpu.append(cpu)

	somme = 0
	nombre = 0
	charge = 0
	compteur = 1

	#temps ecouler en seconde depuis le debut du lancement du programme
	val_temps = time.time() - temps
	print "temps :", val_temps," secondes"
	
	#affiche la charge de tous les conteneurs apaches
	for val in Liste_cpu:
		print compteur," ==> ",val
		somme +=float(val)
		nombre +=1
		compteur +=1

	#Pour eviter division par 0 si aucun conteneur ne tourne
	if nombre == 0:
		nombre = 1

	charge = somme/nombre
	#nombre de conteneur
	print "nombre de conteneur : ",nombre
	#charge moyenne par conteneur
	print "charge  moyenne :",charge
	print""
	
	#Obliger d'ouvrir et de fermer a chaque fois sinon pas d'ecriture dans le fichier
	sauvegarde = open("results/"+str(round(temps))+".csv","a")

	#On ecrit les donnees dans unn fichier csv
	sauvegarde.write(str(val_temps)+";"+str(charge)+";"+str(nombre)+"\n")
	sauvegarde.close()

	#Politique
	if (charge >= 60 and nombre >= 1):
		cmd = "sudo sh manage-containers.sh \"add\""
		os.system(cmd)
	
	if (charge <=15 and nombre > 1):
		cmd = "sudo sh manage-containers.sh \"remove\""
		os.system(cmd)


