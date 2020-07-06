# index.py

from random import randint
from datetime import datetime
import time
from threading import Thread
import sys
import select
import json
import os.path
from os import path
from json.decoder import JSONDecodeError
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import csv

class TimeoutExpired(Exception):
    pass

# Regarde si le timeout est depasse
def input_with_timeout(prompt, timeout):
    sys.stdout.write(prompt)
    sys.stdout.flush()
    ready, _, _ = select.select([sys.stdin], [], [], timeout)
    if ready:
        return sys.stdin.readline().rstrip('\n')  # expect stdin to be line-buffered
    raise TimeoutExpired

# Retourne le nombre de coup max selon le niveau
def coupParLevel(level):
    if level == 1:
        nb_coup = 3
    elif level == 2:
        nb_coup = 5
    elif level == 3:
        nb_coup = 7

    return nb_coup

# Retourne le nombre max pour le chiffre aleatoire
def rangeParLevel(level):
    if level == 1:
        range = 10
    elif level == 2:
        range = 20
    elif level == 3:
        range = 30

    return range

# Retourne le gain gagne
def gainUser(coup, mise, level):
    if coup == 1:
        if level == 1:
            gain = mise * 2
        elif level == 2:
            gain = mise * 3
        elif level == 3:
            gain = mise * 5
    if coup == 2:
        if level == 1:
            gain = mise + mise * 1
        elif level == 2:
            gain = mise + mise * 1.25
        elif level == 3:
            gain = mise + mise * 1.5
    if coup >= 3:
        if level == 1:
            gain = mise + mise * 0.25
        elif level == 2:
            gain = mise + mise * 0.50
        elif level == 3:
            gain = mise + mise * 0.75
    return float(gain)

# Retour les regles du jeu
def regle():
    str = """Je vous explique le principe du jeu :  \n
Je viens de penser à un nombre entre 1 et 10. Devinez lequel ?\n 
Attention : vous avez le droit à trois essais ! \n 
\t* Si vous devinez mon nombre dès le premier coup:
\t- au niveau 1 vous doublez votre mise !!
\t- au niveau 2 vous triplez votre mise !!!
\t- au niveau 3 vous quintuplez votre mise !!!!!\n
\t* Si vous le devinez au 2è coup
\t- au niveau 1 vous gagnez exactement votre mise !
\t- au niveau 2 vous gagnez votre mise + 25% de votre mise
\t- au niveau 3 vous gagnez votre mise + 50% de votre mise\n
\t* Si vous le devinez au 3è coup, vous gagnez la moitiè votre mise !
\t- au niveau 1 vous gagnez 20% de votre mise !
\t- au niveau 2 vous gagnez 33% de votre mise !
\t- au niveau 3 vous gagnez 50% de votre mise !\n
\t* Si vous ne le devinez pas au 3è coup, vous perdez votre mise et vous avez le droit :
\t - de retenter votre chance avec l'argent qu'il vous reste pour reconquérir le level perdu.
\t - de quitter le jeu. \n\n
Dès que vous devinez mon nombre : vous avez le droit de quitter le jeu et de partir avec vos gains
OU de continuer le jeu en passant au level supérieur.\n
"""

    return str

# Retourne le solde entree par l'utilisateur
def credit_solde():
    error = "Le montant saisie n'est pas valide, solde minimum de 1€ requis : "
    argent_solde = True
    while argent_solde:
        solde = input("Veuillez entrez votre solde de départ : \n-> ")
        try:
            solde = float(solde)
            if solde < 1:
                print(error)
            else:
                argent_solde = False
        except ValueError:
            print(error)
    return solde


# Retourne la mise entree par l'utilisateur
def controle_mise(solde):
    mise_min = 0.01
    argent_mise = True
    while argent_mise:
        mise = input("Le jeu commence, entrez votre mise : ")
        try:
            mise = float(mise)
            if (mise < mise_min):
                print(
                    "Le montant saisi n'est pas valide. Entrer SVP un montant entre 1 et %.2f € :" % (solde))
            elif mise > solde:
                print("Erreur, votre mise est plus elevé que votre solde.\n")
                print("Entrez une mise inférieur ou égale à %.2f € :" % (solde))
            else:
                argent_mise = False
        except ValueError:
            print("Le montant saisi n'est pas valide. Entrer SVP un montant entre 1 et %.2f € : " % (solde))

    return mise

