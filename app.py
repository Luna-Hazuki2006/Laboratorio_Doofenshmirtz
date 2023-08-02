from flask import Flask, render_template, request, redirect, url_for, flash
from bson.objectid import ObjectId
from validaciones import validar_categoria, validar_examen, validar_indicacion
from db import examenes, categorias, indicaciones
# ) xbox fruit 2 PARK LAPTOP walmart 8 . _ golf USA korean JACK ? ~ 
app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = ')xf2PLw8._gUkJ?~'

@app.route('/', methods=['GET'])
def listar_examenes():
    servicios = examenes.find()
    return render_template('/examenes/index.html')

@app.route('/crear_examen', methods=['GET', 'POST'])
def crear_examen():
    if request.method == 'POST':
        forma = request.form
        nuevo_examen = {
            'id': forma['id'], 
            'nombre:': forma['nombre'], 
            'estatus': 'A'
        }
        if validar_examen(nuevo_examen):
            id = examenes.insert_one(nuevo_examen).inserted_id
            if id:
                flash('Examen creado con éxito')
                return redirect(url_for('listar_examenes'))
            else: 
                flash('Ocurrió un error guardando')
    return render_template('/examenes/index.html')

@app.route('/<id>/consultar_examen', methods=['GET'])
def consultar_examen(id):
    oid = ObjectId(id)
    examen = examenes.find_one({'_id': oid})
    return render_template('/examenes/index.html', examen=examen)

@app.route('/<id>/actualizar_examen', methods=['GET', 'POST'])
def actualizar_examen(id):
    oid = ObjectId(id)
    viejo_examen = examenes.find_one({'_id': oid})

    if not viejo_examen:
        flash('Examen no encontrado')
        return redirect(url_for('listar_examenes'))
    
    if request.method == 'POST':
        forma = request.form
        nuevo_examen = {
            'id': forma['id'], 
            'nombre:': forma['nombre'], 
            'estatus': 'A'
        }
        if validar_examen(nuevo_examen):
            examenes.replace_one({'_id': oid}, nuevo_examen)
            return redirect(url_for('listar_examenes'))
    return render_template('/examenes/index.html', viejo_examen=viejo_examen)

@app.route('/<id>/eliminar_examen', methods=['GET', 'POST'])
def eliminar_examen(id):
    oid = ObjectId(id)
    viejo_examen = examenes.find_one({'_id': oid})

    if not viejo_examen:
        flash('Examen no encontrado')
        return redirect(url_for('listar_examenes'))
    
    if request.method == 'POST':
        examenes.delete_one({'_id': oid})
        flash('Examen eliminado con éxito')
        return redirect(url_for('buscar_clases'))
    return render_template('/eliminar/index.html', viejo_examen=viejo_examen)

@app.route('/listar_indicaciones', methods=['GET'])
def listar_indicaciones():
    indicados = indicaciones.find()
    return render_template('/indicaciones/index.html')

@app.route('/crear_indicacion', methods=['GET', 'POST'])
def crear_indicacion():
    if request.method == 'POST':
        forma = request.form
        nueva_indicacion = {
            'id': forma['id'], 
            'nombre:': forma['nombre'], 
            'estatus': 'A'
        }
        if validar_indicacion(nueva_indicacion):
            id = indicaciones.insert_one(nueva_indicacion).inserted_id
            if id:
                flash('Indicación creada con éxito')
                return redirect(url_for('listar_indicaciones'))
            else: 
                flash('Ocurrió un error guardando')
    return render_template('/indicaciones/index.html')

@app.route('/<id>/consultar_indicacion', methods=['GET'])
def consultar_indicacion(id):
    oid = ObjectId(id)
    indicacion = indicaciones.find_one({'_id': oid})
    return render_template('/indicaciones/index.html', indicacion=indicacion)

@app.route('/<id>/actualizar_indicacion', methods=['GET', 'POST'])
def actualizar_indicacion(id):
    oid = ObjectId(id)
    vieja_indicacion = indicaciones.find_one({'_id': oid})

    if not vieja_indicacion:
        flash('Indicación no encontrada')
        return redirect(url_for('listar_indicaciones'))
    
    if request.method == 'POST':
        forma = request.form
        nueva_indicacion = {
            'id': forma['id'], 
            'nombre:': forma['nombre'], 
            'estatus': 'A'
        }
        if validar_indicacion(nueva_indicacion):
            indicaciones.replace_one({'_id': oid}, nueva_indicacion)
            return redirect(url_for('listar_indicaciones'))
    return render_template('/indicaciones/index.html', vieja_indicacion=vieja_indicacion)

@app.route('/<id>/eliminar_indicacion', methods=['GET', 'POST'])
def eliminar_indicacion(id):
    oid = ObjectId(id)
    vieja_categoria = indicaciones.find_one({'_id': oid})

    if not vieja_categoria:
        flash('Categoría no encontrada')
        return redirect(url_for('listar_categorias'))
    
    if request.method == 'POST':
        indicaciones.delete_one({'_id': oid})
        flash('Indicación eliminada con éxito')
        return redirect(url_for('listar_indicaciones'))
    return render_template('/indicaciones/index.html', vieja_categoria=vieja_categoria)

@app.route('/listar_categorias', methods=['GET'])
def listar_categorias():
    divisiones = categorias.find()
    return render_template('/categorias/index.html')

@app.route('/crear_categorias', methods=['GET', 'POST'])
def crear_categorias():
    if request.method == 'POST':
        forma = request.form
        nueva_categoria = {
            'id': forma['id'], 
            'nombre:': forma['nombre'], 
            'estatus': 'A'
        }
        if validar_categoria(nueva_categoria):
            id = categorias.insert_one(nueva_categoria).inserted_id
            if id:
                flash('Categoría creada con éxito')
                return redirect(url_for('buscar_clases'))
            else: 
                flash('Ocurrió un error guardando')
    return render_template('/categorias/index.html')

@app.route('/<id>/consultar_categoria', methods=['GET'])
def consultar_categorias(id):
    oid = ObjectId(id)
    categoria = categorias.find_one({'_id': oid})
    return render_template('/catogorias/index.html', categoria=categoria)

@app.route('/<id>/actualizar_categoria', methods=['GET', 'POST'])
def actualizar_categoria(id):
    oid = ObjectId(id)
    vieja_categoria = categorias.find_one({'_id': oid})

    if not vieja_categoria:
        flash('Categoría no encontrada')
        return redirect(url_for('listar_categorias'))
    
    if request.method == 'POST':
        forma = request.form
        nueva_categoria = {
            'id': forma['id'], 
            'nombre:': forma['nombre'], 
            'estatus': 'A'
        }
        if validar_categoria(nueva_categoria):
            categorias.replace_one({'_id': oid}, nueva_categoria)
            return redirect(url_for('buscar_clases'))
    return render_template('/actualizar/index.html', vieja_categoria=vieja_categoria)

@app.route('/<id>/eliminar_categoria', methods=['GET', 'POST'])
def eliminar_categoria(id):
    oid = ObjectId(id)
    vieja_categoria = categorias.find_one({'_id': oid})

    if not vieja_categoria:
        flash('Categoría no encontrada')
        return redirect(url_for('listar_categorias'))
    
    if request.method == 'POST':
        categorias.delete_one({'_id': oid})
        flash('Categoría eliminada con éxito')
        return redirect(url_for('listar_categorias'))
    return render_template('/categorias/index.html', vieja_categoria=vieja_categoria)

if __name__ == '__main__':
    app.run(debug=True)