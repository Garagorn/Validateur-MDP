import tkinter as tk
from tkinter import ttk

from score import score_structure, niveau, analyser_date_naissance, penalites_securite, est_valide
from verif_dico import verification_dictionnaire, score_zxcvbn
from feedback import feedback
from database import ajouterMDP, verifierMDP


def apply_dark_theme(root):
    style = ttk.Style()
    style.theme_use("clam")

    bg = "#1e1e1e"
    fg = "#ffffff"
    entry_bg = "#2a2a2a"
    focus_bg = "#3a3a3a"
    accent = "#4a90e2"

    style.configure(".", background=bg, foreground=fg)

    style.configure("TLabel",
        background=bg,
        foreground=fg,
        font=("Segoe UI", 10)
    )

    style.configure("TEntry",
        fieldbackground=entry_bg,
        foreground=fg,
        insertcolor=fg,
        padding=5
    )

    style.map("TEntry",
        fieldbackground=[("focus", focus_bg)]
    )

    style.configure("TButton",
        background=accent,
        foreground="white",
        padding=6
    )

    root.configure(bg=bg)


#Lancement de la version graphique
def lancer():

    # Barres de progression
    root = tk.Tk()
    root.title("Analyseur de mot de passe")
    root.geometry("900x750")

    apply_dark_theme(root)

    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True)


    #Création de mot de passe - - -
    frame = ttk.Frame(notebook, padding=20)
    notebook.add(frame, text="Création")

    # Champs
    entry_username = ttk.Entry(frame)
    entry_nom = ttk.Entry(frame)
    entry_prenom = ttk.Entry(frame)
    entry_naissance = ttk.Entry(frame)
    entry_mdp = ttk.Entry(frame, show="*")

    labels = ["Username", "Nom", "Prénom", "Date de naissance", "Mot de passe"]
    entries = [entry_username, entry_nom, entry_prenom, entry_naissance, entry_mdp]

    for i, (label, entry) in enumerate(zip(labels, entries)):
        ttk.Label(frame, text=label).grid(row=i, column=0, sticky="w")
        entry.grid(row=i, column=1, sticky="ew", pady=5)

    frame.columnconfigure(1, weight=1)

    # Barres de progression 

    def update_bar(canvas, value, max_value):
        canvas.delete("bar")
        width = canvas.winfo_width() or 250
        ratio = min(value / max_value, 1.0)
        fill = int(width * ratio)

        if value == 0:
            color = "#d9534f"
        elif value < max_value:
            color = "#f0ad4e"
        else:
            color = "#5cb85c"

        canvas.create_rectangle(0, 0, fill, 20, fill=color, outline="", tags="bar")

    def add_bar(row, text):
        ttk.Label(frame, text=text).grid(row=row, column=0, sticky="w")
        bar = tk.Canvas(frame,height=22,bg="#2a2a2a",highlightthickness=0)
        bar.grid(row=row, column=1, sticky="ew", pady=4)
        return bar

    bar_maj = add_bar(5, "Majuscules")
    bar_min = add_bar(6, "Minuscules")
    bar_chiffres = add_bar(7, "Chiffres")
    bar_spec = add_bar(8, "Spéciaux")


    # Analyse du mot de passe
    def analyser(event=None):
        password = entry_mdp.get()
        nom = entry_nom.get()
        prenom = entry_prenom.get()
        naissance = entry_naissance.get()

        if not password:
            return

        infos = [nom, prenom, naissance]
        score_struct, stats = score_structure(password)

        try:
            zx = verification_dictionnaire(password, infos)
            zx_score = score_zxcvbn(zx)
        except:
            zx_score = 0
            zx = {"feedback": {"suggestions": []}}

        date_fragments = analyser_date_naissance(password, naissance)

        penalty, issues = penalites_securite(
            password, nom, prenom, date_fragments, zx_score
        )

        score_total = max(0, score_struct + penalty)

        if issues:
            score_total = min(score_total, 40)

        progress["value"] = score_total

        # Couleur dynamique
        if score_total < 40:
            color = "red"
        elif score_total < 75:
            color = "orange"
        else:
            color = "green"

        label_score.config(
            text=f"Score : {score_total} / 100 ({niveau(score_total)})",
            foreground=color
        )

        # Activation bouton ajouter
        if est_valide(score_total):
            btn_ajouter.config(state="normal")
        else:
            btn_ajouter.config(state="disabled")

        # Barres
        update_bar(bar_maj, stats["Majuscules"], 2)
        update_bar(bar_min, stats["Minuscules"], 2)
        update_bar(bar_chiffres, stats["Chiffres"], 2)
        update_bar(bar_spec, stats["Spéciaux"], 1)

        # Feedback
        messages = feedback(password, stats, zx, date_fragments, nom, prenom, issues)

        text_feedback.delete("1.0", tk.END)
        for msg in messages:
            text_feedback.insert(tk.END, f"• {msg}\n")

    entry_mdp.bind("<KeyRelease>", analyser)

    def ajouter():
        username = entry_username.get()
        password = entry_mdp.get()

        success, message = ajouterMDP(username, password)

        if success:
            label_info.config(text=message, foreground="green")
        else:
            label_info.config(text=message, foreground="red")


    #UI

    btn_ajouter = ttk.Button(frame, text="Ajouter", command=ajouter, state="disabled")
    btn_ajouter.grid(row=9, column=1, pady=10)

    label_score = ttk.Label(frame, text="Score :")
    label_score.grid(row=10, column=0, columnspan=2)

    progress = ttk.Progressbar(frame, maximum=100)
    progress.grid(row=11, column=0, columnspan=2, sticky="ew")

    label_info = ttk.Label(frame, text="")
    label_info.grid(row=12, column=0, columnspan=2)

    text_feedback = tk.Text(frame,height=12,bg="#2a2a2a",fg="#ffffff",insertbackground="white",relief="flat")

    frame.rowconfigure(13, weight=1)

    frame_login = ttk.Frame(notebook, padding=20)
    notebook.add(frame_login, text="Connexion")

    container = ttk.Frame(frame_login)
    container.place(relx=0.5, rely=0.5, anchor="center")

    ttk.Label(container, text="Connexion", font=("Segoe UI", 14, "bold")).pack(pady=10)

    ttk.Label(container, text="Username").pack()
    login_user = ttk.Entry(container, width=30)
    login_user.pack(pady=5)

    ttk.Label(container, text="Mot de passe").pack()
    login_pass = ttk.Entry(container, show="*", width=30)
    login_pass.pack(pady=5)

    label_login = ttk.Label(container, text="")
    label_login.pack(pady=10)

    def verifier():
        success, message = verifierMDP(
            login_user.get(),
            login_pass.get()
        )

        if success:
            label_login.config(text=message, foreground="#5cb85c")
        else:
            label_login.config(text=message, foreground="#d9534f")

    ttk.Button(container, text="Se connecter", command=verifier)\
        .pack(pady=10)

    root.mainloop()