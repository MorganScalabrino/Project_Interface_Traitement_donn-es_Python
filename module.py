#Modules nécessaires:

import sys
import os
import pandas as pd
from Bio import SeqIO
import subprocess
from Bio.Blast import NCBIXML
import platform

##Fonctions de notre module:

#Fonction créeant un dataframe à partir du fichier d'annotation du génome spécifié:
def recup_data(genome):
    """
    Description :
    ------------
        Fonction récupérant le dataframe du fichier d'annotation à du génome donnée en argument.

    Arguments :
    -----------
        genome : string

    Returns :
    ---------
        Retourne le dataframe correspondant.

    """
    ##On récupére en dataframe le fichier tsv.
    dataframe = pd.read_csv(f'data/genomes/{genome}/annotation_{genome}.tsv', sep = '\t')
    dataframe.index += 1
    return dataframe


#Fonction récupérant les informations sur la protéine du génome spécifié:
def recup_info_prot(genome,proteine):
    """
    Description :
    ------------
        Fonction récupérant les informations associée à la protéine et au génome rentrés en argument.

    Arguments :
    -----------
        genome : string , le génome d'intérêt.
        proteine : string , la protéine d'intérêt.

    Returns :
    ---------
        Retourne un dataframe correspondant à la ligne de la protéine du fichier d'annotation.
    """
    ##La gestion d'erreur sert si on exécute le code dans le mauvais dossier de travail ou que le dossier contenant le génome n'existe pas.
    try:
        ##On récupére en dataframe le fichier tsv.
        dataframe = recup_data(genome)
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
    """
    Description :
    ------------
        Fonction récupérant la liste des protéines disponibles dans le génome d'intérêt.
        
    Arguments :
    -----------
        genome : string , le génome d'intérêt.
        
    Returns :
    ---------
        Retourne une liste avec tous les id des protéines du génome d'intérêt.
    """
    ##La gestion d'erreur sert si on exécute le code dans le mauvais dossier de travail ou que le dossier contenant le génome n'existe pas.
    try:
        ##On récupére en dataframe le fichier tsv.
        dataframe = recup_data(genome)
        ##On crée une liste avec toutes les protéines.
        list_prot = list(dataframe.Protein_Id)
    except FileNotFoundError:
        print("Rentrez un argument correct svp.")
    return list_prot


#Fonction récupérant une liste avec les 30 génomes:
def recup_genome(file):
    """
    Description :
    ------------
        Fonction récupérant la liste des 30 génomes par leur Assembly accesion.
        
    Arguments :
    -----------
        file : string , chemin d'accès au fichier, généralement "data/Ecoli_genomes_refseq.xlsx"

    Returns :
    ---------
        Retourne une liste composée des 30 génomes de notre projet.
    """
    ##La gestion d'erreur sert si on exécute le code dans le mauvais dossier de travail.
    try :
        ##On converit le fichier excell en argument en dataframe.
        classeur = pd.read_excel(file)
        ##On récupère seulement les génomes, représentés par le Assembly accesion.
        genom = list(classeur["Assembly Accession"])
    except FileNotFoundError:
        print("Rentrez un argument correct svp.")
    return genom

#Fonction qui récupère la séquence de la protéine du fichier fasta contenant les séquences de toutes les protéines du génome :
def recup_seq(genome,protein):
    """
    Description :
    ------------
        Fonction récupérant l'objet seq_record associé à notre protéine.
        
    Arguments :
    -----------
        genome : string , le génome d'intérêt.
        proteine : string , la protéine d'intérêt.

    Returns :
    ---------
        Retourne un objet seq_record contenant la séquence de notre protéine d'intérêt et son identifiant.

    """
    
    for seq_record in SeqIO.parse(f'data/genomes/{genome}/protein.faa',"fasta"):
        if seq_record.id == protein:
            return(seq_record)
            
