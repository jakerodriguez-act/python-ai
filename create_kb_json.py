import os
import logging
import json
from sentence_transformers import SentenceTransformer
from charset_normalizer import detect

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


output_directory = "knowledge_base_documents"

# Process Markdown files and insert into Milvus
def process_markdown_files(markdown_dir):
    model = SentenceTransformer("all-MiniLM-L6-v2")  # Choose an appropriate embedding model

    vector_list = []
    destination_file = 'kb.json'
    destination_path = os.path.join(markdown_dir, destination_file)
    for filename in os.listdir(markdown_dir):
        if filename.endswith(".md"):
            file_path = os.path.join(markdown_dir, filename)
            with open(file_path, "rb") as file:  # Open in binary mode to detect encoding
                raw_data = file.read()
                encoding = detect(raw_data)['encoding']  # Detect the encoding

            with open(file_path, "r", encoding=encoding) as file:
                content = file.read()
                embedding = model.encode(content).tolist()  # Convert numpy array to list for Milvus

        entry = {"embedding": embedding, "content": content}
        vector_list.append(entry)

    with open(destination_path, 'w') as json_file:
        json.dump(vector_list, json_file, indent=2)

    return

# Main function
def main():

    process_markdown_files(output_directory)

if __name__ == "__main__":
    main()