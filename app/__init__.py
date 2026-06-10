from flask import Flask

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config['SECRET_KEY']='vem-pra-jampa-2026'


from app import routes
from app.autenticacao import auth
app.register_blueprint(auth)