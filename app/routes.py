from flask import render_template
from app import app

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/historia")
def historia():
    return render_template("historia.html")

@app.route("/pontos")
def turistico():
    return render_template("pontos.html")