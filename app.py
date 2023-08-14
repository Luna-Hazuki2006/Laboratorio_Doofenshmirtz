from flask import Flask, render_template, request, redirect, url_for, flash
from pprint import pprint
from validaciones import validar_categoria, validar_examen, validar_indicacion, validar_tipos
from db import examenes, categorias, indicaciones, tipos, usuarios
# ) xbox fruit 2 PARK LAPTOP walmart 8 . _ golf USA korean JACK ? ~ 
app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = ')xf2PLw8._gUkJ?~'

@app.route('/', methods=['GET', 'POST'])
def listar_examenes():
    servicios = examenes.find({'estatus': 'A'})
    divisiones = categorias.find({'estatus': 'A'})
    caracteristicas = tipos.find({'estatus': 'A'})
    if request.method == 'POST': 
        forma = request.form
        tipo = forma['tipo']
        categoria = forma['categoria']
        print(tipo)
        print(categoria)
        servicios = filtrar_examenes(categoria, tipo)
        return render_template('/examenes/listar/index.html', 
                                servicios=servicios, 
                                divisiones=divisiones, 
                                caracteristicas=caracteristicas)
    return render_template('/examenes/listar/index.html', 
                           servicios=servicios, 
                           divisiones=divisiones, 
                           caracteristicas=caracteristicas)

def filtrar_examenes(categoria, tipo):
    servicios = []
    if len(tipo) != 0 and len(categoria) != 0:
        print('si y si')
        categoria = categorias.find_one({'id': categoria, 'estatus': 'A'})
        tipo = tipos.find_one({'id': tipo, 'estatus': 'A'})
        servicios = examenes.find({'categoria': categoria, 'tipo': tipo, 'estatus': 'A'})
    elif len(tipo) == 0 and len(categoria) != 0: 
        print('no y si')
        categoria = categorias.find_one({'id': categoria, 'estatus': 'A'})
        servicios = examenes.find({'categoria': categoria, 'estatus': 'A'})
    elif len(tipo) != 0 and len(categoria) == 0: 
        print('si y no')
        tipo = tipos.find_one({'id': tipo, 'estatus': 'A'})
        servicios = examenes.find({'tipo': tipo, 'estatus': 'A'})
    else: 
        print('no y no')
        servicios = examenes.find({'estatus': 'A'})
    return servicios

@app.route('/crear_examen', methods=['GET', 'POST'])
def crear_examen():
    divisiones = categorias.find({'estatus': 'A'})
    caracteristicas = tipos.find({'estatus': 'A'})
    descripciones = indicaciones.find({'estatus': 'A'})
    if request.method == 'POST':
        forma = request.form
        numero = examenes.count_documents({}) + 1
        # pprint(forma['categoria'])
        # pprint(forma['indicacion'])
        # print(forma['tipo'])
        # print(forma['precio'])
        # print(forma['nombre'])
        # pprint(forma['categoria'])
        # pprint(forma['tipo'])
        # pprint(forma['indicacion'])
        lista = []
        # for indica in descripciones:
            # pprint(forma['indicacion'])
            # if indica['id'] == forma[indica['id']]:
            #     lista.append(forma[indica['id']])
            #     pprint(forma[indica['id']])
        pprint(request.form.getlist('check'))
        for item in request.form.getlist('check'):
            lista.append(indicaciones.find_one(item))
        nuevo_examen = {
            'id': 'E' + str(numero), 
            'nombre': forma['nombre'], 
            'categoria': categorias.find_one({'id': forma['categoria'], 'estatus': 'A'}), 
            'tipo': tipos.find_one({'id': forma['tipo'], 'estatus': 'A'}), 
            'precio': forma['precio'], 
            'indicaciones': indicaciones.find_one({'id': forma['indicacion'], 'estatus': 'A'}), 
            'estatus': 'A'
        }
        if validar_examen(nuevo_examen):
            id = examenes.insert_one(nuevo_examen).inserted_id
            if id:
                flash('Examen creado con éxito')
                return redirect(url_for('listar_examenes'))
            else: 
                flash('Ocurrió un error guardando')
    return render_template('/examenes/agregar/index.html', 
                           divisiones=divisiones, 
                           caracteristicas=caracteristicas, 
                           descripciones=descripciones)

@app.route('/<id>/consultar_examen', methods=['GET'])
def consultar_examen(id):
    examen = examenes.find_one({'id': id, 'estatus': 'A'})
    print(examen)
    return render_template('/examenes/consultar/index.html', examen=examen)

