from pymongo import MongoClient
import os

# Obtener URI desde variable de entorno o usar valor por defecto seguro
mongo_uri = os.getenv('MONGO_URI', 'mongodb://root:example@mongodb:27017/project_db?authSource=admin')

# Conectar a MongoDB
client = MongoClient(mongo_uri)
db = client.get_database()  # Usa la base de datos definida en la URI
collection = db[os.getenv('MONGO_COLLECTION', 'cats_dataset')]

def get_latest_dataset():
    """Obtiene todos los documentos sin mostrar _id."""
    data = list(collection.find({}, {'_id': 0}))
    return data
