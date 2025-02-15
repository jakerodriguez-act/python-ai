from flask import Flask, request, jsonify
from pymilvus import connections, Collection
from sentence_transformers import SentenceTransformer

# Initialize Flask app
app = Flask(__name__)

# Milvus settings
MILVUS_HOST = "localhost"
MILVUS_PORT = "19530"
COLLECTION_NAME = "knowledge_base"

# Initialize Milvus connection
def connect_to_milvus():
    connections.connect("default", host=MILVUS_HOST, port=MILVUS_PORT)
    print("Connected to Milvus")

# Load the embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Milvus query function
def query_milvus(query_text, top_k=5):
    # Connect to the Milvus collection
    collection = Collection(COLLECTION_NAME)
    collection.load()

    # Generate embedding for the query
    query_embedding = embedding_model.encode(query_text).tolist()

    # Perform similarity search
    search_params = {"metric_type": "IP", "params": {"nprobe": 10}}
    results = collection.search(
        data=[query_embedding],
        anns_field="embedding",
        param=search_params,
        limit=top_k,
        expr=None,  # You can add filters here if needed
    )

    # Extract results
    matches = []
    for result in results[0]:
        matches.append({
            "id": result.id,
            "score": result.score,
            "content": result.entity.get("content"),
        })
    return matches

# Flask route to handle AI Agent queries
@app.route("/milvus-query", methods=["POST"])
def milvus_query():
    try:
        # Extract input from the request
        data = request.json
        query_text = data.get("query", "")
        top_k = data.get("top_k", 5)

        if not query_text:
            return jsonify({"error": "Query text is required"}), 400

        # Query Milvus
        matches = query_milvus(query_text, top_k)
        return jsonify({"matches": matches})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Start Flask app
if __name__ == "__main__":
    connect_to_milvus()
    app.run(host="0.0.0.0", port=5000)
