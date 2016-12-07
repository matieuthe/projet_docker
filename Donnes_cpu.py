#!/usr/local/bin/env python

import os 						#Pour executer des commandes systemes
import re						#Pour les expressions regulieres
from docker import Client 		#Pour docker


def average_usage(Liste_id):
	Cpu = usage(Liste_id)
	compteur = 0
	valeur = 0
	for cp in Cpu:
		compteur+=1
		valeur+=cp
	
	if compteur > 0:
		valeur = valeur/compteur
	
	return valeur

def usage(Liste_id):

	os.system("docker stats --no-stream > .donnes.txt")
				
	Liste_cpu = []

	for ligne in Liste_id:

		fichier_CPU = open(".donnes.txt","r")
		
		#Recupere seulement les premiers caracteres de l'id du conteneur
		debut_ligne = re.sub(r".{56}$","", ligne)
	
		for valeur in fichier_CPU:
		
		#Si l'id du conteneur est dans la ligne on recupere la charge du cpu
			if re.match(debut_ligne, valeur) is not None:
				cpu_deb = re.sub(r"^.{12}[ 	]+","",valeur)
				cpu_fin = re.sub(r"[^%]+$","",cpu_deb)
				cpu_re = re.sub(r"%$","",cpu_fin)
				cpu = re.sub(r"%[^%]+$","",cpu_re)
				Liste_cpu.append(float(cpu))
		
	return Liste_cpu
	
def liste_conteneur():
	cli = Client(base_url='unix://var/run/docker.sock')
	#Recupere tous les conteneurs
	conteneurs = cli.containers()

	Liste_id = []
	#On recupere l'id des conteneurs apache et on les mets dans Liste_id
	for cont in conteneurs:
		regexp = r"(^[a-zA-Z0-9._-]+apache)"
		if re.match(regexp,cont['Image']) is not None:
			Liste_id.append(cont['Id'])

	return Liste_id

def nombre_apache(Liste_id):
	compteur = 0
	for cont in Liste_id:
		compteur+= 1
	return compteur