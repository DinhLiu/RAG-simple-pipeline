import json
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter

INPUT_FILE = "../raw_data/raw_data.json"
OUTPUT_FOLDER = '../processed_data'
OUTPUT_FILE = f'{OUTPUT_FOLDER}/processed_chunks.json'
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def process_chunks():
    if not os.path.exists(INPUT_FILE):
        print(f"Cannot open {INPUT_FILE} to process chunks")
        return

    with open(INPUT_FILE, 'r', encoding='utf-8') as file:
        articles = json.load(file)

    print(f"Processing {len(articles)} articles...")

    # Analyze spliter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1000,
        chunk_overlap = 200,
        separators=["\n\n", "\n", " ", ""]
    )

    all_chunks = []

    for article in articles:
        markdown_content = article.get('content', {}).get('markdown', '')

        if not markdown_content:
            continue
        
        chunks = text_splitter.create_documents([markdown_content])

        for chunk in chunks:
            chunk_record = {
                "text": chunk.page_content,
                "metadata": article['metadata'],
                "article_id": article['id']
            }

            chunk_record['metadata']['chunk_len'] = len(chunk.page_content)

            all_chunks.append(chunk_record)

        with open(OUTPUT_FILE, 'w', encoding='utf-8') as file:
            json.dump(all_chunks, file, ensure_ascii=False, indent=2)

    print('Chunking raw data done')
    print(f'From {len(articles)} articles created {len(all_chunks)} chunks')

if __name__ == "__main__":
    process_chunks()