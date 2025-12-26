from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
import google.genai as genai
from qdrant_client.http import models
from dotenv import load_dotenv, dotenv_values
import os


load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

COLLECTION_NAME = "devto_articles"
QDRANT_URL = "http://localhost:6333"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

gemini_client = genai.Client(api_key=GEMINI_API_KEY)

def search_knowledge_base():
    print(f"Loading embedding model {EMBEDDING_MODEL}")
    model = SentenceTransformer(EMBEDDING_MODEL)

    print(f'Connecting to Qdrant at {QDRANT_URL}...')
    client = QdrantClient(url=QDRANT_URL)

    print("RAG system ready!")
    print("Type 'exit' to exit\n")

    while True:
        query = input("\n\nInput your question):\n")
        if query.lower() in ['exit', 'quit']:
            break
            
        query_vector = model.encode(query).tolist()

        hits = client.query_points(
            collection_name=COLLECTION_NAME,
            query=query_vector,
            limit=3, # Get 3 most relevant result,
            with_payload=True
        ).points

        print(f"{len(hits)} info founded")

        context_text = ""

        for i, hit in enumerate(hits):
            score = hit.score
            payload = hit.payload

            title = payload.get('title', 'N/A')
            text = payload.get('text', '')
            context_text += f"\n---\nSource: {title}\nContent: {text}\n"

            # print('-'*20)
            # print(f'Result {i + 1}  | Score: {score:.4f}')
            # print(f"Source: {payload['title']}")
            # print(f"URL: {payload['url']}")
            # print(f"Content: {payload['text'][:500]}...")
            # print('-'*20)
            
        print("Thinking...")

        prompt = f"""
        You are a helpful and knowledgeable software engineering assistant.
        Your task is to answer the user's question using ONLY the provided context below.
        
        Instructions:
        1. Answer strictly based on the provided context.
        2. If the context does not contain the answer, explicitly state: "I cannot find the answer in the provided documents."
        3. Do not make up information or use outside knowledge unless necessary to explain the context.
        4. Answer in the same language as the user's question.

        ### Context:
        {context_text}

        ### User Question:
        {query}

        ### Answer:
        """

        try:
            response = gemini_client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            print(f"\nAssistance: {response.text}")
            print('-'*30)
        except Exception as e:
            print(f"Error calling Gemini APi: {e}")


if __name__ == '__main__':
    search_knowledge_base()