# Retourne si le chiffre aleatoire a ete trouve
def nombreGagnant(nb_ordi, nb_coup, nb_coup_user, level):

    # Tant que le nb_user n'est pas egale au nb_ordi
    while True:
        # On verifie si l'user a bien tape un nombre
        try:
            nb_user = int(input("Alors mon nombre est : \n-> "))
        except ValueError:
            print("Je n'ai pas compris ce que vous avez deviné")
            continue

        if nb_user < nb_ordi:
            print("Votre nombre est trop petit !")
            perdu = False
        elif nb_user > nb_ordi:
            print("Votre nombre est trop grand ! ")
            perdu = False

        if nb_user == nb_ordi:
            gain = gainUser(nb_coup_user, mise, level)
            print("Bingo %s, vous avez gagné en %d coups et vous avez emporté %.2f € !\n" % (name_user, nb_coup_user, gain))
            nb_coup_gagne = nb_coup_user

            # On enregistre les donnees dans un dictionnaire
            stat_user = {}
            if level == 1:
                stat_user = {
                    'nb_coup' : nb_coup_user,
                    'mise' : mise,
                    'gain' : gain,
                    'gagne' : 1
                }
            elif level == 2:
                stat_user = {
                    'nb_coup' : nb_coup_user,
                    'mise' : mise,
                    'gain' : gain,
                    'gagne' : 1
                }
            elif level == 3:
                stat_user = {
                    'nb_coup' : nb_coup_user,
                    'mise' : mise,
                    'gain' : gain,
                    'gagne' : 1
                }
            level += 1
            nb_coup_user = 1
            perdu = False
            break

        # S'il reste un essai
        if nb_coup - nb_coup_user == 1:
            print('Il vous reste une chance !')
        nb_coup_user += 1

        # Si le nombre du coup du joueur est egale au coup max
        if nb_coup_user > nb_coup:
            print("Vous avez perdu ! Mon nombre est %s !" % (nb_ordi))
            nb_coup_user = 1
            gain = 0
            perdu = True
            stat_user = {}
            if level == 1:
                stat_user = {
                    'mise' : mise,
                    'gain' : gain,
                    'gagne' : 0
                }
            elif level == 2:
                stat_user = {
                    'mise' : mise,
                    'gain' : gain,
                    'gagne' : 0
            }
            elif level == 3:
                stat_user = {
                    'mise' : mise,
                    'gain' : gain,
                    'gagne' : 0
            }
            break

    list = {"gain": gain, "level": level, "perdu": perdu, "stat" : stat_user}
    return list

# Ajout de donnees d'user dans un fichier .json
def statistic(donnees):
    if path.exists("data.json"):
        try:
            with open('data.json', 'r+') as json_file:
                try:
                    data = json.load(json_file)
                    data.append(donnees)
                    json_file.seek(0)
                    json.dump(data, json_file)
                except JSONDecodeError as e:
                    print("Erreur : ", e)
        except IOError as i:
            print("Erreur : ", i)
    else: 
        with open('data.json', 'w') as outfile:
            json.dump(donnees, outfile)