@app.route('/<id>/actualizar_examen', methods=['GET', 'POST'])
def actualizar_examen(id):
    viejo_examen = examenes.find_one({'id': id, 'estatus': 'A'})
    divisiones = categorias.find({'estatus': 'A'})
    caracteristicas = tipos.find({'estatus': 'A'})
    descripciones = indicaciones.find({'estatus': 'A'})

    if not viejo_examen:
        flash('Examen no encontrado')
        return redirect(url_for('listar_examenes'))
    
    if request.method == 'POST':
        forma = request.form
        pprint(forma['tipo'])
        pprint(forma['categoria'])
        pprint(forma['indicacion'])
        lista = []
        for indica in descripciones:
            pprint(forma['indicacion'])
            if indica['id'] == forma[indica['id']]:
                lista.append(forma[indica['id']])
                pprint(forma[indica['id']])
        pprint(lista)
        nuevo_examen = {
            'id': viejo_examen['id'], 
            'nombre': forma['nombre'], 
            'categoria': categorias.find_one({'id': forma['categoria'], 'estatus': 'A'}), 
            'tipo': tipos.find_one({'id': forma['tipo'], 'estatus': 'A'}), 
            'precio': forma['precio'], 
            'indicaciones': indicaciones.find_one({'id': forma['indicacion'], 'estatus': 'A'}) , 
            'estatus': 'A'
        }
        pprint(nuevo_examen)
        if validar_examen(nuevo_examen):
            examenes.replace_one({'id': id}, nuevo_examen)
            return redirect(url_for('listar_examenes'))
    return render_template('/examenes/actualizar/index.html', 
                           viejo_examen=viejo_examen, 
                           divisiones=divisiones, 
                           caracteristicas=caracteristicas, 
                           descripciones=descripciones)

@app.route('/<id>/eliminar_examen', methods=['GET', 'POST'])
def eliminar_examen(id):
    viejo_examen = examenes.find_one({'id': id, 'estatus': 'A'})

    if not viejo_examen:
        flash('Examen no encontrado')
        return redirect(url_for('listar_examenes'))
    
    examen_eliminado = {
        'id': viejo_examen['id'], 
        'nombre': viejo_examen['nombre'], 
        'categoria': viejo_examen['categoria'], 
        'tipo': viejo_examen['tipo'], 
        'precio': viejo_examen['precio'], 
        'indicaciones': viejo_examen['indicaciones'], 
        'estatus': 'I'
    }
    
    if request.method == 'POST':
        examenes.replace_one({'id': id, 'estatus': 'A'}, examen_eliminado)
        flash('Examen eliminado con éxito')
        return redirect(url_for('listar_examenes'))
    return render_template('/examenes/eliminar/index.html', viejo_examen=viejo_examen)

@app.route('/listar_indicaciones', methods=['GET'])
def listar_indicaciones():
    indicados = indicaciones.find({'estatus': 'A'})
    return render_template('/indicaciones/listar/index.html', indicados=indicados)

@app.route('/crear_indicacion', methods=['GET', 'POST'])
def crear_indicacion():
    if request.method == 'POST':
        numero = indicaciones.count_documents({}) + 1
        forma = request.form
        nueva_indicacion = {
            'id': 'I' + str(numero), 
            'nombre': forma['nombre'], 
            'explicacion': forma['explicacion'], 
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
    vieja_indicacion = indicaciones.find_one({'id': id, 'estatus': 'A'})

    if not vieja_indicacion:
        flash('Indicación no encontrada')
        return redirect(url_for('listar_indicaciones'))
    
    if request.method == 'POST':
        forma = request.form
        nueva_indicacion = {
            'id': vieja_indicacion['id'], 
            'nombre': forma['nombre'], 
            'explicacion': forma['explicacion'], 
            'estatus': 'A'
        }
        if validar_indicacion(nueva_indicacion):
            indicaciones.replace_one({'id': id}, nueva_indicacion)
            return redirect(url_for('listar_indicaciones'))
    return render_template('/indicaciones/actualizar/index.html', vieja_indicacion=vieja_indicacion)

@app.route('/<id>/eliminar_indicacion', methods=['GET', 'POST'])
def eliminar_indicacion(id):
    vieja_indicacion = indicaciones.find_one({'id': id, 'estatus': 'A'})

    if not vieja_indicacion:
        flash('Categoría no encontrada')
        return redirect(url_for('listar_categorias'))
    
    indicacion_eliminada = {
        'id': vieja_indicacion['id'], 
        'nombre': vieja_indicacion['nombre'], 
        'explicacion': vieja_indicacion['explicacion'], 
        'estatus': 'I'
    }
    
    if request.method == 'POST':
        indicaciones.replace_one({'id': id, 'estatus': 'A'}, indicacion_eliminada)
        flash('Indicación eliminada con éxito')
        return redirect(url_for('listar_indicaciones'))
    return render_template('/indicaciones/eliminar/index.html', vieja_indicacion=vieja_indicacion)

@app.route('/listar_categorias', methods=['GET'])
def listar_categorias():
    divisiones = categorias.find({'estatus': 'A'})
    return render_template('/categorias/listar/index.html', divisiones=divisiones)

@app.route('/crear_categorias', methods=['GET', 'POST'])
def crear_categoria():
    if request.method == 'POST':
        numero = categorias.count_documents({}) + 1
        forma = request.form
        nueva_categoria = {
            'id': 'C' + str(numero), 
            'nombre': forma['nombre'], 
            'descripcion': forma['descripcion'], 
            'estatus': 'A'
        }
        if validar_categoria(nueva_categoria):
            id = categorias.insert_one(nueva_categoria).inserted_id
            if id:
                flash('Categoría creada con éxito')
                return redirect(url_for('listar_categorias'))
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
            'id': vieja_categoria['id'], 
            'nombre': forma['nombre'], 
            'descripcion': forma['descripcion'], 
            'estatus': 'A'
        }
        if validar_categoria(nueva_categoria):
            categorias.replace_one({'id': id, 'estatus': 'A'}, nueva_categoria)
            return redirect(url_for('listar_categorias'))
    return render_template('/categorias/actualizar/index.html', vieja_categoria=vieja_categoria)

