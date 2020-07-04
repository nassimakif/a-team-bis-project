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
            gain = mise
        elif level == 2:
            gain = mise * 1.25
        elif level == 3:
            gain = mise * 1.5
    if coup >= 3:
        if level == 1:
            gain = mise / 4
        elif level == 2:
            gain = mise / 3
        elif level == 3:
            gain = mise * 1
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
        solde = input("Veuillez entrez votre solde de départ : ")
        try:
            solde = float(solde)
            if(solde < 1):
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
    nb_user = int(input("Alors mon nombre est : "))

    # Tant que le nb_user n'est pas egale au nb_ordi
    while nb_ordi != nb_user:
        
        if nb_user < nb_ordi:
            print("Votre nombre est trop petit !")
            perdu = False
        elif nb_user > nb_ordi:
            print("Votre nombre est trop grand ! ")
            perdu = False

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
            break

        nb_user = int(input("Alors mon nombre est : "))

    if nb_user == nb_ordi:
        gain = gainUser(nb_coup_user, mise, level)
        print("Bingo %s, vous avez gagné en %d coups et vous avez emporté %.2f € !\n" % (name_user, nb_coup_user, gain))
        nb_coup_gagne = nb_coup_user
        # On enregistre les donnees dans un dictionnaire
        stat_user = {}
        # stat_user['partie'] = []
        if level == 1:
            stat_user = ({
                'level_1' : level,
                'nb_coup' : nb_coup_user,
                'mise' : mise,
                'gain' : gain,
                'partie' : 1
            })
        elif level == 2:
            stat_user = {
                'level_2' : level,
                'nb_coup' : nb_coup_user,
                'mise' : mise,
                'gain' : gain,
                'partie' : 1
            }
        elif level == 3:
            stat_user={
                'level_3' : level,
                'nb_coup' : nb_coup_user,
                'mise' : mise,
                'gain' : gain,
                'partie' : 1
            }      

        level += 1
        nb_coup_user = 1
        perdu = False

    list = {"gain": gain, "level": level, "perdu": perdu, "data" : stat_user}
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
        with open('data.json', 'a+') as outfile:
            json.dump(donnees, outfile)


# Debut du jeu 

# On enregistre la date d'execution du jeu
now = datetime.now()
date_time = now.strftime("%m/%d/%Y, %H:%M:%S")

# On regarde si le fichier data.json existe, ce qui veut dire que l'user a deja joue
if path.exists("data.json"):
    donnees = {}
    try:
        with open('data.json', 'r+') as json_file:
            try:
                data = json.load(json_file)
                for d in data: 
                    if "name" in d:
                        name_user = d['name']
                    
                    if "jeu" in d: 
                        jeu = d['jeu']
                
                # Recuperation de donnees
                donnees = {"name": name_user, "date" : date_time, "jeu": jeu + 1}

                print("Rebonjour %s, Content de vous revoir au Casino, prêt pour un nouveau challenge !" %(name_user))
            except JSONDecodeError as e:
                print("Erreur : ", e)
    except IOError as i:
        print("Erreur : ", i)
else:
    name_user = input('Je suis Python. Quel est votre pseudo ? ')
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
    nb_ordi = randint(1, rangeParLevel(level))
    print("nb_ordi", nb_ordi)

    # On regarde combien mise le joueur
    mise = controle_mise(solde)

    solde -= mise

    # Fonction qui regarde si le nb a ete trouve
    data = nombreGagnant(nb_ordi, nb_coup, nb_coup_user, level)
    gain = data['gain']
    level = data['level']
    perdu = data['perdu']
    solde += gain

    resultat_partie = data['data']

    print(resultat_partie)
    if path.exists("data.json"):
        donnees = {
                'name' : name_user,
                'date' : date_time,
                'jeu' : 1,
                'solde' : solde_debut
            }
    else:
        donnees.append({
            'name' : name_user,
            'date' : date_time,
            'jeu' : 1,
            'solde' : solde_debut
        })




    if level <= 3:
        # Si l'on souhaite quitter la partie ou pas
        continuer_jeu = ''
        try:
            continuer_jeu = input('Souhaitez-vous continuer la partie (O/N) ? ')
        except TimeoutExpired:
            print("Vous n'avez rien répondu. Vous finissez la partie avec %.2f €" % (solde))
            sys.exit()
            exit()
        else:
            while(continuer_jeu != 'O' or continuer_jeu != 'N'):
                if continuer_jeu == 'O':
                    if (perdu):
                        print('Vous continuez, super ! Vous restez au level %d' % (level))
                        break
                    elif(not perdu):
                        print('Super ! Vous passez au level %d' % (level))
                        break
                elif continuer_jeu == 'N':
                    print("Au revoir ! Vous finissez la partie avec %.2f €" % (solde))
                    statistic(donnees)                    
                    jeu = False
                    break
                else:
                    continuer_jeu = input(
                        "Je ne comprends pas votre réponse. Souhaitez-vous continuer la partie (O/N) ?")
                    continue
    elif level > 3:
        print("Bravo, vous avez gagné !")
        statistic(donnees) 
        jeu = False
