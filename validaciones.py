from db import examenes, categorias, indicaciones, tipos, usuarios

def validar_crear_examen(examen):
    verdad = True
    for esto in examenes.find({'estatus': 'A'}):
        if (examen['id'] == esto['id'] or 
            examen['nombre'] == esto['nombre']):
            verdad = False
            break
    if not isinstance(examen['precio'], int, float):
        verdad = False
    
    return verdad

def validar_editar_examen(examen):
    verdad = True
    for esto in examenes.find({'estatus': 'A'}):
        if (examen['id'] != esto['id'] and 
            examen['nombre'] == esto['nombre']):
            verdad = False
            break
    if not isinstance(examen['precio'], int, float):
        verdad = False
    return verdad

def validar_crear_categoria(categoria):
    verdad = True
    for esto in categorias.find({'estatus': 'A'}):
        if (categoria['id'] == esto['id'] or 
            categoria['nombre'] == esto['nombre']):
            verdad = False
            break
    return verdad

def validar_editar_categoria(categoria):
    verdad = True
    for esto in categorias.find({'estatus': 'A'}):
        if (categoria['id'] != esto['id'] and 
            categoria['nombre'] == esto['nombre']):
            verdad = False
            break
    return verdad

def validar_eliminar_categoria(categoria):
    verdad = True
    for esto in examenes.find({'estatus': 'A'}):
        if esto['categoria']['id'] == categoria['id']:
            verdad = False
            break
    return verdad

def validar_crear_indicacion(indicacion):
    verdad = True
    for esto in indicaciones.find({'estatus': 'A'}): 
        if (indicacion['id'] == esto['id'] or 
            indicacion['nombre'] == esto['nombre']):
            verdad = False
            break
    return verdad

def validar_editar_indicacion(indicacion):
    verdad = True
    for esto in indicaciones.find({'estatus': 'A'}): 
        if (indicacion['id'] != esto['id'] and 
            indicacion['nombre'] == esto['nombre']):
            verdad = False
            break
    return verdad

def validar_eliminar_indicacion(indicacion): 
    verdad = True
    for esto in examenes.find({'estatus': 'A'}):
        for cosa in esto['indicaciones']:
            if cosa['id'] == indicacion['id']:
                verdad = False
                break
    return verdad

def validar_crear_tipos(tipo):
    verdad = True
    for esto in tipos.find({'estatus': 'A'}): 
        if (tipo['id'] == esto['id'] or 
            tipo['nombre'] == esto['nombre']):
            verdad = False
            break
    return verdad

def validar_editar_tipos(tipo):
    verdad = True
    for esto in tipos.find({'estatus': 'A'}): 
        if (tipo['id'] != esto['id'] and  
            tipo['nombre'] == esto['nombre']):
            verdad = False
            break
    return verdad

def validar_eliminar_tipos(tipo): 
    verdad = True
    for esto in examenes.find({'estatus': 'A'}):
        if esto['tipo']['id'] == tipo['id']:
            verdad = False
            break
    return verdad

def validar_registrar(usuario): 
    verdad = True
    for esto in usuarios.find({'estatus': 'A'}): 
        if usuario['nombre'] == esto['nombre']:
            verdad = False
            break
    return verdad

def validar_iniciar(usuario): 
    verdad = False
    for esto in usuarios.find({'estatus': 'A'}): 
        if (usuario['nombre'] == esto['nombre'] and 
            usuario['clave'] == esto['clave']):
            verdad = True
            break
    return verdad