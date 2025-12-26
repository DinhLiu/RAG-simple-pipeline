from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from qdrant_client.http import models


COLLECTION_NAME = "devto_articles"
QDRANT_URL = "http://localhost:6333"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"


def search_knowledge_base():
    print(f"Loading embedding model {EMBEDDING_MODEL}")
    model = SentenceTransformer(EMBEDDING_MODEL)

    print(f'Connecting to Qdrant at {QDRANT_URL}...')
    client = QdrantClient(url=QDRANT_URL)

    print("RAG system ready!")
    print("Type 'exit' to exit\n")

    while True:
        query = input("\n\nInput your question:\n")
        if query.lower() in ['exit', 'quit']:
            break
            
        query_vector = model.encode(query).tolist()

        hits = client.query_points(
            collection_name=COLLECTION_NAME,
            query=query_vector,
            limit=3, # Get 3 most relevant result,
            with_payload=True
        ).points

        for i, hit in enumerate(hits):
            
            score = hit.score
            payload = hit.payload

            print('-'*20)
            print(f'Result {i + 1}  | Score: {score:.4f}')
            print(f"Source: {payload['title']}")
            print(f"URL: {payload['url']}")
            print(f"Content: {payload['text'][:300]}...")
            print('-'*20)

if __name__ == '__main__':
    search_knowledge_base()