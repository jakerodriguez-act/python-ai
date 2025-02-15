import os
import logging
import json
from pymilvus import (
    connections,
    FieldSchema,
    CollectionSchema,
    DataType,
    Collection,
    utility
)
from sentence_transformers import SentenceTransformer
from charset_normalizer import detect

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Milvus connection settings
MILVUS_HOST = "localhost"
MILVUS_PORT = "19530"
COLLECTION_NAME = "knowledge_base"

# Connect to Milvus
def connect_to_milvus():
    connections.connect("default", host=MILVUS_HOST, port=MILVUS_PORT)
    print("Connected to Milvus")

# Create Milvus collection
def create_collection():
    fields = [
        FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
        FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=384),  # Adjust the dim for your embedding model
        FieldSchema(name="content", dtype=DataType.VARCHAR, max_length=65535),
    ]
    schema = CollectionSchema(fields, description="Knowledge Base Collection")
    collection = Collection(name=COLLECTION_NAME, schema=schema)
    print(f"Collection {COLLECTION_NAME} created")
    return collection

# Insert embeddings and content into Milvus
def insert_to_milvus(collection, embeddings, content_list):
    entities = {
        "embedding": embeddings,
        "content": content_list,
    }
    collection.insert(entities)
    print("Data inserted into Milvus")

# Main function
def main():
    # Connect to Milvus
    connect_to_milvus()

    # Create collection (if it doesn't exist)
    if not utility.has_collection(COLLECTION_NAME):
        collection = create_collection()
    else:
        collection = Collection(COLLECTION_NAME)

    # Insert data into Milvus
    # insert_to_milvus(collection, embeddings, content_list)

if __name__ == "__main__":
    main()