# Debut du jeu 
print("""\
 /=======================WELCOME TO FABULOUS=========================\   
|                                                                    |
|   $$$$$$$\ $$\     $$\ $$$$$$$$\ $$\   $$\  $$$$$$\  $$\   $$\     | 
|   $$  __$$\\$$\   $$  |\__ $$  __|$$ |  $$ |$$  __$$\ $$$\  $$ |    |
|   $$ |  $$ |\$$\ $$  /    $$ |   $$ |  $$ |$$ /  $$ |$$$$\ $$ |    |
|   $$$$$$$  | \$$$$  /     $$ |   $$$$$$$$ |$$ |  $$ |$$ $$\$$ |    |
|   $$  ____/   \$$  /      $$ |   $$  __$$ |$$ |  $$ |$$ \$$$$ |    |
|   $$ |         $$ |       $$ |   $$ |  $$ |$$ |  $$ |$$ |\$$$ |    |
|   $$ |         $$ |       $$ |   $$ |  $$ | $$$$$$  |$$ | \$$ |    |
|   \__|         \__|       \__|   \__|  \__| \______/ \__|  \__|    |
|                                                                    |                   
|                                                                    | 
|    $$$$$$\   $$$$$$\   $$$$$$\  $$$$$$\ $$\   $$\  $$$$$$\         |   
|   $$  __$$\ $$  __$$\ $$  __$$\ \_$$  _|$$$\  $$ |$$  __$$\        |   
|   $$ /  \__|$$ /  $$ |$$ /  \__|  $$ |  $$$$\ $$ |$$ /  $$ |       |  
|   $$ |      $$$$$$$$ |\$$$$$$\    $$ |  $$ $$\$$ |$$ |  $$ |       | 
|   $$ |      $$  __$$ | \____$$\   $$ |  $$ \$$$$ |$$ |  $$ |       | 
|   $$ |  $$\ $$ |  $$ |$$\   $$ |  $$ |  $$ |\$$$ |$$ |  $$ |       |
|   \$$$$$$  |$$ |  $$ |\$$$$$$  |$$$$$$\ $$ | \$$ | $$$$$$  |       |
|   \______/ \__|  \__| \______/ \______|\__|  \__| \______/         |
|                                                                    |
\====================================================================/
""")

# On enregistre la date d'execution du jeu
now = datetime.now()
date_time = now.strftime("%m/%d/%Y, %H:%M:%S")

# On regarde si le fichier data.json existe, ce qui veut dire que l'user a deja joue
if path.exists("data.json"):
    donnees = {}
    mise_max = 0
    gain_max = 0
    try:
        # Ouverture du fichier data.json
        with open('data.json', 'r+') as json_file:            
            
            try:
                data = json.load(json_file)
                # Recuperation de donnees
                for d in data: 
                    if "name" in d:
                        name_user = d['name']
                    if "jeu" in d: 
                        nb_fois_jeu = d['jeu']
                    if "partie" in d:
                        for partie in d['partie']:
                            if "level_1" in partie:
                                if partie['level_1']['mise'] > mise_max:
                                    mise_max = partie['level_1']['mise']
                                if partie['level_1']['gain'] > gain_max:
                                    gain_max = partie['level_1']['gain']

            except JSONDecodeError as e:
                print("Erreur : ", e)
    except IOError as i:
        print("Erreur : ", i)
    
    print("Rebonjour %s, Content de vous revoir au Casino, prêt pour un nouveau challenge !" %(name_user))
    print("Voici les statistiques, depuis la 1è fois ", data[0]['date'], " : ")
    print("\t - Vous avez deja joué à ce jeu : %d fois" %(nb_fois_jeu))
    print("\t - Votre mise max est de  : %d euros" %(mise_max))
    print("\t - Votre gain max est de  : %d euros" %(gain_max))

    # Recuperation des donnees du fichier csv
    df = pd.read_csv('test.csv')
    df.head()
    df.info
    df["solde"].value_counts(normalize=True).plot(kind='pie')

else:
    # Creation du fichier .csv
    if not path.exists('test.csv'):
        with open('test.csv', 'w+') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=["jeu", "solde"])
            writer.writeheader()

    name_user = input('Je suis Python. Quel est votre pseudo ? \n-> ')
    print(regle())
    donnees = []
    
level = 1
nb_coup_user = 1
gain = 0
jeu = True
perdu = False

# Demande du solde du joueur
solde = credit_solde()
solde_debut = solde
print("Vous avez %.2f euros. Très bien ! Installez vous SVP à la table de paris." % (solde))

