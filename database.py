import sqlite3 as sql
from hashing import verifier,hasher
from score import est_valide

def ajouterMDP(username, mdp,score_total):
    if not username or not mdp:
        return False, "Champs vides"

    if not est_valide(score_total):
        return False, "Mot de passe trop faible"
    try:
        #Connection à la bdd
        conn = sql.connect("database.db")
        cursor = conn.cursor()

        # Hashage
        hashed_password = hasher(mdp)

        # Insertion dans la bdd
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hashed_password)
        )
        #Fermeture de la connection
        conn.commit()
        conn.close()

        return True, "Utilisateur ajouté"

    except sql.IntegrityError:
        return False, "Nom d'utilisateur déjà existant"

    except Exception as e:
        return False, f"Erreur : {e}"

def verifierMDP(username, mdp):
    if not username or not mdp:
        return False, "Champs vides"

    #Connection à la bdd
    try:
        conn = sql.connect("database.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT password FROM users WHERE username = ?",
            (username,)
        )

        result = cursor.fetchone()
        conn.close()

        if result is None:
            return False, "Utilisateur introuvable"

        mdpBD = result[0] #mdp hashé depuis la base

        if verifier(mdp, mdpBD):
            return True, "Mot de passe correspondant"
        else:
            return False, "Mot de passe incorrect"

    except Exception as e:
        return False, f"Erreur : {e}"
