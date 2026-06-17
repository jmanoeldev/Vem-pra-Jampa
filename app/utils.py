import csv
from datetime import datetime
import os

CSV_PATH=os.path.join(os.path.dirname(__file__), '..', 'data', 'usuarios.csv')

def ler_usuarios():
    usuarios=[]
    with open(CSV_PATH, newline='', encoding='utf-8') as f:
        leitor = csv.DictReader(f)
        for linha in leitor:
            usuarios.append(linha)
    return usuarios

def salvar_usuario(username, email, password_hash):
    with open(CSV_PATH, 'a', newline='', encoding='utf-8') as f:
        escritor= csv.DictWriter(f, fieldnames=['username', 'email', 'password_hash'])
        escritor.writerow({'username':username,'email':email,'password_hash':password_hash})

def buscar_email(email):
    for usuario in ler_usuarios():
        if usuario['email']==email:
            return usuario
    return None

# FUNÇÕES DE PERSISTÊNCIA E MANIPULAÇÃO DE DADOS (CSV)
def ler_pontos():
    #Lê a lista de pontos turísticos do arquivo CSV.
    pontos = []
    try:
        with open('data/pontos.csv', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                row['avaliacao'] = float(row['avaliacao'])
                # Converte as dicas textuais separadas por '|' em uma lista do Python
                row['dicas'] = row['dicas'].split('|') if row['dicas'] else []
                row['categoria'] = row['categoria'].split('|') 
                pontos.append(row)
    except FileNotFoundError:
        pass
    return pontos


def ler_comentarios():
    """Lê todos os comentários do arquivo CSV."""
    comentarios = []
    try:
        with open('data/comentarios.csv', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                comentarios.append(row)
    except FileNotFoundError:
        pass
    return comentarios


def escrever_comentario(ponto_id, autor, texto):
    """Escreve um novo comentário salvando com segurança a quebra de linha."""
    comentarios = ler_comentarios()
    novo_id = str(len(comentarios) + 1)
    data_hoje = datetime.now().strftime('%d/%m/%Y')

    # 'a+' permite anexar ao final do arquivo e ler para validar a última linha
    with open('data/comentarios.csv', 'a+', newline='', encoding='utf-8') as f:
        f.seek(0, 2) # Move o cursor para o final absoluto do arquivo
        
        if f.tell() > 0: # Se o arquivo não estiver totalmente vazio
            f.seek(f.tell() - 1, 0) # Recua 1 caractere
            ultimo_char = f.read(1) # Lê o último caractere existente
            
            # Se o arquivo não terminar com uma quebra de linha, insere uma para prevenir colagem
            if ultimo_char not in ('\n', '\r'):
                f.write('\n')
        
        # Grava a nova linha de forma limpa
        writer = csv.DictWriter(f, fieldnames=['id', 'ponto_id', 'autor', 'data', 'texto'])
        writer.writerow({
            'id': novo_id,
            'ponto_id': str(ponto_id),
            'autor': autor,
            'data': data_hoje,
            'texto': texto
        })

def editar_comentario(comentario_id, novo_texto):
    comentarios = ler_comentarios()

    for comentario in comentarios:
        if int(comentario['id']) == comentario_id:
            comentario['texto'] = novo_texto
            break
    
    with open('data/comentarios.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames= ['id', 'ponto_id', 'autor', 'data', 'texto'])
        writer.writeheader()
        writer.writerows(comentarios)
