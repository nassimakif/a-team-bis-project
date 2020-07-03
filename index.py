# index.py

from random import randint
from math import ceil
from datetime import datetime
import time
from threading import Thread
import sys
import select

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
def gainUser(coup, mise):
    if coup == 1:
        gain = mise * 2
    if coup == 2:
        gain = mise
    if coup >= 3:
        gain = mise / 2

    return gain

# Retour les regles du jeu
def regle():
    str = """Je vous explique le principe du jeu :  \n
Je viens de penser à un nombre entre 1 et 10. Devinez lequel ?\n 
Attention : vous avez le droit à trois essais ! \n 
- Si vous devinez mon nombre dès le premier coup, vous gagnez le double de votre mise !
- Si vous le devinez au 2è coup, vous gagnez exactement votre mise !
- Si vous le devinez au 3è coup, vous gagnez la moitiè votre mise !
- Si vous ne le devinez pas au 3è coup, vous perdez votre mise et vous avez le droit :
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
        print('Veuillez entrez votre solde de départ : ')
        solde = input()
        try:
            solde = int(solde)
            if(solde < 1):
                print(error)
            else:
                argent_solde = False
        except ValueError:
            print(error)
    return solde


# Retourne la mise entree par l'utilisateur
def controle_mise(solde):
    argent_mise = True
    while argent_mise:
        mise = input("Le jeu commence, entrez votre mise : ")
        try:
            mise = int(mise)

            if (mise < 1):
                print(
                    "Le montant saisi n'est pas valide. Entrer SVP un montant entre 1 et 10 € : ")
            elif mise > solde:
                print("Erreur, votre mise est plus elevé que votre solde.\n")
                print("Entrez une mise inférieur à %d € :" % (solde))
            else:
                argent_mise = False
        except ValueError:
            print(
                "Le montant saisi n'est pas valide. Entrer SVP un montant entre 1 et 10 € : ")

    return mise

# Retourne si le chiffre aleatoire a ete trouve
def nombreGagnant(nb_ordi, nb_coup, nb_coup_user, level):

    nb_user = int(input("Alors mon nombre est : "))

    # Tant que le nb_user n'est pas egale au nb_ordi
    while nb_ordi != nb_user:
        nb_coup_user += 1

        if nb_user < nb_ordi:
            print("Votre nombre est trop petit !")
            perdu = False
        elif nb_user > nb_ordi:
            print("Votre nombre est trop grand ! ")
            perdu = False

        # Si le nombre du coup du joueur est egale au coup max
        if nb_coup_user > nb_coup:
            print("Vous avez perdu ! Mon nombre est %s !" % (nb_ordi))
            nb_coup_user = 1
            gain = 0
            perdu = True
            break

        nb_user = int(input("Alors mon nombre est : "))

    if nb_user == nb_ordi:
        gain = gainUser(nb_coup_user, mise)
        print("Bingo %s, vous avez gagné en %d coups et vous avez emporté %d € !\n" % (
            name_user, nb_coup_user, gain))
        level += 1
        nb_coup_user = 1
        perdu = False

    list = {"gain": gain, "level": level, "perdu": perdu}
    return list


level = 1
nb_coup_user = 1
gain = 0
name_user = input('Je suis Python. Quel est votre pseudo ? ')
jeu = True
perdu = False

solde = credit_solde()

print("Hello ", name_user, ", vous avez", solde, "euros. Très bien ! Installez vous SVP à la table de paris.")
print(regle())

while jeu:
    nb_coup = coupParLevel(level)
    nb_ordi = randint(1, rangeParLevel(level))
    print("nb_ordi", nb_ordi)

    # On regarde combien mise le joueur
    mise = controle_mise(solde)

    solde -= mise

    data = nombreGagnant(nb_ordi, nb_coup, nb_coup_user, level)
    gain = data['gain']
    level = data['level']
    perdu = data['perdu']

    solde += gain

    # Si l'on souhaite quitter la partie ou pas
    continuer_jeu = ''
    # continuer_jeu = input('Souhaitez-vous continuer la partie (O/N) ?')
    try:
        continuer_jeu = input('Souhaitez-vous continuer la partie (O/N) ? ')
    except TimeoutExpired:
        print("Vous n'avez rien répondu. Vous finissez la partie avec %d €" % (solde))
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
                print("Au revoir ! Vous finissez la partie avec %d €" % (solde))
                jeu = False
                break
            else:
                continuer_jeu = input(
                    "Je ne comprends pas votre réponse. Souhaitez-vous continuer la partie (O/N) ?")
                continue