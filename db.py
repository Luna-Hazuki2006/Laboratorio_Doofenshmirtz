import pymongo

cliente = pymongo.MongoClient('mongodb+srv://lunahazuki2006:cXU0lYhSncWZ12FM@cluster0.owjghpf.mongodb.net/')

db = cliente.laboratorio_doofenshmirtz

examenes = db.examenes
categorias = db.categorias
indicaciones = db.indicaciones