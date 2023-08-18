from flask import Flask, render_template, request, redirect, url_for, flash
from pprint import pprint
from validaciones import *
from db import examenes, categorias, indicaciones, tipos, usuarios
# ) xbox fruit 2 PARK LAPTOP walmart 8 . _ golf USA korean JACK ? ~ 
app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = ')xf2PLw8._gUkJ?~'
Usuario_actual = None

@app.route('/', methods=['GET', 'POST'])
def listar_examenes():
    servicios = examenes.find({'estatus': 'A'})
    divisiones = categorias.find({'estatus': 'A'})
    caracteristicas = tipos.find({'estatus': 'A'})
    if request.method == 'POST': 
        forma = request.form
        tipo = forma['tipo']
        categoria = forma['categoria']
        servicios = filtrar_examenes(categoria, tipo)
        return render_template('/examenes/listar/index.html', 
                                servicios=servicios, 
                                divisiones=divisiones, 
                                caracteristicas=caracteristicas, 
                                UA=Usuario_actual)
    return render_template('/examenes/listar/index.html', 
                           servicios=servicios, 
                           divisiones=divisiones, 
                           caracteristicas=caracteristicas, 
                           UA=Usuario_actual)

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
        lista = []
        for item in request.form.getlist('check'):
            lista.append(indicaciones.find_one({'id': item, 'estatus': 'A'}))
        nuevo_examen = {
            'id': 'E' + str(numero), 
            'nombre': str(forma['nombre']), 
            'categoria': categorias.find_one({'id': forma['categoria'], 'estatus': 'A'}), 
            'tipo': tipos.find_one({'id': forma['tipo'], 'estatus': 'A'}), 
            'precio': forma['precio'], 
            'indicaciones': lista, 
            'estatus': 'A'
        }
        if validar_crear_examen(nuevo_examen):
            nuevo_examen['precio'] = int(forma['precio'])
            id = examenes.insert_one(nuevo_examen).inserted_id
            if id:
                flash('Examen creado con éxito')
                return redirect(url_for('listar_examenes'))
            else: 
                flash('Ocurrió un error guardando')
        else: flash('El examen no pasó las validaciones')
    return render_template('/examenes/agregar/index.html', 
                           divisiones=divisiones, 
                           caracteristicas=caracteristicas, 
                           descripciones=descripciones, 
                           UA=Usuario_actual)

@app.route('/<id>/consultar_examen', methods=['GET'])
def consultar_examen(id):
    examen = examenes.find_one({'id': id, 'estatus': 'A'})
    print(examen)
    return render_template('/examenes/consultar/index.html', 
                           examen=examen, 
                           UA=Usuario_actual)

@app.route('/<id>/actualizar_examen', methods=['GET', 'POST'])
def actualizar_examen(id):
    viejo_examen = examenes.find_one({'id': id, 'estatus': 'A'})
    divisiones = categorias.find({'estatus': 'A'})
    caracteristicas = tipos.find({'estatus': 'A'})
    descripciones = indicaciones.find({'estatus': 'A'})
    listas = []

    if not viejo_examen:
        flash('Examen no encontrado')
        return redirect(url_for('listar_examenes'))
    for datos in indicaciones.find({'estatus': 'A'}):
            realidad = {
                'id': '', 
                'nombre': '', 
                'verdad': True
            }
            print('datos')
            pprint(datos)
            verdad = False
            for estos in viejo_examen['indicaciones']:
                print()
                pprint(estos)
                if estos['id'] == datos['id']:
                    verdad = True
            realidad['id'] = datos['id']
            realidad['nombre'] = datos['nombre']
            realidad['verdad'] = verdad
            listas.append(realidad)
    
    if request.method == 'POST':
        forma = request.form
        lista = []
        for item in request.form.getlist('indicacion'):
            lista.append(indicaciones.find_one({'id': item, 'estatus': 'A'}))
        nuevo_examen = {
            'id': viejo_examen['id'], 
            'nombre': forma['nombre'], 
            'categoria': categorias.find_one({'id': forma['categoria'], 'estatus': 'A'}), 
            'tipo': tipos.find_one({'id': forma['tipo'], 'estatus': 'A'}), 
            'precio': forma['precio'], 
            'indicaciones': lista , 
            'estatus': 'A'
        }
        pprint(nuevo_examen)
        if validar_editar_examen(nuevo_examen):
            nuevo_examen['precio'] = int(forma['precio'])
            examenes.replace_one({'id': id}, nuevo_examen)
            return redirect(url_for('listar_examenes'))
        else: flash('No pasó las validaciones')
    return render_template('/examenes/actualizar/index.html', 
                           viejo_examen=viejo_examen, 
                           divisiones=divisiones, 
                           caracteristicas=caracteristicas, 
                           listas=listas, 
                           UA=Usuario_actual)

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
    return render_template('/examenes/eliminar/index.html', 
                           viejo_examen=viejo_examen, 
                           UA=Usuario_actual)

