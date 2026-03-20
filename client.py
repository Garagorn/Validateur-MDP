#Guesser en console
def recupInfos():
    infos=[]
    infos.append(input("Entrez votre nom : "))
    infos.append( input("Entrez votre prenom : "))
    infos.append(input("Entrez votre date de naissance (jj/mm/aaaa) : "))

    animal=input("Avez vous un animal ? ")
    if(animal.lower() == "oui"):
        infos.append(input("Quel est le nom de votre animal ? "))
    return infos


def recupMDP():
    return input("Mot de passe : ")

