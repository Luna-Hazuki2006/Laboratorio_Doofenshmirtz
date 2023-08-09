from flask import Flask, render_template, request, redirect, url_for, flash
from bson.objectid import ObjectId
from validaciones import validar_categoria, validar_examen, validar_indicacion
from db import examenes, categorias, indicaciones, tipos, usuarios
# ) xbox fruit 2 PARK LAPTOP walmart 8 . _ golf USA korean JACK ? ~ 
app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = ')xf2PLw8._gUkJ?~'

@app.route('/', methods=['GET'])
def listar_examenes():
    servicios = examenes.find({'estatus': 'A'})
    divisiones = categorias.find({'estatus': 'A'})
    caracteristicas = tipos.find({'estatus': 'A'})
    print(servicios)
    return render_template('/examenes/listar/index.html', servicios=servicios, divisiones=divisiones, caracteristicas=caracteristicas)

@app.route('/<categoria>/filtrar_examenes')
def filtrar_examenes_categorias(categoria):
    servicios = examenes.find({'categoria': categoria, 'estatus': 'A'})
    return render_template('/examenes/listar/index.html', servicios=servicios)

@app.route('/<tipo>/filtrar_examenes_tipo')
def filtrar_examenes_tipos(tipo):
    servicios = examenes.find({'tipo': tipo, 'estatus': 'A'})
    return render_template('/examenes/listar/index.html', servicios=servicios)

@app.route('/crear_examen', methods=['GET', 'POST'])
def crear_examen():
    if request.method == 'POST':
        forma = request.form
        id = len(examenes.find({'estatus': 'A'}))
        id = "A" + id
        nuevo_examen = {
            'id': forma['id'], 
            'nombre:': forma['nombre'], 
            'categoria': categorias.find({'nombre': forma['categoria']}), 
            'tipo': forma['tipo'], 
            'precio': forma['precio'], 
            'indicaciones': forma['indicaciones'], 
            'estatus': 'A'
        }
        if validar_examen(nuevo_examen):
            id = examenes.insert_one(nuevo_examen).inserted_id
            if id:
                flash('Examen creado con éxito')
                return redirect(url_for('listar_examenes'))
            else: 
                flash('Ocurrió un error guardando')
    return render_template('/examenes/agregar/index.html')

@app.route('/<id>/consultar_examen', methods=['GET'])
def consultar_examen(id):
    examen = examenes.find_one({'id': id, 'estatus': 'A'})
    print(examen)
    return render_template('/examenes/consultar/index.html', examen=examen)

@app.route('/<id>/actualizar_examen', methods=['GET', 'POST'])
def actualizar_examen(id):
    oid = ObjectId(id)
    viejo_examen = examenes.find_one({'_id': oid, 'estatus': 'A'})

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
    return render_template('/examenes/actualizar/index.html', viejo_examen=viejo_examen)

@app.route('/<id>/eliminar_examen', methods=['GET', 'POST'])
def eliminar_examen(id):
    oid = ObjectId(id)
    viejo_examen = examenes.find_one({'_id': oid, 'estatus': 'A'})

    if not viejo_examen:
        flash('Examen no encontrado')
        return redirect(url_for('listar_examenes'))
    
    if request.method == 'POST':
        examenes.delete_one({'_id': oid, 'estatus': 'A'})
        flash('Examen eliminado con éxito')
        return redirect(url_for('buscar_clases'))
    return render_template('/eliminar/eliminar/index.html', viejo_examen=viejo_examen)

@app.route('/listar_indicaciones', methods=['GET'])
def listar_indicaciones():
    indicados = indicaciones.find({'estatus': 'A'})
    return render_template('/indicaciones/listar/index.html', indicados=indicados)

@app.route('/crear_indicacion', methods=['GET', 'POST'])
def crear_indicacion():
    if request.method == 'POST':
        forma = request.form
        nueva_indicacion = {
            'id': forma['id'], 
            'informacion:': forma['nombre'], 
            'estatus': 'A'
        }
        if validar_indicacion(nueva_indicacion):
            id = indicaciones.insert_one(nueva_indicacion).inserted_id
            if id:
                flash('Indicación creada con éxito')
                return redirect(url_for('listar_indicaciones'))
            else: 
                flash('Ocurrió un error guardando')
    return render_template('/indicaciones/agregar/index.html')

@app.route('/<id>/consultar_indicacion', methods=['GET'])
def consultar_indicacion(id):
    indicacion = indicaciones.find_one({'id': id, 'estatus': 'A'})
    return render_template('/indicaciones/consultar/index.html', indicacion=indicacion)

@app.route('/<id>/actualizar_indicacion', methods=['GET', 'POST'])
def actualizar_indicacion(id):
    oid = ObjectId(id)
    vieja_indicacion = indicaciones.find_one({'_id': oid, 'estatus': 'A'})

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
    return render_template('/indicaciones/actualizar/index.html', vieja_indicacion=vieja_indicacion)

@app.route('/<id>/eliminar_indicacion', methods=['GET', 'POST'])
def eliminar_indicacion(id):
    oid = ObjectId(id)
    vieja_categoria = indicaciones.find_one({'_id': oid, 'estatus': 'A'})

    if not vieja_categoria:
        flash('Categoría no encontrada')
        return redirect(url_for('listar_categorias'))
    
    if request.method == 'POST':
        indicaciones.delete_one({'_id': oid, 'estatus': 'A'})
        flash('Indicación eliminada con éxito')
        return redirect(url_for('listar_indicaciones'))
    return render_template('/indicaciones/eliminar/index.html', vieja_categoria=vieja_categoria)

@app.route('/listar_categorias', methods=['GET'])
def listar_categorias():
    divisiones = categorias.find({'estatus': 'A'})
    return render_template('/categorias/listar/index.html', divisiones=divisiones)

@app.route('/crear_categorias', methods=['GET', 'POST'])
def crear_categoria():
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
    return render_template('/categorias/agregar/index.html')

@app.route('/<id>/consultar_categoria', methods=['GET'])
def consultar_categoria(id):
    categoria = categorias.find_one({'id': id, 'estatus': 'A'})
    return render_template('/categorias/consultar/index.html', categoria=categoria)

@app.route('/<id>/actualizar_categoria', methods=['GET', 'POST'])
def actualizar_categoria(id):
    vieja_categoria = categorias.find_one({'id': id, 'estatus': 'A'})

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
            categorias.replace_one({'id': id, 'estatus': 'A'}, nueva_categoria)
            return redirect(url_for('buscar_clases'))
    return render_template('/categorias/actualizar/index.html', vieja_categoria=vieja_categoria)

@app.route('/<id>/eliminar_categoria', methods=['GET', 'POST'])
def eliminar_categoria(id):
    oid = ObjectId(id)
    vieja_categoria = categorias.find_one({'_id': oid, 'estatus': 'A'})

    if not vieja_categoria:
        flash('Categoría no encontrada')
        return redirect(url_for('listar_categorias'))
    
    if request.method == 'POST':
        categorias.delete_one({'_id': oid, 'estatus': 'A'})
        flash('Categoría eliminada con éxito')
        return redirect(url_for('listar_categorias'))
    return render_template('/categorias/eliminar/index.html', vieja_categoria=vieja_categoria)

@app.route('/reportes', methods=['GET'])
def reportes():
    return render_template('/reportes/index.html')

if __name__ == '__main__':
    app.run(debug=True)