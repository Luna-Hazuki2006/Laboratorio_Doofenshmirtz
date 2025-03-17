import pymongo
import os

cliente = pymongo.MongoClient(os.environ.get('URL'))

db = cliente.laboratorio_doofenshmirtz

examenes = db.examenes
categorias = db.categorias
indicaciones = db.indicaciones
tipos = db.tipos
usuarios = db.usuarios