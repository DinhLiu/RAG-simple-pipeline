"""
Main controller script for the RAG pipeline.
Orchestrates data fetching, processing, and vectorization.
"""
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.raw_data import fetch_data
from src.process_data import process_chunks
from src.vectorize_db import load_to_qdrant


def run_pipeline(tag="ai", limit=20, skip_fetch=False, skip_process=False, skip_vectorize=False):
    """
    Run the complete RAG pipeline.
    
    Args:
        tag: Tag to fetch articles from dev.to
        limit: Maximum number of articles to fetch
        skip_fetch: Skip data fetching step
        skip_process: Skip data processing step
        skip_vectorize: Skip vectorization step
    """
    print("=" * 60)
    print("Starting RAG Pipeline")
    print("=" * 60)
    
    try:
        # Step 1: Fetch raw data
        if not skip_fetch:
            print("\n[Step 1/3] Fetching raw data from dev.to...")
            fetch_data(tag=tag, limit=limit)
        else:
            print("\n[Step 1/3] Skipping data fetch...")
        
        # Step 2: Process and chunk data
        if not skip_process:
            print("\n[Step 2/3] Processing and chunking data...")
            process_chunks()
        else:
            print("\n[Step 2/3] Skipping data processing...")
        
        # Step 3: Vectorize and load to Qdrant
        if not skip_vectorize:
            print("\n[Step 3/3] Vectorizing and loading to Qdrant...")
            load_to_qdrant()
        else:
            print("\n[Step 3/3] Skipping vectorization...")
        
        print("\n" + "=" * 60)
        print("Pipeline completed successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\nPipeline failed with error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # Run complete pipeline
    run_pipeline(tag="programming", limit=400)
    
    # Or run only specific steps:
    # run_pipeline(tag="python", limit=10, skip_fetch=True)  # Skip fetch, reprocess existing data
    # run_pipeline(skip_fetch=True, skip_process=True)  # Only vectorize existing processed data
