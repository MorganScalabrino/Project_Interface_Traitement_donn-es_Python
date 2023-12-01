import tkinter as tk
from tkinter import ttk
import random as rd
import os
import sys
from threading import Thread
import module_vraidevrai
import tkinter as tk
from PIL import Image, ImageTk
 
class StdoutRedirector(object):
    def __init__(self, text_widget):
        self.text_widget = text_widget
 
    def write(self, s):
        self.text_widget.insert('end', s)
        self.text_widget.see('end')

class Appli(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.height = 650
        self.width = 1000
        self.genome_var=tk.StringVar()
        self.protein_var=tk.StringVar()
        self.os_var=tk.StringVar()
        self.loading=False
        self.creer_widgets()

    def creer_widgets(self):
        """
        #Colorer la frame ou on renseigne les données à voir plus tard
        self.canv = tk.Canvas(self, bg="red", height=self.height, width=self.width)
        self.canv.place(x=0, y=0)

        # Frame for the right side of the window
        right_frame = tk.Frame(self, bg="cyan", width=self.width, height=self.height)
        right_frame.place(x=400, y=0)
        right_frame.pack_propagate(False) 
        """
        
        # boutons
        self.intro = tk.Label(self, text="Choix des paramètres:",font=('arial',25, 'bold'))
        self.genome = tk.Label(self,bg="cyan", text="Genome",font=('arial',20, 'bold'))
        self.protein= tk.Label(self, text="Protein",font=('arial',20, 'bold'))
        self.os = tk.Label(self, text="OS",font=('arial',20, 'bold'))
        self.genome_entry = tk.Entry(self,textvariable = self.genome_var, bd=5,font=('arial',25,'normal'))
        self.protein_entry = tk.Entry(self,textvariable = self.protein_var, bd=5,font=('arial',25,'normal'))
        self.os_set=ttk.Combobox(self,values=module_vraidevrai.get_list_os(),font=('arial',25,'normal'))
        self.os_set.current(0)
        self.submit_btn=tk.Button(self,text = 'Submit',bg="#CAFF70", font=('arial',25),height= 2, width=10,command = self.submit)

        self.intro.pack(side=tk.TOP)
        self.genome.pack(side=tk.TOP)
        self.genome_entry.pack(side=tk.TOP)
        self.protein.pack(side=tk.TOP)
        self.protein_entry.pack(side=tk.TOP)
        self.os.pack(side=tk.TOP)
        self.os_set.pack(side=tk.TOP)
        self.submit_btn.pack(side=tk.TOP)

        self.bouton_quitter = tk.Button(self, text="Quitter",
                                        command=self.quit)
        self.bouton_quitter.pack(side=tk.BOTTOM)
        
    def submit(self):
        self.genome_use = self.genome_var.get()
        self.protein_use = self.protein_var.get()
        self.os_use = self.os_set.get()

        if self.genome_use in os.listdir('./data/genomes') and self.protein_use in module_vraidevrai.recup_prot(self.genome_use):
            
            print("Genome chosen : " + self.genome_use)
            print("Protein chosen : " + self.protein_use)
            print("OS chosen : " + self.os_use)

            self.genome_var.set("")
            self.protein_var.set("")

            self.textbox = tk.Text(self.canv, wrap='word',height=45,bg="#CAFF70") #char pour couper au carac, word pour couper au mot
            self.textbox.pack()
            self.textbox.configure(font=("arial", 20, "italic"))
 
            ## Voici le truc, on pointe le sys.stdout vers le textbox
            sys.stdout = StdoutRedirector(self.textbox)
            print("zebiiiiiiiiiii")
        else:
            self.err=tk.Label(self,text="Au moins un des arguments est incorrect")
            self.err.pack()


            thread.join()

if __name__ == "__main__":
    app = Appli()
    app.title("BLAST Interface")
    app.mainloop()
