import csv
from datetime import datetime
from flask import render_template, request, redirect, url_for, flash
from app import app

# =====================
# FUNÇÕES DE LEITURA E ESCRITA (CSV)
# =====================

def ler_pontos():
    pontos = []
    try:
        with open('data/pontos.csv', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                row['avaliacao'] = float(row['avaliacao'])
                # Converte as dicas textuais separadas por '|' em uma lista do Python
                row['dicas'] = row['dicas'].split('|') if row['dicas'] else []
                pontos.append(row)
    except FileNotFoundError:
        pass
    return pontos


def ler_comentarios():
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
    comentarios = ler_comentarios()
    novo_id = str(len(comentarios) + 1)
    data_hoje = datetime.now().strftime('%d/%m/%Y')

    with open('data/comentarios.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['id', 'ponto_id', 'autor', 'data', 'texto'])
        writer.writerow({
            'id': novo_id,
            'ponto_id': str(ponto_id),
            'autor': autor,
            'data': data_hoje,
            'texto': texto
        })


# =====================
# ROTAS DA APLICAÇÃO
# =====================

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/historia")
def historia():
    return render_template("historia.html")


# Sua página principal estática (apenas renderiza o HTML manual)
@app.route("/pontos-turisticos")
def turistico():
    return render_template("pontos.html")


# Rota dinâmica que constrói a página dedicada com base no CSV
@app.route("/pontos-turisticos/<int:ponto_id>")
def ponto_detalhe(ponto_id):
    pontos = ler_pontos()

    ponto = None
    for p in pontos:
        if int(p['id']) == ponto_id:
            ponto = p
            break

    # Caso alguém digite um ID que não existe no CSV (Ex: /pontos-turisticos/999)
    if ponto is None:
        return render_template("404.html"), 404

    # Busca e filtra os comentários específicos deste ponto turístico
    todos_comentarios = ler_comentarios()
    comentarios_filtrados = [c for c in todos_comentarios if int(c['ponto_id']) == ponto_id]

    # Renderiza o arquivo que você possui para os detalhes ('card_base.html')
    return render_template("card_base.html", ponto=ponto, comentarios=comentarios_filtrados)


# Rota para receber o formulário de comentários (via POST)
@app.route("/pontos-turisticos/<int:ponto_id>/comentar", methods=["POST"])
def comentar(ponto_id):
    autor = request.form.get("autor")
    texto = request.form.get("texto")
    
    if autor and texto:
        escrever_comentario(ponto_id, autor, texto)
        flash("Comentário adicionado com sucesso!", "success")
    else:
        flash("Por favor, preencha todos os campos.", "warning")
        
    return redirect(url_for('ponto_detalhe', ponto_id=ponto_id))