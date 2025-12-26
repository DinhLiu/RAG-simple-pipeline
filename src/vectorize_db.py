import json
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer
import uuid

INPUT_FILE = '../processed_data/processed_chunks.json'
COLLECTION_NAME = "devto_articles"
QDRANT_URL = "http://localhost:6333"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
def load_to_qdrant():

    # Initialyze Model and Client
    print(f"Loading embedding model {EMBEDDING_MODEL}...")
    encoder = SentenceTransformer(EMBEDDING_MODEL)

    print(f"Connecting to Qdrant at {QDRANT_URL}")
    client = QdrantClient(url=QDRANT_URL)

    # Create Collection
    if not client.collection_exists(COLLECTION_NAME):
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE)
        )
        print(f"Collection {COLLECTION_NAME} created sucessfully")
    else:
        print(f"Collection {COLLECTION_NAME} has already been exist")

    try:
        with open(INPUT_FILE, 'r', encoding='utf-8') as file:
            chunks = json.load(file)
    except FileNotFoundError:
        print(f'Cannot find file {INPUT_FILE}')
        return
    
    print(f"Start addin {len(chunks)} chunks into database...")

    points = []

    for idx, chunk in enumerate(chunks):
        text = chunk['text']
        metadata = chunk['metadata']
        article_id = chunk['article_id']

        # EMbedding: convert text into vectors
        vector = encoder.encode(text).tolist()

        # Pack into point (data point)
        point_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{article_id}_{idx}"))

        # Payload
        payload = metadata
        payload['text'] = text
        payload['article_id'] = article_id

        points.append(PointStruct(id=point_id, vector=vector, payload=payload))

    if points:
        client.upsert(collection_name=COLLECTION_NAME, points=points)
        print(f'Uploaded {len(chunks)}/{len(chunks)} chunks')

    print(f"Vectorize done")

if __name__ == "__main__":
    load_to_qdrant()