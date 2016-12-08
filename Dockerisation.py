#!/usr/bin/env python

try:
    # for Python2
    from Tkinter import *   	## notice capitalized T in Tkinter 
except ImportError:
    # for Python3
    from tkinter import *   	## notice lowercase 't' in tkinter here

import os 						#Pour executer des commandes systemes
from threading import Thread	#Pour l'affichage en temps reel
import time						#Pour la gestion du temps
from scriptDocker.Donnes_cpu import *


class Interface(Frame):
    
	def __init__(self, fenetre, **kwargs):
		Frame.__init__(self, fenetre, width=768, height=576, **kwargs)
		self.pack(fill=BOTH)
		
		fenetre.title('Dockerisation de rubis')

		#Menu de la fenetre
		fenetre.iconbitmap("@./image/docker.xbm")
		menubar = Menu(fenetre)

		menu1 = Menu(menubar, tearoff=0)

		menu1.add_separator()
		menu1.add_command(label="Quitter", command=self.quit)
		menubar.add_cascade(label="Fichier", menu=menu1)

		menu2 = Menu(menubar, tearoff=0)
		menu2.add_command(label="Enregister donnees script", command=self.quit)
		menubar.add_cascade(label="Editer", menu=menu2)

		menu3 = Menu(menubar, tearoff=0)
		menu3.add_command(label="Liberer port 80", command=self.lib80)
		menubar.add_cascade(label="Outils", menu=menu3)

		fenetre.config(menu=menubar)
	
		#Premiere onglet
		ong1 = LabelFrame(self, text="Choix du type de client", padx=200, pady=20)
		ong1.pack(fill="both", expand="yes")

		self.choix = IntVar()
		choix_base = Radiobutton(ong1, text="Client dockerise", variable=self.choix, value=0)
		choix_clif = Radiobutton(ong1, text="Client non dockerise(Clif, Apache Benchmark...)", variable=self.choix, value=1)

		choix_base.pack(side ="left")
		choix_clif.pack(side ="left")
		

		#Choix du script
		sc = LabelFrame(self, text="Choix du type de client", padx=200, pady=20)
		sc.pack(fill="both", expand="yes")

		self.choix_script = IntVar()
		choix_script_base = Radiobutton(sc, text="script de base", variable=self.choix_script, value=0)
		choix_script_ameliore = Radiobutton(sc, text="script ameliore", variable=self.choix_script, value=1)

		choix_script_base.pack(side ="left")
		choix_script_ameliore.pack(side ="left")


		#Second onglet
		ong2 = LabelFrame(self, text="Lancement manuel", padx=200, pady=20)
		ong2.pack(fill="both", expand="yes")

	
		ong2.bouton_docker = Button(ong2, text="Lancement de docker", command=self.choisir)
		ong2.bouton_docker.pack(side="left")

		#Pour lancer le script de gestion des conteneurs
		ong2.bouton_auto = Button(ong2, text="Lancement du script auto", command=self.choisir_script)
		ong2.bouton_auto.pack(side="right")

		#Troisieme Onglet
		ong3 = LabelFrame(self, text="Stopper la simulation", padx=200, pady=20)
		ong3.pack(fill="both", expand="yes")

		#Pour arreter docker et le scrip
		ong3.bouton_stopper = Button(ong3, text="Arreter la simulation", command=self.stop)
		ong3.bouton_stopper.pack()

		#4e Onglet ==> Affichage en temps reel
		ong4 = LabelFrame(self, text="Donnees Conteneurs", padx=200, pady=0)
		ong4.pack(fill="both", expand="yes")
	
		ong4.bouton_heure = Button(ong4, text="Actualiser", command=self.maj)
		ong4.bouton_heure.pack(side="left")
		
		self.heure = StringVar()
		self.heure.set(time.strftime('%H:%M:%S'))	#Initialisation de heure
		Label(ong4,text="Heure :").pack(padx=10, pady=10)
		Label(ong4,textvariable=self.heure).pack(padx=20, pady=0)
		
		self.nbConteneur = StringVar()
		self.nbConteneur.set("0")			#Initialisation de nbConteneur
		Label(ong4,text="nombre de conteneur :").pack(padx=10, pady=10)
		Label(ong4,textvariable=self.nbConteneur).pack(padx=20, pady=0)

		self.charge_moyenne = StringVar()
		self.charge_moyenne.set("0")			#Initialisation de la charge moyenne
		Label(ong4,text="Charge moyenne :").pack(padx=10, pady=10)
		Label(ong4,textvariable=self.charge_moyenne).pack(padx=20, pady=0)

  		
	def runner(self):
		cmd = "docker-compose -f ./compose_file/docker-compose.yml up&"
		os.system(cmd)

	def run_non(self):
		cmd = "docker-compose -f ./compose_file/docker-compose.yml.ndc up&"
		os.system(cmd)

	def script(self):
		cmd = "sudo ./script_auto.py&"
		os.system(cmd)

	def stop(self):
		cmd = "docker rm -f $(docker ps -a -q)&"
		os.system(cmd)

	def choisir(self):
		if self.choix.get()==0:
			cmd = "docker-compose up&"
			os.system(cmd)
		elif self.choix.get()==1:
			cmd = "docker-compose -f docker-compose.yml.ndc up&"
			os.system(cmd)	

	def choisir_script(self):
		if self.choix_script.get()==0:
			cmd = "sudo ./script_auto.py&"
			os.system(cmd)
		elif self.choix_script.get()==1:
			cmd = "sudo ./script_modif.py&"
			os.system(cmd)		

	def lib80(self):
		cmd = "sudo fuser -k 80/tcp&"
		os.system(cmd)
	
	def maj(self):
	
		self.heure.set(time.strftime('%H:%M:%S'))
		
		Liste_id = liste_conteneur()
		
		self.nbConteneur.set(nombre_apache(Liste_id))

		self.charge_moyenne.set(average_usage(Liste_id))


fenetre = Tk()
interface = Interface(fenetre)
interface.mainloop()
interface.destroy()