#Fonction lançant un blastp pour la protéine sur le génome indiqué:
def blastp(genome,record):
    """
    Description :
    ------------
        Fonction lançant un blastp pour la protéine sur le génome indiqué et créant un fichier xml à partir des résultats.
        
    Arguments :
    -----------
        genome : string , le génome d'intérêt.
        record : objet seq_record, informations sur la protéine étudiée.

    Returns :
    ---------
        Ne retourne rien, crée temporairement un fichier xml jusqu'à délétion dans une autre fonction.
    """
    #On crée le fichier fasta.
    SeqIO.write(record, "proteine.fasta", "fasta")
    
    #Sélection de l'OS.
    l_cmdos = ["data/Blast+/linux/bin/blastp","data/Blast+/win/bin/blastp.exe", "data/Blast+/macosx/bin/blastp"]
    cmdos = l_cmdos[list_os.index(my_os_type)]

    #On définit la commande à run par python.
    cmd_line = [cmdos,"-query","./proteine.fasta","-db","data/genomes/"+genome+"/"+genome,"-evalue","0.001","-out","result.xml","-outfmt", "5"]
    subprocess.run(cmd_line)

#Fonction récupérant le meilleur hit d'un blastp à partir d'un fichier xml contenant ses résultats.
def best_hit(file):
    """
    Description :
    ------------
        Fonction récupérant le meilleur hit, s'il existe, pour des résulats de blastp dans un tableau xml.
        
    Arguments :
    -----------
        file : string, le fichier xml contenant le résultat du blastp.

    Returns :
    ---------
        Retourne le meilleur hit sous forme d'un objet Alignement
    """
    
    with open(file) as handle:
        record = NCBIXML.read(handle)

    #Compteur.
    t = 0
    
    #Au cas où le gène n'est pas sur le gènome.
    result_hit = "Pas de résultat"
    
    for i in record.alignments:
        #Si t = 1 alors on a déja pris le meilleur hit qui est le premier.
        if t == 1:
            break
        else:
            t+=1
        result_hit = i

    #On supprimer le fichier xml du blast.
    os.remove("result.xml")

    #On supprime le fichier fasta crée plus tôt.
    os.remove("proteine.fasta")

    #On renvoie le résultat qui est un objet blast.
    return result_hit

#Fonction cherchant la protéine en amont et en aval de la protéine donnée:

def amont_aval(genome,proteine):
    """
    Description :
    ------------
        Fonction cherchant la protéine en amont et en aval de notre protéine d'intérêt dans notre génome d'intérêt.
        
    Arguments :
    -----------
        genome : string , le génome d'intérêt.
        proteine : string , la protéine d'intérêt.

    Returns :
    ---------
        Retourne une liste avec en premier l'ID de la protéine en amont et en second la protéine en aval.
    """
    
    #On récupére en dataframe le fichier tsv.
    dataframe = recup_data(genome)

    #On récupère la position dans le dataframe de notre protéine.
    position_prot = dataframe[dataframe["Protein_Id"] == proteine].index[0]

    #On fait une boucle pour gérer si la protéine est au début du génome ou à la fin (dans le tableau tsv).
    if position_prot == 1:
        print("Attention votre protéine est sur le premier gène du génome, comme il est circulaire ce n'est pas pénalisant")
        prot1 = dataframe.loc[position_prot + 1]["Protein_Id"]
        prot2 = dataframe.loc[dataframe.shape[0]]["Protein_Id"]
    elif position_prot == dataframe.shape[0]:
        print("Attention votre protéine est sur le dernier gène du génome, comme il est circulaire ce n'est pas pénalisant")
        prot1 = dataframe.loc[1]["Protein_Id"]
        prot2 = dataframe.loc[position_prot - 1]["Protein_Id"]
    else:
        prot1 = dataframe.loc[position_prot + 1]["Protein_Id"]
        prot2 = dataframe.loc[position_prot - 1]["Protein_Id"]

    #On gère le fait qu'un gène en brin + ou - n'a pas les mêmes définitions de aval et amont.
    if list_proteine_info["Strand"][position_prot] == "+":
        proteine_aval = prot1
        proteine_amont = prot2
    else:
        proteine_aval = prot2
        proteine_amont = prot1

    return [proteine_amont, proteine_aval]

