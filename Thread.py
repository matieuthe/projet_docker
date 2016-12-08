#!/usr/bin/env python

import sys
import random
from threading import Thread
import time
from Donnes_cpu import *


class Afficheur(Thread):

    def __init__(self, mot):
        Thread.__init__(self)

    def run(self):
    	while 1>0:
			Liste_id = liste_conteneur()
			print nombre_apache(Liste_id)
			print average_usage(Liste_id)
