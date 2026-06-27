from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from app import app
from app.utils import salvar_usuario, buscar_email, buscar_usuario_por_username, atualizar_usuario, atualizar_autor_comentarios, excluir_usuario, excluir_comentarios_usuario

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method=='POST':
        username=request.form.get('username')
        email=request.form.get('email')
        password=request.form.get('password')

        if buscar_email(email):
            flash('Este email já foi cadastrado.', "erro")
            return render_template('cadastro.html')
        
        password_hash = generate_password_hash(password)
        salvar_usuario(username, email, password_hash)
        flash('Cadastro realizado com sucesso!', "sucesso")
        return redirect(url_for('auth.login'))
            
    return render_template('cadastro.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email=request.form.get('email')
        password=request.form.get('password')

        usuario = buscar_email(email)

        if not usuario or not check_password_hash(usuario['password_hash'], password):
            flash('Email ou senha incorretos.', 'erro')
            return redirect(url_for('auth.login'))
        
        session['usuario']=usuario['username']
        return redirect(url_for('index'))
    return render_template('login.html')

@auth.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('index'))

@auth.route('/perfil', methods=['GET', 'POST'])
def perfil():

    if 'usuario' not in session:
        flash('Faça login para acessar seu perfil.', 'erro')
        return redirect(url_for('auth.login'))

    usuario = buscar_usuario_por_username(session['usuario'])

    if request.method == 'POST':

        novo_username = request.form.get('username').strip()
        novo_email = request.form.get('email').strip()

        nova_senha = request.form.get('password')
        confirmar_senha = request.form.get('confirm_password')

        if not novo_username:

            flash('O nome é obrigatório.', 'erro')

            return redirect(url_for('auth.perfil'))

        if not novo_email:

            flash('O e-mail é obrigatório.', 'erro')

            return redirect(url_for('auth.perfil'))
        
        if len(novo_username) < 3:

            flash('O nome deve possuir pelo menos 3 caracteres.', 'erro')

            return redirect(url_for('auth.perfil'))

        usuario_email = buscar_email(novo_email)

        if (usuario_email and usuario_email['email'] != usuario['email']):
            flash('Este e-mail já está sendo utilizado.','erro')

            return redirect(url_for('auth.perfil'))
        
        if nova_senha or confirmar_senha:

            if nova_senha != confirmar_senha:

                flash('As senhas não coincidem.','erro')

                return redirect(url_for('auth.perfil'))

            if len(nova_senha) < 8:
                flash('A senha deve possuir pelo menos 8 caracteres.', 'erro')

                return redirect(url_for('auth.perfil'))
            
        if nova_senha:  
            password_hash = generate_password_hash(nova_senha)
            
        else:
            password_hash = usuario['password_hash']
            
        atualizar_usuario(
            usuario['username'],
            novo_username,
            novo_email,
            password_hash
        )

        if usuario['username'] != novo_username:

            atualizar_autor_comentarios(usuario['username'], novo_username)

        session['usuario'] = novo_username

        flash('Perfil atualizado com sucesso.','sucesso')

        return redirect(url_for('auth.perfil'))
        

    return render_template('perfil.html', usuario=usuario)

@auth.route('/perfil/excluir')
def confirmar_exclusao():

    if 'usuario' not in session:

        flash('Faça login para acessar esta página.', 'erro')

        return redirect(url_for('auth.login'))

    return render_template('confirmar_exclusao.html')

@auth.route('/perfil/excluir/confirmar', methods=['POST'])
def excluir_perfil():

    if 'usuario' not in session:

        flash('Faça login para continuar.','erro')

        return redirect(url_for('auth.login'))

    username = session['usuario']

    excluir_comentarios_usuario(username)
    excluir_usuario(username)

    session.pop('usuario', None)

    flash('Sua conta foi excluída com sucesso.','sucesso')

    return redirect(url_for('index'))