from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from app import app
from app.utils import salvar_usuario, buscar_email

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
            flash('Email ou senha incorretos.')
            return redirect(url_for('auth.login'))
        
        session['usuario']=usuario['username']
        return redirect(url_for('index'))
    return render_template('login.html')

@auth.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('index'))