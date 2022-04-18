import os, string, random,  sqlite3
from django.db import OperationalError
from tabulate import tabulate


if not os.geteuid() == 0:
	print("Vous devez être root !")
else:
	user = os.getlogin()
        print(f"Bienvenue, {user} !")
        database_exists()

def database_exists():
    try:
        conn = sqlite3.connect("passwords.db")
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE passwords(
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            user TEXT,
            email TEXT,
            website TEXT,
            password TEXT)""")
        conn.commit()
        conn.close()
        print("Base de données créée.\n")
        os.system("sleep 1")
        print("Vous devez vous créer un utilisateur !")
        register()
        print("Veuillez configurer le nom d'utilisateur et l'email pour les mots de passe. ")
        create_change_user()
    except sqlite3.OperationalError:
        database_methods()

def create_change_user():
    global user
    global email
    user = input("Entrez votre nom d'utilisateur : ")
    email = input("Entrez votre e-mail : ")
    database_methods()

def database_methods():
    choix = eval(input("""Choisissez parmi les options suivantes :
    1) Générer et stocker un mot de passe sécurisé dans la base de données
    2) Chercher un mot de passe dans la base de données
    3) Mettre à jour un mot de passe
    4) Supprimer un mot de passe (supprimer une ligne de la base de données)
    5) Ajouter / Changer d'utilisateur dans la table USERS 
    6) Afficher la base de données
    7) Quitter
    >>> ... """))

    if choix == 1:
        generate_password()
    elif choix ==2:
        search_password()
    elif choix ==3:
        update_password()
    elif choix ==4:
        delete_line()
    elif choix ==5:
        create_change_user()
    elif choix == 6:
        print_database()
    elif choix == 7:
        print("À Bientôt !")
    else:
        print("Veuillez entrer un numéro valide !")

def generate_password():
    random_source = string.ascii_letters + string.digits + string.punctuation
    taille = int(input("Veuillez entre la taille du mot de passe. Celle-ci doit être comprise entre 12 et 20."))
    if 12<= taille <=20:
        password = ''.join(random.choice(random_source) for i in range(taille))
        print(f"Le mot de passe généré est : {password}")
        website = input("Veuillez entrer le nom de domaine du site web pour lequel vous voulez enregistrer ce mot de passe : ")
        conn = sqlite3.connect("passwords.db")
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO passwords(user, email, website, password) VALUES(?, ?, ?, ?)""", (user, email, website, password))
        conn.commit()
        conn.close()
        print("Mot de passe enregistré !")
        os.system("sleep 1")
        database_methods()
    else:
        print("Veuillez entrer une taille de mot de passe valide !")

def search_password():
    search = input(">>> ...")
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute(f"""SELECT password FROM passwords WHERE user = '{search}' or email = '{search}' or website = '{search}' """)
    cursor.fetchrow()
    result = cursor.fetchall()
    for rows in result:
        if search == ('{5}'.format(rows[5])):
            print(f"""[+] Résultat trouvé pour {search} : '{result}'""")
        else:
            print("[-] Aucun résultat trouvé !")
    conn.commit()
    conn.close()
    return password

def print_database():
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM passwords""")
    database = cursor.fetchall() 
    headers = ["id", "user", "email", "website", "password"]
    print(tabulate(database, headers, tablefmt="fancy_grid"))
    conn.commit()
    conn.close()


def update_password():
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    if search_password():
        cursor.execute(f"""UPDATE password FROM passwords where * = '{search}' """)
        conn.commit()
        conn.close()
    else:
        print("Aucun mot de passe trouvé !")
        conn.commit()
        conn.close()

if __name__ == "__main__":
    root()
