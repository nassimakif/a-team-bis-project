#casino.py
from random import randint
from math import ceil

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
        nb_ordi = 10
    elif level == 2:
        nb_ordi == 20
    elif level == 3:
        nb_ordi == 30

    return nb_ordi

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


# Retourne la mise entree par l'utilisateur
def mise(solde):
    argent_mise = True
    while argent_mise:
        mise = input("Le jeu commence, entrez votre mise : ")
        try:
            mise = int(mise)
            if (mise < 1 or mise > solde): 
                print("Le montant saisi n'est pas valide. Entrer SVP un montant entre 1 et 10 € : ")
            elif mise > solde:
                print("Erreur, votre mise est plus elevé que votre solde.\n")
                print("Entrez une mise inférieur à %d € :" %(solde))
            else:
                argent_mise = False
        except ValueError:
            print("Le montant saisi n'est pas valide. Entrer SVP un montant entre 1 et 10 € : ")

    return mise

# Retourne si le chiffre aleatoire a ete trouve
# def nombreGagnant(nb_ordi, nb_user, nb_coup_user):
    

level = 1
nb_coup = coupParLevel(level)
nb_ordi = randint(1, rangeParLevel(level))
nb_coup_user = 1
solde = 10
gain = 0
name_user = input('Je suis Python. Quel est votre pseudo ? ')
jeu = True

print("Hello ", name_user, ", vous avez", solde, "euros. Très bien ! Installez vous SVP à la table de paris.")
print(regle())

while jeu:

    # On regarde combien mise le joueur
    mise = mise(solde)
        
    solde -= mise

    nb_user = int(input("Alors mon nombre est : "))

    # Tant que le nb_user n'est pas egale au nb_ordi
    while nb_ordi != nb_user:
        print(nb_ordi)

        if nb_user == nb_ordi: 
            gain = gainUser(nb_coup_user, mise)
            print("Bingo René, vous avez gagné en %d coups et vous avez emporté %d € !\n" %(nb_coup_user, gain))
            level += 1
        elif nb_user < nb_ordi: 
            print("Votre nombre est trop petit !\n")
        elif nb_user > nb_ordi: 
            print("Votre nombre est trop grand ! \n")

        nb_coup_user += 1
        # Si le nombre du coup du joueur est egale au coup max
        if nb_coup_user > nb_coup:
            print("Vous avez perdu ! Mon nombre est %s !" %(nb_ordi))
            nb_coup_user = 0
            break
        
        nb_user = int(input("Alors mon nombre est : "))

        
    if nb_user == nb_ordi: 
        gain = gainUser(nb_coup_user, mise)
        print("Bingo René, vous avez gagné en %d coups et vous avez emporté %d € !\n" %(nb_coup_user, gain))
        level += 1

    gain_total = solde + gain
    continuer_jeu = ''
    continuer_jeu = input('Souhaitez-vous continuer la partie (O/N) ?')

    while(continuer_jeu != 'O' or continuer_jeu != 'N'):
        if continuer_jeu == 'O':
            print('Super ! Vous passez au level %d' %(level))
            break
        elif continuer_jeu == 'N':
            print("Au revoir ! Vous finissez la partie avec %d €" %(gain_total))
            break
            jeu = False

fodefohezo
    

    
        
    