@app.route('/<id>/eliminar_categoria', methods=['GET', 'POST'])
def eliminar_categoria(id):
    vieja_categoria = categorias.find_one({'id': id, 'estatus': 'A'})

    if not vieja_categoria:
        flash('Categoría no encontrada')
        return redirect(url_for('listar_categorias'))
    
    categoria_eliminada = {
        'id': vieja_categoria['id'], 
        'nombre': vieja_categoria['nombre'], 
        'descripcion': vieja_categoria['descripcion'], 
        'estatus': 'I'
    }
    
    if request.method == 'POST':
        categorias.replace_one({'id': id, 'estatus': 'A'}, categoria_eliminada)
        flash('Categoría eliminada con éxito')
        return redirect(url_for('listar_categorias'))
    return render_template('/categorias/eliminar/index.html', vieja_categoria=vieja_categoria)

@app.route('/listar_tipos', methods=['GET'])
def listar_tipos():
    diferencias = tipos.find({'estatus': 'A'})
    return render_template('/tipos/listar/index.html', diferencias=diferencias)

@app.route('/crear_tipos', methods=['GET', 'POST'])
def crear_tipo():
    if request.method == 'POST':
        numero = tipos.count_documents({}) + 1
        forma = request.form
        nuevo_tipo = {
            'id': 'C' + str(numero), 
            'nombre': forma['nombre'], 
            'descripcion': forma['descripcion'], 
            'estatus': 'A'
        }
        if validar_tipos(nuevo_tipo):
            id = tipos.insert_one(nuevo_tipo).inserted_id
            if id:
                flash('Tipo creado con éxito')
                return redirect(url_for('listar_tipos'))
            else: 
                flash('Ocurrió un error guardando')
    return render_template('/tipos/agregar/index.html')

@app.route('/<id>/consultar_tipos', methods=['GET'])
def consultar_tipo(id):
    tipo = tipos.find_one({'id': id, 'estatus': 'A'})
    return render_template('/tipos/consultar/index.html', tipo=tipo)

@app.route('/<id>/actualizar_tipo', methods=['GET', 'POST'])
def actualizar_tipo(id):
    viejo_tipo = tipos.find_one({'id': id, 'estatus': 'A'})

    if not viejo_tipo:
        flash('Tipo no encontrado')
        return redirect(url_for('listar_tipos'))
    
    if request.method == 'POST':
        forma = request.form
        nuevo_tipo = {
            'id': viejo_tipo['id'], 
            'nombre': forma['nombre'], 
            'descripcion': forma['descripcion'], 
            'estatus': 'A'
        }
        if validar_tipos(nuevo_tipo):
            tipos.replace_one({'id': id, 'estatus': 'A'}, nuevo_tipo)
            return redirect(url_for('listar_tipos'))
    return render_template('/tipos/actualizar/index.html', viejo_tipo=viejo_tipo)

@app.route('/<id>/eliminar_tipo', methods=['GET', 'POST'])
def eliminar_tipo(id):
    viejo_tipo = tipos.find_one({'id': id, 'estatus': 'A'})

    if not viejo_tipo:
        flash('Tipo no encontrado')
        return redirect(url_for('listar_tipos'))
    
    tipo_eliminado = {
        'id': viejo_tipo['id'], 
        'nombre': viejo_tipo['nombre'], 
        'descripcion': viejo_tipo['descripcion'], 
        'estatus': 'I'
    }
    
    if request.method == 'POST':
        tipos.replace_one({'id': id, 'estatus': 'A'}, tipo_eliminado)
        flash('Tipo eliminado con éxito')
        return redirect(url_for('listar_tipos'))
    return render_template('/tipos/eliminar/index.html', viejo_tipo=viejo_tipo)

@app.route('/reportes', methods=['GET'])
def reportes():
    
    return render_template('/reportes/index.html')

@app.route('/registrar_sesion', methods=['GET', 'POST'])
def registrar_sesion():
    if request.method == 'POST':
        forma = request.form

    return render_template('/usuarios/registrar_sesion/index.html')

@app.route('/inciar_sesion', methods=['GET', 'POST'])
def iniciar_sesion():
    if request.method == 'POST':
        forma = request.form

    return render_template('/usuarios/iniciar_sesion/index.html')

if __name__ == '__main__':
    app.run(debug=True)