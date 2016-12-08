#!/usr/bin/env python

import time			#Pour recuperer la date et l'heure
import os.path			#Pour la manipulation de fichier
from shutil import copyfile	#Pour copier des fichiers
from Donnes_cpu import *

#verification de la presence du fichier de conf
if os.path.isfile("../load_balancerad_balancer/nginx.conf.old"):
	os.rename("../load_balancer/nginx.conf.old", "../load_balancer/nginx.conf")

copyfile("../load_balancer/nginx.conf", "../load_balancer/nginx.conf.old")
copyfile("../load_balancer/nginx.conf", "../load_balancer/new.conf")

#Temps de debut du programme
temps = time.time()

#Creation du fichier de sauvegarde
sauvegarde = open("../load_balancer/results/"+str(round(temps))+".csv","w")
sauvegarde.write("temps;charge;nb_conteneur\n")
sauvegarde.close()

nb_cont = 1
up_or_down = 0

#Boucle infinie
while nb_cont>0:
	
	#Tableau contenant l'id des conteneurs 
	Liste_id = liste_conteneur()

	#Creation du tableau avec les valeurs de cpu
	Liste_cpu = usage(Liste_id)

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

	
	print nb_cont
	#Pour eviter division par 0 si aucun conteneur ne tourne
	if nombre == 0:
		nb_cont = 0
		nombre = 1

	charge = somme/nombre
	#nombre de conteneur
	print "nombre de conteneur : ",nombre
	#charge moyenne par conteneur
	print "charge  moyenne :",charge
	print""
	
	#Obliger d'ouvrir et de fermer a chaque fois sinon pas d'ecriture dans le fichier
	sauvegarde = open("../load_balancer/results/"+str(round(temps))+".csv","a")

	#On ecrit les donnees dans unn fichier csv
	sauvegarde.write(str(val_temps)+";"+str(charge)+";"+str(nombre)+"\n")
	sauvegarde.close()
	
	if (charge < 60 and charge > 15):
		up_or_down = 0

	#Politique
	if (charge >= 60 and nombre >= 1):
		if up_or_down == 0:
			up_or_down = 1
			#time.sleep(2)
		elif up_or_down == 1:
			up_or_down = 0
			if charge > 100:
				cmd = "sudo sh ./manage-containers.sh \"add\""
				os.system(cmd)
			cmd = "sudo sh ./manage-containers.sh \"add\""
			os.system(cmd)
	
	if (charge <=15 and nombre > 1):
		if up_or_down == 0:
			up_or_down = -1
			time.sleep(2)
		elif up_or_down == -1:
			up_or_down = 0
			cmd = "sudo sh ./manage-containers.sh \"remove\""
			os.system(cmd)


