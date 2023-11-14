import sys
import os
import pandas as pd

##Notre dossier de travail est celui juste avant le dossier data.

#Récupération des données (protéine et génome)
var = sys.argv
genome = var[1]
proteine = var[2]
my_os_type = var[3]

#Vérification des arguments en entrée:
list_os = ["linux","win","macosx"]

if len(var) != 4:
    sys.exit("Fournir le bon nombre d'arguments svp.")
else:
    if my_os_type not in list_os :
        sys.exit("Fournir un os correct : linux, win ou macosx")

###PARTIE 1:

##Fonctions :
#Fonction récupérant les informations sur la protéine du génome spécifié:

def recup_info_prot(genome,proteine):
    "Fonction récupérant les informations sur une protéine dans le génome spécifié. Premier argument : génome; deuxième argument : protéine"
    ##La gestion d'erreur sert si on exécute le code dans le mauvais dossier de travail ou que le dossier contenant le génome n'existe pas.
    try:
        ##On récupére en dataframe le fichier tsv.
        dataframe = pd.read_csv(f'data/genomes/{genome}/annotation_{genome}.tsv', sep = '\t', index_col = 0)
        ##Si la protéine qu'on a demandé n'est pas dans le génome on break le script, sinon on récupère en dictionaire les infos sur la protéine. A OPTIMISER
        if proteine in set(dataframe["Protein_Id"]):
            list_prot_info = dataframe[dataframe["Protein_Id"] == proteine]
        else:
            sys.exit("La protéine n'est pas contenu dans le génome donné.")
    except FileNotFoundError:
        print("Rentrez un argument correct svp.")
    return list_prot_info

#Fonction récupérant la liste des protéines dans le génome spécifié:

def recup_prot(genome):
    "Fonction récupérant la liste des protéines dans le génome spécifié. Premier argument : génome"
    ##La gestion d'erreur sert si on exécute le code dans le mauvais dossier de travail ou que le dossier contenant le génome n'existe pas.
    try:
         ##On récupére en dataframe le fichier tsv.
        dataframe = pd.read_csv(f'data/genomes/{genome}/annotation_{genome}.tsv', sep = '\t', index_col = 0)
        ##On crée une liste avec toutes les protéines.
        list_prot = list(dataframe.Protein_Id)
    except FileNotFoundError:
        print("Rentrez un argument correct svp.")
    return list_prot


#Fonction récupérant une liste avec les 30 génomes:

def recup_genome(file):
    "Récupération des génomes du fichier rentré en argument."
    ##La gestion d'erreur sert si on exécute le code dans le mauvais dossier de travail.
    try :
        ##On converit le fichier excell en argument en dataframe.
        classeur = pd.read_excel(file)
        ##On récupère seulement les génomes, représentés par le Assembly accesion.
        genom = list(classeur["Assembly Accession"])
    except FileNotFoundError:
        print("Rentrez un argument correct svp.")
    return genom

##Main:

##Si le nombre d'argument est bien de 2 et que le génome existe, 
##alors on récupère les protéines présentes dans celui-ci et on
##récupère les informations sur la protéine demandée.
if genome in recup_genome("data/Ecoli_genomes_refseq.xlsx"):
    liste_proteines = recup_prot(genome)
    list_proteine_info = recup_info_prot(genome,proteine)
else:
    sys.exit("Attention, le génome demandé n'est pas dans les 30 génomes donnés.")
    
#Affichage des demandes :
#print("La liste des différentes protéines du génome est : ", liste_proteines)
print("Les informations sur notre protéine d'intéret sont : ", list_proteine_info) 


###PARTIE 2:
from Bio import SeqIO

#Si on arrive à cette partie c'est que la protéine existe bien dans le génome et qu'on a récupéré les informations dans dict_proteine_info.

##Fonctions:
#Fonction qui récupère la séquence de la protéine du fichier fasta contenant les séquences de toutes les protéines du génome :

def recup_seq(genome,proteine):
    "Fonction récupérant la séquence de la protéine dans le génome spécifié. Premier argument : génome; Deuxième argument : protéine"
    ##On récupère le fichier fasta contenant les séquences du génome donné.
    fasta = SeqIO.parse(f'data/genomes/{genome}/protein.faa', "fasta")
    #On récupère la séquence. A OPTIMISER
    for i in fasta:
        if i.id == proteine:
            seq = i.seq
    return seq


##Main:

sequence = recup_seq(genome,proteine)

print("La séquence de la protéine d'intéret est : ", sequence)

###PARTIE 3: 

##Fonctions:


##Main:

#On récupère les 29 autres génomes de la liste :
list_genome_autre = recup_genome("data/Ecoli_genomes_refseq.xlsx")
list_genome_autre.remove(genome)






