from datetime import datetime
import os

CSV_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'usuarios.csv')

# ==========================================================================
# ENGENHARIA DE ARQUIVOS (Mecanismos manuais para substituir a biblioteca CSV)
# ==========================================================================

def separar_linha_csv(linha):
    """Separa uma linha por vírgulas, mas ignora as vírgulas dentro de aspas duplas."""
    valores = []
    campo_atual = []
    em_aspas = False
    i = 0
    while i < len(linha):
        caractere = linha[i]
        if caractere == '"':
            # Se encontrar aspas duplicadas (""), trata como aspa literal interna do texto
            if em_aspas and i + 1 < len(linha) and linha[i+1] == '"':
                campo_atual.append('"')
                i += 1
            else:
                em_aspas = not em_aspas
        elif caractere == ',' and not em_aspas:
            valores.append("".join(campo_atual).strip())
            campo_atual = []
        else:
            campo_atual.append(caractere)
        i += 1
    valores.append("".join(campo_atual).strip())
    return valores

def formatar_linha_csv(valores):
    """Formata uma lista de strings em uma linha válida de CSV com quebra de linha."""
    linha_formatada = []
    for v in valores:
        v_str = str(v)
        # Se o texto contiver caracteres especiais de separação, protege envolvendo em aspas duplas
        if ',' in v_str or '"' in v_str or '\n' in v_str or '\r' in v_str:
            v_str = v_str.replace('"', '""')
            linha_formatada.append(f'"{v_str}"')
        else:
            linha_formatada.append(v_str)
    return ",".join(linha_formatada) + "\n"

def ler_csv_dinamico(caminho_arquivo):
    """Simula o comportamento do csv.DictReader criando dicionários dinamicamente."""
    dados_lista = []
    if not os.path.exists(caminho_arquivo) or os.path.getsize(caminho_arquivo) == 0:
        return dados_lista
        
    arq = open(caminho_arquivo, 'r', encoding='utf-8')
    linhas = arq.read().splitlines()
    arq.close()
    
    if len(linhas) <= 1:
        return dados_lista
        
    cabecalhos = separar_linha_csv(linhas[0])
    
    for linha in linhas[1:]:
        if not linha.strip():
            continue
        valores = separar_linha_csv(linha)
        
        dicionario_linha = {}
        for i, cabecalho in enumerate(cabecalhos):
            if i < len(valores):
                dicionario_linha[cabecalho] = valores[i]
            else:
                dicionario_linha[cabecalho] = ""
        dados_lista.append(dicionario_linha)
        
    return dados_lista

def salvar_csv_dinamico(caminho_arquivo, cabecalhos, lista_dicionarios):
    """Simula o comportamento do csv.DictWriter reescrevendo o arquivo com segurança."""
    arq = open(caminho_arquivo, 'w', encoding='utf-8')
    arq.write(",".join(cabecalhos) + "\n")
    for d in lista_dicionarios:
        valores = [d.get(c, "") for c in cabecalhos]
        arq.write(formatar_linha_csv(valores))
    arq.close()


# ==========================================================================
# GERENCIAMENTO DE USUÁRIOS (Python Puro)
# ==========================================================================

def ler_usuarios():
    return ler_csv_dinamico(CSV_PATH)

def salvar_usuario(username, email, password_hash):
    precisa_cabecalho = not os.path.exists(CSV_PATH) or os.path.getsize(CSV_PATH) == 0
    arq = open(CSV_PATH, 'a', encoding='utf-8')
    if precisa_cabecalho:
        arq.write("username,email,password_hash\n")
    arq.write(formatar_linha_csv([username, email, password_hash]))
    arq.close()

def buscar_email(email):
    for usuario in ler_usuarios():
        if usuario['email'] == email:
            return usuario
    return None

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
    salvar_csv_dinamico(CSV_PATH, ['username', 'email', 'password_hash'], usuarios)

def excluir_usuario(username):
    usuarios = ler_usuarios()
    usuarios_filtrados = [u for u in usuarios if u['username'] != username]
    salvar_csv_dinamico(CSV_PATH, ['username', 'email', 'password_hash'], usuarios_filtrados)


# ==========================================================================
# GERENCIAMENTO DE PONTOS TURÍSTICOS (Python Puro)
# ==========================================================================

def ler_pontos():
    pontos = ler_csv_dinamico('data/pontos.csv')
    for row in pontos:
        row['avaliacao'] = float(row['avaliacao']) if row['avaliacao'] else 0.0
        row['dicas'] = row['dicas'].split('|') if row['dicas'] else []
        row['categoria'] = row['categoria'].split('|') if row['categoria'] else []
    return pontos


# ==========================================================================
# GERENCIAMENTO DE COMENTÁRIOS (Python Puro)
# ==========================================================================

def ler_comentarios():
    return ler_csv_dinamico('data/comentarios.csv')

def escrever_comentario(ponto_id, autor, texto):
    comentarios = ler_comentarios()
    novo_id = str(len(comentarios) + 1)
    data_hoje = datetime.now().strftime('%d/%m/%Y')
    
    # Sanitização para evitar quebras físicas de linha no arquivo de texto comum
    texto_limpo = texto.replace('\n', ' ').replace('\r', ' ')
    
    caminho = 'data/comentarios.csv'
    precisa_cabecalho = not os.path.exists(caminho) or os.path.getsize(caminho) == 0
    
    arq = open(caminho, 'a', encoding='utf-8')
    if precisa_cabecalho:
        arq.write("id,ponto_id,autor,data,texto\n")
    arq.write(formatar_linha_csv([novo_id, str(ponto_id), autor, data_hoje, texto_limpo]))
    arq.close()

def atualizar_autor_comentarios(nome_antigo, nome_novo):
    comentarios = ler_comentarios()
    for comentario in comentarios:
        if comentario['autor'] == nome_antigo:
            comentario['autor'] = nome_novo
    salvar_csv_dinamico('data/comentarios.csv', ['id', 'ponto_id', 'autor', 'data', 'texto'], comentarios)

def excluir_comentarios_usuario(username):
    comentarios = ler_comentarios()
    comentarios_filtrados = [c for c in comentarios if c['autor'] != username]
    salvar_csv_dinamico('data/comentarios.csv', ['id', 'ponto_id', 'autor', 'data', 'texto'], comentarios_filtrados)

def editar_comentario(comentario_id, novo_texto):
    comentarios = ler_comentarios()
    texto_limpo = novo_texto.replace('\n', ' ').replace('\r', ' ')
    for comentario in comentarios:
        if int(comentario['id']) == comentario_id:
            comentario['texto'] = texto_limpo
            break
    salvar_csv_dinamico('data/comentarios.csv', ['id', 'ponto_id', 'autor', 'data', 'texto'], comentarios)

def excluir_comentario(comentario_id):
    comentarios = ler_comentarios()
    comentarios_filtrados = [c for c in comentarios if int(c['id']) != comentario_id]
    salvar_csv_dinamico('data/comentarios.csv', ['id', 'ponto_id', 'autor', 'data', 'texto'], comentarios_filtrados)