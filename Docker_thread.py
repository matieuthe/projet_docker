#!/usr/bin/python

try:
    # for Python2
    from Tkinter import *   	## notice capitalized T in Tkinter 
except ImportError:
    # for Python3
    from tkinter import *   	## notice lowercase 't' in tkinter here

import os 			#Pour executer des commandes systemes
from threading import Thread	#Pour l'affichage en temps reel
import time			#Pour la gestion du temps
from docker import Client 	#Pour docker

class Afficheur(self,Thread):
		def __init__(self):
			Thread.__init__(self)
			self.heure = StringVar()

	   	def run(self):
			self.heure.set(time.strftime('%H:%M:%S'))

class Interface(Frame):
    
	def __init__(self, fenetre, **kwargs):
		Frame.__init__(self, fenetre, width=768, height=576, **kwargs)
		self.Afficheur()
		self.pack(fill=BOTH)
		self.cli = Client(base_url='unix://var/run/docker.sock')
		
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
	
		#Second onglet
		ong2 = LabelFrame(self, text="Lancement manuel", padx=200, pady=20)
		ong2.pack(fill="both", expand="yes")

	
		ong2.bouton_docker = Button(ong2, text="Lancement de docker", command=self.choisir)
		ong2.bouton_docker.pack(side="left")

		#Pour lancer le script de gestion des conteneurs
		ong2.bouton_auto = Button(ong2, text="Lancement du script auto", command=self.script)
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
		cmd = "docker-compose up&"
		os.system(cmd)

	def run_non(self):
		cmd = "docker-compose -f docker-compose.yml.ndc up&"
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
	def lib80(self):
		cmd = "sudo fuser -k 80/tcp&"
		os.system(cmd)
	
	def maj(self):
		#threading.Timer(5.0, maj).start()
		# on arrive ici toutes les 1000 ms
		
		self.nbConteneur.set(0)
		#Recupere tous les conteneurs
		conteneurs = self.cli.containers()
		variable = 0

		Liste_id = []
		#On recupere l'id des conteneurs apache et on les mets dans Liste_id
		for cont in conteneurs:
			if cont['Image']=="dockerizedrubis_apache":
				variable+=1
				Liste_id.append(cont['Id'])

		self.nbConteneur.set(variable)
		
		os.system("docker stats --no-stream > .donnes.txt")
		
		#Creation du tableau avec les valeurs de cpu
		valeur_cpu = 0
		#Recupere la puissance cpu necessaire au fonctionnement de chaque conteneur apache
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
					valeur_cpu += float(cpu)
		
		if variable > 0:
			valeur_cpu = valeur_cpu/variable

		self.charge_moyenne.set(valeur_cpu)

		#Fin de la fonction maj

fenetre = Tk()
interface = Interface(fenetre)
interface.mainloop()
interface.destroy()
