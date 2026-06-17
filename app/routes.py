from flask import render_template, request, redirect, url_for, flash, session
from app import app
from app.utils import ler_pontos, ler_comentarios, escrever_comentario, editar_comentario

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/historia")
def historia():
    return render_template("historia.html")


@app.route("/pontos-turisticos")
def turistico():
    pontos_lista = ler_pontos()
    return render_template("pontos.html", pontos=pontos_lista)


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
    autor = session.get("usuario")
    
    if not autor:
        flash("Você precisa estar logado para comentar.", "erro")
        return redirect(url_for('auth.login'))
    
    texto = request.form.get('texto')

    if texto:
        escrever_comentario(ponto_id, autor, texto)
        flash('Comentario adicionado com sucesso!', 'success')

    else:
        flash('Por favor, escreva um comentario.', 'warning')
    
    return redirect(url_for('ponto_detalhe', ponto_id=ponto_id))

@app.route("/pontos-turisticos/<int:ponto_id>/comentario/<int:comentario_id>/editar", methods=["POST"])
def editar_comentario_rota(ponto_id, comentario_id):
    usuario_logado = session.get('usuario')

    if not usuario_logado:
        flash('Voce precisa estar logado para editar comenários.', 'erro')
        return redirect(url_for('auth.login'))
    
    comentarios = ler_comentarios()
    comentario = None

    for c in comentarios:
        if int(c['id']) == comentario_id:
            comentario = c
            break
    
    if comentario is None or comentario['autor'] != usuario_logado:
        flash('Você não tem permissão para editar este comentário.', 'erro')
        return redirect(url_for('ponto_detalhe', ponto_id = ponto_id))
    
    novo_texto = request.form.get('texto')

    if novo_texto:
        editar_comentario(comentario_id, novo_texto)
        flash('Comentario atualizado com sucesso!', 'success')
    else:
        flash('O comentário não pode ficar vazio.', 'warning')

    return redirect(url_for('ponto_detalhe', ponto_id=ponto_id))