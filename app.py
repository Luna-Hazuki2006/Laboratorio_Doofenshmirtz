from flask import Flask, render_template, request, redirect, url_for, flash
from bson.objectid import ObjectId
from db import materias, categorias, indicaciones
# ) xbox fruit 2 PARK LAPTOP walmart 8 . _ golf USA korean JACK ? ~ 
app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = ')xf2PLw8._gUkJ?~'

@app.route('/', methods=['GET'])
def listar_servicios():
    pass

@app.route('/crear_examen', methods=['GET', 'POST'])
def crear_examen():
    pass

@app.route('/<id>/actualizar', methods=['GET', 'POST'])
def actualizar_examen(id):
    pass

@app.route('/<id>/eliminar', methods=['GET', 'POST'])
def eliminar_examen(id):
    pass



if __name__ == '__main__':
    app.run(debug=True)