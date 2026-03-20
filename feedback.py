def feedback(password, stats, zx, date_fragments, nom="", prenom="", issues=None):
    messages = []

    # Structure du feedback
    for k, v in stats.items():
        if v == 0:
            messages.append(f"Aucun {k.lower()} détecté")

    # Problèmes liés aux mdp
    if issues:
        if "nom" in issues:
            messages.append("/!\\ Votre NOM apparaît dans le mot de passe")
        if "prenom" in issues:
            messages.append("/!\\ Votre PRÉNOM apparaît dans le mot de passe")
        if "date_complete" in issues:
            messages.append("/!\\ Date de naissance complète détectée")
        if "date_partielle" in issues:
            messages.append("/!\\ Partie de la date de naissance présente")
        if "dictionnaire_critique" in issues:
            messages.append("/!\\ Mot de passe très courant (dictionnaire)")
        if "dictionnaire_faible" in issues:
            messages.append("/!\\ Mot de passe prévisible")

    # Suggestions zxcvbn
    for s in zx["feedback"]["suggestions"]:
        messages.append(s)

    if not messages:
        messages.append("Aucune problème pour le mot de passse")

    return messages