@app.route('/listar_indicaciones', methods=['GET'])
def listar_indicaciones():
    indicados = indicaciones.find({'estatus': 'A'})
    return render_template('/indicaciones/listar/index.html', 
                           indicados=indicados, 
                           UA=Usuario_actual)

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
        if validar_crear_indicacion(nueva_indicacion):
            id = indicaciones.insert_one(nueva_indicacion).inserted_id
            if id:
                flash('Indicación creada con éxito')
                return redirect(url_for('listar_indicaciones'))
            else: 
                flash('Ocurrió un error guardando')
        else: flash('Se ingresó un nombre repetido')
    return render_template('/indicaciones/agregar/index.html', 
                           UA=Usuario_actual)

@app.route('/<id>/consultar_indicacion', methods=['GET'])
def consultar_indicacion(id):
    indicacion = indicaciones.find_one({'id': id, 'estatus': 'A'})
    return render_template('/indicaciones/consultar/index.html', 
                           indicacion=indicacion, 
                           UA=Usuario_actual)

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
        if validar_editar_indicacion(nueva_indicacion):
            indicaciones.replace_one({'id': id}, nueva_indicacion)
            return redirect(url_for('listar_indicaciones'))
    return render_template('/indicaciones/actualizar/index.html', 
                           vieja_indicacion=vieja_indicacion, 
                           UA=Usuario_actual)

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
        if validar_eliminar_indicacion(indicacion_eliminada):
            indicaciones.replace_one({'id': id, 'estatus': 'A'}, indicacion_eliminada)
            flash('Indicación eliminada con éxito')
            return redirect(url_for('listar_indicaciones'))
        else: flash('No se puede eliminar indicaciones que están en uso')
    return render_template('/indicaciones/eliminar/index.html', 
                           vieja_indicacion=vieja_indicacion, 
                           UA=Usuario_actual)

@app.route('/listar_categorias', methods=['GET'])
def listar_categorias():
    divisiones = categorias.find({'estatus': 'A'})
    return render_template('/categorias/listar/index.html', 
                           divisiones=divisiones, 
                           UA=Usuario_actual)

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
        if validar_crear_categoria(nueva_categoria):
            id = categorias.insert_one(nueva_categoria).inserted_id
            if id:
                flash('Categoría creada con éxito')
                return redirect(url_for('listar_categorias'))
            else: 
                flash('Ocurrió un error guardando')
        else: flash('Se ingresó un nombre repetido')
    return render_template('/categorias/agregar/index.html', 
                           UA=Usuario_actual)

@app.route('/<id>/consultar_categoria', methods=['GET'])
def consultar_categoria(id):
    categoria = categorias.find_one({'id': id, 'estatus': 'A'})
    return render_template('/categorias/consultar/index.html', 
                           categoria=categoria, 
                           UA=Usuario_actual)

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
        if validar_editar_categoria(nueva_categoria):
            categorias.replace_one({'id': id, 'estatus': 'A'}, nueva_categoria)
            return redirect(url_for('listar_categorias'))
    return render_template('/categorias/actualizar/index.html', 
                           vieja_categoria=vieja_categoria, 
                           UA=Usuario_actual)

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
        if validar_eliminar_categoria(categoria_eliminada):
            categorias.replace_one({'id': id, 'estatus': 'A'}, categoria_eliminada)
            flash('Categoría eliminada con éxito')
            return redirect(url_for('listar_categorias'))
        else: flash('No se puede eliminar categorías que están en uso')
    return render_template('/categorias/eliminar/index.html', 
                           vieja_categoria=vieja_categoria, 
                           UA=Usuario_actual)

@app.route('/listar_tipos', methods=['GET'])
def listar_tipos():
    diferencias = tipos.find({'estatus': 'A'})
    return render_template('/tipos/listar/index.html', 
                           diferencias=diferencias, 
                           UA=Usuario_actual)

@app.route('/crear_tipos', methods=['GET', 'POST'])
def crear_tipo():
    if request.method == 'POST':
        numero = tipos.count_documents({}) + 1
        forma = request.form
        nuevo_tipo = {
            'id': 'T' + str(numero), 
            'nombre': forma['nombre'], 
            'descripcion': forma['descripcion'], 
            'estatus': 'A'
        }
        if validar_crear_tipos(nuevo_tipo):
            id = tipos.insert_one(nuevo_tipo).inserted_id
            if id:
                flash('Tipo creado con éxito')
                return redirect(url_for('listar_tipos'))
            else: 
                flash('Ocurrió un error guardando')
        else: flash('Se ingresó un nombre repetido')
    return render_template('/tipos/agregar/index.html', 
                           UA=Usuario_actual)

