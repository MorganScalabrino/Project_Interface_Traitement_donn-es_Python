# -*- coding: utf-8 -*-
"""
Created on Sun Nov 19 15:35:05 2023

@author: user
"""
#GCF_001566615.1
#'WP_000241659.1'
#https://www.plus2net.com/python/tkinter-colors.php

import tkinter as tk
from tkinter import ttk
import random as rd
import os
import sys
from threading import Thread
import module
import tkinter as tk
from PIL import Image, ImageTk


#Classe ajoutée pour lancer l'analyse en parallèle du script
class StdoutRedirector(object):
    def __init__(self, text_widget):
        self.text_widget = text_widget
 
    def write(self, s):
        self.text_widget.insert('end', s)
        self.text_widget.see('end')
    #fonction primordiale pour l'execution sur Windows uniquement
    def flush(self):
        pass

class Appli(tk.Tk):
    """
    Création de la classe Appli


    """
    def __init__(self):
        """
        Initialisation de la fenêtre graphique
        """
        tk.Tk.__init__(self)
        self.height = 650
        self.width = 800
        self.genome_var=tk.StringVar()
        self.protein_var=tk.StringVar()
        #La fenêtre s'affiche avec les widgets 
        self.creer_widgets()

    def creer_widgets(self):

    
        #Création du canvas (fenêtre graphique à gauche)
        self.canv = tk.Canvas(self, bg="#CDFAF6", height=self.height,width=self.width)
        self.canv.pack(side=tk.LEFT)


        
        #Définition des widgets demandant l'entrée des paramètres
        self.intro = tk.Label(self, text="Choix des paramètres:",font=('arial',25, 'bold'))
        self.genome = tk.Label(self, text="Genome",font=('arial',20, 'bold'))
        self.protein= tk.Label(self, text="Protein",font=('arial',20, 'bold'))
        self.os = tk.Label(self, text="OS",font=('arial',20, 'bold'))
        self.genome_entry = tk.Entry(self,textvariable = self.genome_var, bd=5,font=('arial',25,'normal'))
        self.protein_entry = tk.Entry(self,textvariable = self.protein_var, bd=5,font=('arial',25,'normal'))
        self.os_set=ttk.Combobox(self,values=module.get_list_os(),font=('arial',25,'normal'))
        self.os_set.current(0)
        self.submit_btn=tk.Button(self,text = 'Submit',bg="#CDFAF6", font=('arial',25),height= 2, width=10,command = self.submit)

        #Fonction qui affiche des widgets définis au-dessus. On pack dans l'ordre d'affichage de haut en bas
        self.intro.pack(side=tk.TOP)
        self.genome.pack(side=tk.TOP)
        self.genome_entry.pack(side=tk.TOP)
        self.protein.pack(side=tk.TOP)
        self.protein_entry.pack(side=tk.TOP)
        self.os.pack(side=tk.TOP)
        self.os_set.pack(side=tk.TOP)
        self.submit_btn.pack(side=tk.TOP)
        
    def submit(self):
        """
        Description:
        Bouton qui lance l'analyse de synténie. On s'assure de la validité des paramètres.
        """
        #On stocke les variables entrées par l'utilisateur
        self.genome_use = self.genome_var.get()
        self.protein_use = self.protein_var.get()
        self.os_use = self.os_set.get()

        #On s'assure que le génome est dans notre data et que la protéine est bien présente dans ce génome
        if self.genome_use in os.listdir('./data/genomes') and self.protein_use in module.recup_prot(self.genome_use):
            
            print("Genome chosen : " + self.genome_use)
            print("Protein chosen : " + self.protein_use)
            print("OS chosen : " + self.os_use)

            #On créé une zone de texte où l'on affichera les résultats de notre analyse
            self.textbox = tk.Text(self.canv, wrap='word',height=45,bg="#CDFAF6") #char pour couper au carac, word pour couper au mot
            self.textbox.pack()
            self.textbox.configure(font=("arial", 20, "italic"))
 
            #On redirige la sortie standard du script vers la textbox
            sys.stdout = StdoutRedirector(self.textbox)

            #On effectue l'analyse de synténie en parallèle de la fenêtre graphique
            thread = Thread(target = module.main(self.genome_use,self.protein_use,self.os_use))
            thread.start() 


            #On ouvre le fichier illustrant notre analyse de synténie 
            image = Image.open('synt.png')
            image.show()
        else:
            self.canv.create_text((400,self.height/2),text="Au moins un des arguments est incorrect",font=('arial','25','bold'),fill='red')






if __name__ == "__main__":
    app = Appli()
    app.title("Synteny Analysis Interface")
    app.mainloop()