#Mane de notre module:

if __name__ == '__main__':
    #Pour calculer le temps que met le script à s'exécuter:
    from datetime import datetime
    start = datetime.now()

    #Récupération des données (protéine et génome)
    var = sys.argv
    genome = var[1]
    proteine = var[2]
    my_os_type = var[3]

    #Vérification des arguments en entrée, l'os est-il bien orthographié.
    list_os = ["linux","win","macosx"]

    if len(var) != 4:
        sys.exit("Fournir le bon nombre d'arguments svp.")
    else:
        if my_os_type not in list_os:
            sys.exit("Fournir un os correct : linux, win ou macosx")
            
    #Vérification des arguments en entrée, l'os est-il correct.
    result_platform = {'linux' : 'Linux' , 'macosx' : 'Darwin' , 'win' : 'Windows'} 
    
    if platform.system() != result_platform[my_os_type]:
        sys.exit(f"Fournir votre os, qui est : {platform.system()}")

    
    ##Si le nombre d'argument est bien de 2 et que le génome existe, 
    #alors on récupère les protéines présentes dans celui-ci et on
    #récupère les informations sur la protéine demandée.
    if genome in recup_genome("data/Ecoli_genomes_refseq.xlsx"):
        liste_proteines = recup_prot(genome)
        list_proteine_info = recup_info_prot(genome,proteine)
    else:
        sys.exit("Attention, le génome demandé n'est pas dans les 30 génomes donnés.")
        
    #Vérification.
    #print("La liste des différentes protéines du génome est : ", liste_proteines)
    print("Les informations sur notre protéine d'intéret sont : ", list_proteine_info)
    
    #On récupère la séquence de notre protéine d'intérêt dans notre génome d'intérêt avec quelques informations.
    record = recup_seq(genome,proteine)
    
    #Vérification.
    print("La séquence de la protéine d'intéret est : ", record.seq)
    
    #On récupère les 29 autres génomes de la liste :
    list_genome_autre = recup_genome("data/Ecoli_genomes_refseq.xlsx")
    list_genome_autre.remove(genome)
    
    #Dictionnaire contenant les génomes et l'objet Alignement associé au Blastp.
    dict_besthit_proteine = {}
    
    for genom in list_genome_autre:
        #On blast sur l'un des 29 génomes.
        blastp(genom,record)

        #Meilleur résultat.
        hit = best_hit("result.xml")

        dict_besthit_proteine[genom] = hit
    
    
    #Vérification :
    print("Les résultats du blast sur notre protéine sont", dict_besthit_proteine)
    
    print("Par exemple, la protéine, d'ID :", proteine ,"sur le génome de référence :",genome,"a un hit sur le génome:",list_genome_autre[5], "et l'id de cette protéine est alors",   dict_besthit_proteine[list_genome_autre[5]].hit_id,"dans ce génome.")
    
    #On définit la protéine en amont et en aval.
    proteine_amont = amont_aval(genome,proteine)[0]
    proteine_aval = amont_aval(genome,proteine)[1]
    
    #Vérification.
    print("La protéine en amont est", proteine_amont)
    print("Les informations sur la protéine en amont sont :", recup_info_prot(genome,proteine_amont))
    
    print("La protéine en aval est", proteine_aval)
    print("Les informations sur la protéine en amont sont :", recup_info_prot(genome,proteine_aval))
    
    #Pour la protéine en amont, même procédé qu'en partie 3:
    record_amont = recup_seq(genome,proteine_amont)
    
    dict_besthit_proteine_amont = {}
    
    for genom in list_genome_autre:
        #On blast sur l'un des 29 génomes.
        blastp(genom,record_amont)

        #Meilleur résultat.
        hit = best_hit("result.xml")

        dict_besthit_proteine_amont[genom] = hit
    
    
    #Pour la proteine en aval, même procédé qu'avant.
    record_aval = recup_seq(genome,proteine_aval)
    
    dict_besthit_proteine_aval = {}
    
    for genom in list_genome_autre:
        #On blast sur l'un des 29 génomes.
        blastp(genom,record_aval)


        #Meilleur résultat.
        hit = best_hit("result.xml")

        dict_besthit_proteine_aval[genom] = hit
    
    
    
    #Vérification :
    #print("Les résultats du blast sur notre protéine en amont sont", dict_besthit_proteine_amont)
    
    print("Par exemple, la protéine en amont, d'ID :", proteine_amont ,"sur le génome de référence :",genome,"a un hit sur le génome:",list_genome_autre[5], "et l'id de cette protéine est alors",   dict_besthit_proteine_amont[list_genome_autre[5]].hit_id,"dans ce génome.")
    
    #print("Les résultats du blast sur notre protéine en aval sont", dict_besthit_proteine_aval)
    
    print("Par exemple, la protéine en aval, d'ID :", proteine_aval ,"sur le génome de référence :",genome,"a un hit sur le génome:",list_genome_autre[5], "et l'id de cette protéine est alors",   dict_besthit_proteine_aval[list_genome_autre[5]].hit_id,"dans ce génome.")
    
    #On fait un dictionnaire avec des listes avec les informations sur les meilleurs hit du blast sur la protéine d'intérêt: 
    
    dict_proteine_info = {}
    
    for i in dict_besthit_proteine:
        
        #On gère si jamais le blastp n'avait pas eu de hit.
        if dict_besthit_proteine[i] != "Pas de résultat":
            list_proteine_info = recup_info_prot(i,dict_besthit_proteine[i].hit_id[4:-1])
            dict_proteine_info[i] = list_proteine_info
        else:
            dict_proteine_info[i] = "Pas de résultat"
            
    print(dict_proteine_info)

    #On fait un dictionnaire avec des listes avec les informations sur les meilleurs hit du blast sur la protéine en amont de celle d'intérêt: 
    
    dict_proteine_amont_info = {}
    
    for i in dict_besthit_proteine_amont:
        
        #On gère si jamais le blastp n'avait pas eu de hit.
        if dict_besthit_proteine_amont[i] != "Pas de résultat":
            list_proteine_amont_info = recup_info_prot(i,dict_besthit_proteine_amont[i].hit_id[4:-1])
            dict_proteine_amont_info[i] = list_proteine_amont_info
        else:
            dict_proteine_amont_info[i] = "Pas de résultat"
            
    print(dict_proteine_amont_info)

    #On fait un dictionnaire avec des listes avec les informations sur les meilleurs hit du blast sur la protéine en aval de celle d'intérêt: 
    
    dict_proteine_aval_info = {}
    
    for i in dict_besthit_proteine_aval:

        #On gère si jamais le blastp n'avait pas eu de hit.
        if dict_besthit_proteine_aval[i] != "Pas de résultat":
            list_proteine_aval_info = recup_info_prot(i,dict_besthit_proteine_aval[i].hit_id[4:-1])
            dict_proteine_aval_info[i] = list_proteine_aval_info
        else:
            dict_proteine_aval_info[i] = "Pas de résultat"
            
    print(dict_proteine_aval_info)

    #Pour connaître le temps à qu'a mis le script à run:
    difference = datetime.now() - start
    print("Le script s'est effectué en",difference)

    #On rajoute le génome de référence et ses informations dans les 3 dictionnaires.
    dict_proteine_info[genome] = list_prot_info
    dict_proteine_amont_info[genome] = list_proteine_amont_info
    dict_proteine_aval_info[genome] = list_proteine_aval_info
