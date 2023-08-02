from flask import Flask, render_template, request, redirect, url_for, flash
from bson.objectid import ObjectId
from db import materias, categorias, indicaciones
# ) xbox fruit 2 PARK LAPTOP walmart 8 . _ golf USA korean JACK ? ~ 
app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = ')xf2PLw8._gUkJ?~'

@app.route('/', methods=['GET'])
def listar_examenes():
    pass

@app.route('/crear_examen', methods=['GET', 'POST'])
def crear_examen():
    pass

@app.route('/<id>/consultar_examen', methods=['GET'])
def consultar_examen(id):
    pass

@app.route('/<id>/actualizar_examen', methods=['GET', 'POST'])
def actualizar_examen(id):
    pass

@app.route('/<id>/eliminar_examen', methods=['GET', 'POST'])
def eliminar_examen(id):
    pass

@app.route('/listar_indicaciones', methods=['GET'])
def listar_indicaciones():
    pass

@app.route('/crear_indicacion', methods=['GET', 'POST'])
def crear_indicacion():
    pass

@app.route('/<id>/consultar_indicacion', methods=['GET'])
def consultar_indicacion(id):
    pass

@app.route('/<id>/actualizar_indicacion', methods=['GET', 'POST'])
def actualizar_indicacion(id):
    pass

@app.route('/<id>/eliminar_indicacion', methods=['GET', 'POST'])
def eliminar_indicacion(id):
    pass

@app.route('/listar_categorias', methods=['GET'])
def listar_categorias():
    pass

@app.route('/crear_categorias', methods=['GET', 'POST'])
def crear_categorias():
    pass

@app.route('/<id>/consultar_categoria', methods=['GET'])
def consultar_categorias(id):
    pass

@app.route('/<id>/actualizar_categoria', methods=['GET', 'POST'])
def actualizar_categoria(id):
    pass

@app.route('/<id>/eliminar_categoria', methods=['GET', 'POST'])
def eliminar_categoria(id):
    pass

if __name__ == '__main__':
    app.run(debug=True)