@app.route('/<id>/consultar_tipos', methods=['GET'])
def consultar_tipo(id):
    tipo = tipos.find_one({'id': id, 'estatus': 'A'})
    return render_template('/tipos/consultar/index.html', 
                           tipo=tipo, 
                           UA=Usuario_actual)

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
        if validar_editar_tipos(nuevo_tipo):
            tipos.replace_one({'id': id, 'estatus': 'A'}, nuevo_tipo)
            return redirect(url_for('listar_tipos'))
    return render_template('/tipos/actualizar/index.html', 
                           viejo_tipo=viejo_tipo, 
                           UA=Usuario_actual)

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
        if validar_eliminar_tipos(tipo_eliminado):
            tipos.replace_one({'id': id, 'estatus': 'A'}, tipo_eliminado)
            flash('Tipo eliminado con éxito')
            return redirect(url_for('listar_tipos'))
        else: flash('No se pueden eliminar tipos que están en uso')
    return render_template('/tipos/eliminar/index.html', 
                           viejo_tipo=viejo_tipo, 
                           UA=Usuario_actual)

@app.route('/reportes', methods=['GET'])
def reportes():
    servicios = examenes.find({'estatus': 'A'})
    divisiones = categorias.find({'estatus': 'A'})
    especificaciones = indicaciones.find({'estatus': 'A'})
    apreciado = {
        '1 - 100': [], 
        '101 - 200': [], 
        '201 - 300': [], 
        '301 - 500': [], 
        '501 +': []
    }
    categorizado = []
    indicados = []
    for servicio in servicios:
        if int(servicio['precio']) >= 1 and int(servicio['precio']) <= 100:
            apreciado['1 - 100'].append(servicio)
        elif int(servicio['precio']) >= 101 and int(servicio['precio']) <= 200:
            apreciado['101 - 200'].append(servicio)
        elif int(servicio['precio']) >= 201 and int(servicio['precio']) <= 300: 
            apreciado['201 - 300'].append(servicio)
        elif int(servicio['precio']) >= 301 and int(servicio['precio']) <= 500: 
            apreciado['301 - 500'].append(servicio)
        elif int(servicio['precio']) >= 501: 
            apreciado['501 +'].append(servicio)
    for categoria in divisiones:
        lista = []
        dato = {}
        for servicio in examenes.find({'estatus': 'A'}):
            if servicio['categoria']['nombre'] == categoria['nombre']: 
                lista.append(servicio['id'])
        dato['nombre'] = categoria['nombre']
        dato['lista'] = lista
        categorizado.append(dato)
    for indicacion in especificaciones:
        lista = []
        dato = {}
        for servicio in examenes.find({'estatus': 'A'}):
            for caso in servicio['indicaciones']:
                if caso['nombre'] == indicacion['nombre']:
                    lista.append(servicio['id'])
        dato['nombre'] = indicacion['nombre']
        dato['lista'] = lista
        indicados.append(dato)
    pprint(indicados)
            
    return render_template('/reportes/index.html', 
                           apreciado=apreciado, 
                           categorizado=categorizado, 
                           indicados=indicados, 
                           UA=Usuario_actual)

@app.route('/registrar_usuario', methods=['GET', 'POST'])
def registrar_usuario():
    if request.method == 'POST':
        forma = request.form
        nombre = forma['usuario']
        clave = forma['contraseña']
        repetida = forma['repetida']
        if clave == repetida:
            numero = usuarios.count_documents({}) + 1
            usuario = {
                'id': 'U' + str(numero), 
                'nombre': nombre, 
                'clave': clave, 
                'estatus': 'A'
            }
            if validar_registrar(usuario):
                id = usuarios.insert_one(usuario).inserted_id
                if id:
                    flash('Usuario registrado con éxito')
                else: 
                    flash('Ocurrió un error guardando')
            else: flash('Se ingresó un nombre de usuario repetido')
        else: flash('La contraseña no es igual')

    return render_template('/usuarios/registrar_usuario/index.html', 
                           UA=Usuario_actual)

@app.route('/inciar_sesion', methods=['GET', 'POST'])
def iniciar_sesion():
    Usuario_actual = None
    if request.method == 'POST':
        forma = request.form
        nombre = forma['usuario']
        clave = forma['contraseña']
        usuario = {
            'nombre': nombre, 
            'clave': clave
        }
        if validar_iniciar(usuario):
            Usuario_actual = usuarios.find_one({'nombre': usuario['nombre'], 'estatus': 'A'})
            return render_template('/base/index.html', UA=Usuario_actual)
        else: flash('Se ha equivocado en uno de los campos')

    return render_template('/usuarios/iniciar_sesion/index.html', 
                           UA=Usuario_actual)

if __name__ == '__main__':
    app.run(debug=True)