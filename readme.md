# 🤖 RAG Simple Pipeline

> A complete Retrieval-Augmented Generation (RAG) system built from scratch using **Qdrant**, **Google Gemini**, and data crawled from **Dev.to**.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Qdrant](https://img.shields.io/badge/Vector%20DB-Qdrant-red)](https://qdrant.tech/)
[![Google Gemini](https://img.shields.io/badge/AI-Google%20Gemini-green)](https://ai.google.dev/)

## 📖 Overview

This project demonstrates how to build an end-to-end RAG pipeline. It automatically collects technical articles from [Dev.to](https://dev.to), processes the text, stores it in a Vector Database (Qdrant), and uses a Large Language Model (Google Gemini 1.5 Flash) to answer user questions based on the collected knowledge.

### ✨ Key Features

* **🕷️ Automated Crawler:** Fetches articles and tags directly from Dev.to.
* **🧹 Data Processing:** Cleans and chunks raw text for optimal embedding.
* **🧠 Vector Embeddings:** Uses `sentence-transformers/all-MiniLM-L6-v2` for efficient semantic search.
* **💾 Qdrant Integration:** Runs a local Qdrant instance via Docker for vector storage.
* **🤖 AI Assistant:** Integrates the new **Google GenAI SDK** to generate human-like answers using Gemini.
* **🔄 Idempotency:** Prevents duplicate data ingestion using UUID generation.

---

## 🛠️ Prerequisites

Before you begin, ensure you have the following installed:

* **Python 3.8+**
* **Docker Desktop** (Required to run Qdrant)
* **Google Gemini API Key** (Get it for free at [Google AI Studio](https://aistudio.google.com/))

---

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone [https://github.com/DinhLiu/RAG-simple-pipeline.git](https://github.com/DinhLiu/RAG-simple-pipeline.git)
cd RAG-simple-pipeline
```
### 2. Setup environment and Install dependencies
```bash
python -m venv venv
venv/Scripts/Activate #Window
pip install -r requirements.txt
```
### 3. Create your `.env` file and add your Goodle Gemini API Key
```bash
GEMINI_API_KEY=YOUR_KEY
```
### 4. Run `tag_crawler.py` to get list of available tag in `tag_list.txt`
```
python -m tag_crawler
```
### 5. Start your Qdrant Database
Use Docker Compose to start the local vector database.
```
docker compose up -d
```
You can verify it's running by visiting: http://localhost:6333/dashboard

## 🏃‍♂️ Usage Guide
### 1. Get tag list
You can get a file of available tag list by running `tag_crawler.py`
```
python -m tag_crawler
```
### 2. Choose your own domain's tag and set limit in `data_controller.py`
```
run_pipeline(tag="programming", limit=400)
```
Or you can create a looo through all available tags to get variety articles' domain
### 3. Run the search engine
If you have `GEMINI_API_KEY`, you can use it to run `gemini_se.py`, which use **gemini-2.5-flash** to answer your question base on the data saved in **Qdrant**
```
python -m gemini_se
```
or else, you can run the basic search engine
```
python -m basic_se
```

## 📂 Project Structure
```
RAG-simple-pipeline/
│
├── processed_data/      # Contains cleaned and chunked data (JSON)
├── qdrant_storage/      # Persistent storage for Qdrant (Managed by Docker)
├── raw_data/            # Contains raw articles fetched from Dev.to
│
├── src/                 # Core logic modules
│   ├── process_data.py  # Logic for cleaning and chunking text
│   ├── raw_data.py      # Crawler script to fetch articles (formerly crawler.py)
│   └── vectorize_db.py  # Logic for embedding and uploading to Qdrant
│
├── basic_se.py          # Basic Search Engine
├── data_controller.py   # Helper script for data management
├── docker-compose.yaml  # Docker configuration for Qdrant service
├── gemini_se.py         # Main AI Search Engine (RAG with Gemini)
├── tag_crawler.py       # Script to fetch tags from Dev.to
├── tag_list.txt         # List of tags to crawl
│
├── .env                 # Environment variables (API Keys - Keep secret!)
├── .gitignore           # Git ignore rules
├── LICENSE              # License file
├── readme.md            # Project documentation
└── requirements.txt     # Python dependencies
```
