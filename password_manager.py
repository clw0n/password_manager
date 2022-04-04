import os, string, random, hashlib, sqlite3

user = os.getlogin()

def root():
    if not os.geteuid() == 0:
        print("Vous devez être root !")
    else:
        print(f"Bienvenue, {user} !")
        database_exists()

def database_exists():
    try:
        conn = sqlite3.connect("create_db.db")
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE users(
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            user TEXT,
            email TEXT)""")
        print("Base de données crée. Veuillez configurer un mot de passe maître pour pouvoir y accéder, et l'utilisateur principal de la table USERS.")
        conn.commit()
        database_methods()

    except sqlite3.OperationalError:
        print("Base de données détectée. Veuillez entrer votre mot de passe maître pour y accéder.")
        database_methods()

def create_main_user():
    pass

def database_methods():
    choix = eval(input("""Choisissez parmi les options suivantes :
    1) Générer un mot de passe sécurisé
    2) Chercher un mot de passe dans la base de données
    3) Mettre à jour un mot de passe
    4) Supprimer un mot de passe (supprimer une ligne de la base de données)
    5) Ajouter un nouvel utilisateur dans la table USERS """))

    if choix == 1:
        generate_password()
    elif choix ==2:
        search_password()
    elif choix ==3:
        update_password()
    elif choix ==4:
        delete_line()
    elif choix ==5:
        update_users()

def generate_password():
    random_source = string.ascii_letters + string.digits + string.punctuation
    taille = int(input("Veuillez entre la taille du mot de passe. Celle-ci doit être comprise entre 12 et 20."))
    if 12<= taille <=20:
        password = ''.join(random.choice(random_source) for i in range(taille))
        print(f"Le mot de passe généré est : {password}")
        
    else:
        print("Veuillez entrer une taille de mot de passe valide !")
        generate_password()

def search_password():
    pass

def update_password():
    pass

def delete_line():
    pass

def update_users():
    pass

def hash_password(password):
    pass

def decrypt_password(password):
    pass

def print_database(database):
    pass

def check_user():
    pass

if __name__ == "__main__":
    root()

