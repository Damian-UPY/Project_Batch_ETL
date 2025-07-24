from pymongo import MongoClient
import os

def get_mongo_client():
    """Crea y devuelve un cliente de MongoDB usando MONGO_URI."""
    mongo_uri = os.getenv('MONGO_URI', 'mongodb://root:example@mongodb:27017/project_db?authSource=admin')
    return MongoClient(mongo_uri)

def insert_data(data, collection_name):
    """Inserta uno o varios documentos en la colección especificada."""
    client = get_mongo_client()
    db = client.get_database()  # Usa el DB definido en la URI
    collection = db[collection_name]

    if isinstance(data, list):
        collection.insert_many(data)
        print(f"✅ Inserted {len(data)} documents into '{collection_name}'")
    else:
        collection.insert_one(data)
        print(f"✅ Inserted 1 document into '{collection_name}'")

def find_data(collection_name, query=None):
    """Busca documentos en la colección (query opcional)."""
    client = get_mongo_client()
    db = client.get_database()
    collection = db[collection_name]
    return list(collection.find(query or {}))

def delete_data(collection_name, query=None):
    """Elimina documentos según la query (o todos si no se especifica)."""
    client = get_mongo_client()
    db = client.get_database()
    collection = db[collection_name]
    result = collection.delete_many(query or {})
    print(f"✅ Deleted {result.deleted_count} documents from '{collection_name}'")
