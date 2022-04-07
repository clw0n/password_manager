import os, string, random,  sqlite3
from django.db import OperationalError
from fastapi import File

def root():
    if not os.geteuid() == 0:
        print("Vous devez être root !")
    else:
        user = os.getlogin()
        print(f"Bienvenue, {user} !")
        database_exists()

def register():
    global username
    username = eval(input("Veuillez entrer votre nom : "))
    print(type(username))
    print(type(password))
    password = eval(input("Veuillez entrer votre mot de passe : "))
    File = open("accountext.txt", "a")
    File.write(f"{username}")
    File.write(" ")
    File.write(f"{password}")
    File.write("\n")
    File.close()
    print("Compte crée.")
    login()
    
def login():
    print("Veuillez vous enregistrer !")
    username = eval(input("Veuillez entrer votre nom : "))
    password = input("Veuillez entrer votre mot de passe : ")
    for line in open("accountext.txt").readlines():
        login_info = line.split()
        print(login_info)
        if username == login_info[0] and password == login_info[1]:
            print("Bienvenue !")
            database_exists()
        else:
            print("Mot de passe ou nom d'utilisateur incorrect.")

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
        login()

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
            print(f"""[+] Match found for {search} : '{result}'""")
        else:
            print("[-] No Match Found !")
    conn.commit()
    conn.close()
    
def print_database():
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM passwords""")
    database = cursor.fetchall() 
    id = "id"
    user = "user"
    email = "email"
    password = "password"
    date = "date"
    a = ("""| {id} | {user} | {email} | {password} | {date} |""")
    b = ("="* len(a))
    print(b)
    print(a)
    print(b)
    #boucler deux indices (i, j) sur la variable database: pour faire en sorte de centrer les indices de a, il faut soustraire la taille de l'élément
    #associé pour vérifier si son nombre est pair ou pas : si la soustraction est paire, alors on ajoute simplement un nombre d'espace de chaque côté
    #de l'indicateur pour le centrer, si la soustraction est impaire, il nous suffit simplement de rajouter 1 au résultat de la soustraction
    #et effectuer le même procédé précédent. Si la soustraction est négative, alors il nous suffit de faire le même procédé mais en inverse.
    conn.commit()
    conn.close()
    
def update_password():
    pass

def delete_line():
    pass

if __name__ == "__main__":
    root()
