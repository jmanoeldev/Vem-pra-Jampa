from flask import render_template, request, redirect, url_for, flash
from app import app
from app.utils import ler_pontos, ler_comentarios, escrever_comentario

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/historia")
def historia():
    return render_template("historia.html")


@app.route("/pontos-turisticos")
def turistico():
    return render_template("pontos.html")


@app.route("/pontos-turisticos/<int:ponto_id>")
def ponto_detalhe(ponto_id):
    pontos = ler_pontos()

    ponto = None
    for p in pontos:
        if int(p['id']) == ponto_id:
            ponto = p
            break

    if ponto is None:
        return render_template("404.html"), 404

    # Busca e filtra os comentários específicos deste ponto turístico
    todos_comentarios = ler_comentarios()
    comentarios_filtrados = [c for c in todos_comentarios if int(c['ponto_id']) == ponto_id]

    return render_template("card_base.html", ponto=ponto, comentarios=comentarios_filtrados)


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