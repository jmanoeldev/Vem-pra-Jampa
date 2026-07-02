import csv
from datetime import datetime
import os

CSV_PATH=os.path.join(os.path.dirname(__file__), '..', 'data', 'usuarios.csv')

def ler_usuarios():
    usuarios = []
    try:
        # Abre e lê o arquivo como um texto comum
        arq = open(CSV_PATH, 'r', encoding='utf-8')
        linhas = arq.read().splitlines()
        arq.close()

        # Verifica se o arquivo tem mais que apenas o cabeçalho
        if len(linhas) > 1:
            for i in range(1, len(linhas)):
                # Separa os dados pela vírgula
                valores = linhas[i].split(',')
                
                # Monta um dicionário manual para manter a compatibilidade com o resto do seu projeto
                usuario = {
                    'username': valores[0],
                    'email': valores[1],
                    'password_hash': valores[2]
                }
                usuarios.append(usuario)
    except FileNotFoundError:
        pass
        
    return usuarios

def salvar_usuario(username, email, password_hash):
    # Primeiro, verificamos se precisamos colocar o cabeçalho (caso o arquivo não exista)
    precisa_cabecalho = not os.path.exists(CSV_PATH)
    
    # Abre o arquivo no modo 'a' (append/adicionar)
    arq = open(CSV_PATH, 'a', encoding='utf-8')
    
    if precisa_cabecalho:
        arq.write("username,email,password_hash\n")
        
    # Cria a string (linha) formatada manualmente com as vírgulas e a quebra de linha no final
    nova_linha = f"{username},{email},{password_hash}\n"
    
    # Escreve no arquivo e fecha
    arq.write(nova_linha)
    arq.close()
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
                row['periodo'] = row['periodo'].split('|') if row['periodo'] else []
                row['publico'] = row['publico'].split('|') if row['publico'] else []
                row['custo'] = row['custo'].split('|') if row['custo'] else []
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

def buscar_usuario_por_username(username):
    for usuario in ler_usuarios():
        if usuario['username'] == username:
            return usuario
    return None

def atualizar_usuario(username_atual, novo_username, novo_email, novo_password_hash):

    usuarios = ler_usuarios()

    for usuario in usuarios:

        if usuario['username'] == username_atual:

            usuario['username'] = novo_username
            usuario['email'] = novo_email
            usuario['password_hash'] = novo_password_hash

            break

    with open(CSV_PATH, 'w', newline='', encoding='utf-8') as f:

        writer = csv.DictWriter(f, fieldnames=['username', 'email', 'password_hash'])
        writer.writeheader()
        writer.writerows(usuarios)

def atualizar_autor_comentarios(nome_antigo, nome_novo):

    comentarios = ler_comentarios()

    for comentario in comentarios:

        if comentario['autor'] == nome_antigo:
            comentario['autor'] = nome_novo

    with open('data/comentarios.csv', 'w', newline='', encoding='utf-8') as f:

        writer = csv.DictWriter(f, fieldnames=['id', 'ponto_id', 'autor', 'data', 'texto'])

        writer.writeheader()
        writer.writerows(comentarios)

def excluir_usuario(username):

    usuarios = ler_usuarios()

    usuarios_filtrados = []

    for usuario in usuarios:

        if usuario['username'] != username:
            usuarios_filtrados.append(usuario)

    with open(CSV_PATH,'w', newline='', encoding='utf-8') as f:

        writer = csv.DictWriter(f, fieldnames=['username', 'email', 'password_hash'])

        writer.writeheader()
        writer.writerows(usuarios_filtrados)

def excluir_comentarios_usuario(username):

    comentarios = ler_comentarios()

    comentarios_filtrados = []

    for comentario in comentarios:

        if comentario['autor'] != username:
            comentarios_filtrados.append(comentario)

    with open('data/comentarios.csv', 'w', newline='', encoding='utf-8') as f:

        writer = csv.DictWriter(f, fieldnames=['id','ponto_id','autor','data','texto'])

        writer.writeheader()
        writer.writerows(comentarios_filtrados)

def editar_comentario(comentario_id, novo_texto):
    comentarios = ler_comentarios()

    for comentario in comentarios:
        if int(comentario['id']) == comentario_id:
            comentario['texto'] = novo_texto
            break

    with open('data/comentarios.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['id', 'ponto_id', 'autor', 'data', 'texto'])
        writer.writeheader()
        writer.writerows(comentarios)

def excluir_comentario(comentario_id):
    comentarios = ler_comentarios()

    comentarios_filtrados = []
    for comentario in comentarios:
        if int(comentario['id']) != comentario_id:
            comentarios_filtrados.append(comentario)

    with open('data/comentarios.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['id', 'ponto_id', 'autor', 'data', 'texto'])
        writer.writeheader()
        writer.writerows(comentarios_filtrados)