while jeu:
    nb_coup = coupParLevel(level)
    nb_ordi = randint(1, 10)

    # On regarde combien mise le joueur
    mise = controle_mise(solde)

    solde -= mise
    
    # Fonction qui regarde si le nb a ete trouve
    data = nombreGagnant(nb_ordi, nb_coup, nb_coup_user, level)
    gain = data['gain']
    level = data['level']
    perdu = data['perdu']
    solde += gain

    resultat_partie = data['stat']

    if level - 1 == 1 or level - 1 == 0:
        resultat_level_1 = resultat_partie
        partie = [{'level_1' : resultat_level_1}]

    if level - 1 == 2 : 
        resultat_level_2 = resultat_partie
        partie = [{'level_1' : resultat_level_1}, {'level_2' : resultat_level_2}]

    if level - 1 == 3 : 
        resultat_level_3 = resultat_partie
        partie = [{'level_1' : resultat_level_1}, {'level_2' : resultat_level_2}, {'level_3' : resultat_level_3}]

    if level <= 3:
        if solde <= 0:
            print("Vous êtes fauchés, il est temps de partir ...!")
            exit()
                            
        # Si l'on souhaite quitter la partie ou pas
        continuer_jeu = ''
        try:
            continuer_jeu = input_with_timeout('Souhaitez-vous continuer la partie (O/N) ? \n-> ', 10)
        except TimeoutExpired:
            print("Vous n'avez rien répondu. Vous finissez la partie avec %.2f €" % (solde))
            exit()
        else:
            while True:
                if continuer_jeu == 'O' or continuer_jeu == 'o':
                    if perdu:
                        print('Vous continuez ! Vous restez au level %d' % (level))
                        break
                    elif not perdu:
                        print('Super ! Vous passez au level %d' % (level))
                        break
                elif continuer_jeu == 'N' or continuer_jeu == 'n':
                    print("Au revoir ! Vous finissez la partie avec %.2f €" % (solde))
                    if path.exists("data.json"):
                        donnees = {
                            'name' : name_user,
                            'date' : date_time,
                            'jeu' : nb_fois_jeu + 1 ,
                            'solde' : solde_debut,
                            'partie' : partie
                        }
                        # Ecriture sur fichier test.csv 
                        with open('test.csv', 'a+') as csv_file:
                            cv_writer = csv.writer(csv_file)
                            cv_writer.writerow([donnees['jeu'],donnees['solde']])
                    else:
                        donnees.append({
                            'name' : name_user,
                            'date' : date_time,
                            'jeu' : 1,
                            'solde' : solde_debut,
                            'partie' : partie
                        })
                        for d in donnees:
                            # Ecriture sur fichier test.csv 
                            with open('test.csv', 'a+') as csv_file:
                                cv_writer = csv.writer(csv_file)
                                cv_writer.writerow([d['jeu'], d['solde']])
                        
                    statistic(donnees)                    
                    jeu = False
                    break
                else:
                    continuer_jeu = input_with_timeout("Je ne comprends pas votre réponse. Souhaitez-vous continuer la partie (O/N) ? \n-> ", 10)
                    continue
    elif level > 3:
        print("Bravo, vous avez gagné !")
        if path.exists("data.json"):
            donnees = {
                'name' : name_user,
                'date' : date_time,
                'jeu' : nb_fois_jeu + 1 ,
                'solde' : solde_debut,
                'partie' : partie
            }  
            # Ecriture sur fichier test.csv 
            with open('test.csv', 'a+') as csv_file:
                cv_writer = csv.writer(csv_file)
                cv_writer.writerow([donnees['jeu'],donnees['solde']])
        else:
            donnees.append({
                'name' : name_user,
                'date' : date_time,
                'jeu' : 1,
                'solde' : solde_debut,
                'partie' : partie
            })       
            for d in donnees:
                # Ecriture sur fichier test.csv 
                with open('test.csv', 'a+') as csv_file:
                    cv_writer = csv.writer(csv_file)
                    cv_writer.writerow([d['jeu'], d['solde']])

        statistic(donnees) 
        jeu = False