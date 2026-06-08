import csv
import os

CSV_PATH=os.path.join(os.path.dirname(__file__), '..', 'data', 'usuarios.csv')

def ler_usuarios():
    usuarios=[]
    with open(CSV_PATH, newline='', encoding='urf-8') as f:
        leitor = csv.DictReader(f)
        for linha in leitor:
            usuarios.append(linha)
    return usuarios

def salvar_usuario(username, email, password_hash):
    with open(CSV_PATH, 'a', newline='', encoding='utf-8') as f:
        escritor= csv.DictWriter(f, fieldnames=['username', 'email', 'password_hash'])
        escritor.writerow({'username':username,'email':email,'password_hash':password_hash})

def buscar_email(email):
    for usuario in ler_usuarios:
        if usuario['email']==email:
            return usuario
    return None