import pdfplumber
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
import logging
from transformers import pipeline
import os
import warnings

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  


logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')


logging.getLogger("transformers").setLevel(logging.ERROR)
logging.getLogger("sentence_transformers").setLevel(logging.ERROR)


embedding_model = SentenceTransformer('all-MiniLM-L6-v2')


llm = pipeline("text-generation", model="gpt2")

def extract_all_pages(pdf_path):
    """Extracts text from all pages in the PDF."""
    extracted_data = {}
    with pdfplumber.open(pdf_path) as pdf:
        for page_number in range(len(pdf.pages)):
            page = pdf.pages[page_number]
            extracted_data[page_number + 1] = page.extract_text()
    return extracted_data

def chunk_text(text, chunk_size=200):
    """Chunks the extracted text into smaller pieces."""
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

def create_embeddings(chunks):
    """Creates embeddings for the text chunks."""
    return embedding_model.encode(chunks)

def main():
   
    pdf_files = [
        r"C:\Users\Administrator.L2133\Desktop\tables.pdf" 
    ]


    all_chunks = []
    all_embeddings = []

    for pdf_path in pdf_files:
        extracted_data = extract_all_pages(pdf_path)
        for page_number, content in extracted_data.items():
            if content:
                chunks = chunk_text(content)
                all_chunks.extend(chunks)
                embeddings = create_embeddings(chunks)
                all_embeddings.append(embeddings)

  
    all_embeddings = np.vstack(all_embeddings)

  
    index = faiss.IndexFlatL2(all_embeddings.shape[1])  # L2 distance
    index.add(all_embeddings)  # Add embeddings to the index

  
    while True:
        user_input = input("Enter your query (or 'exit' to quit): ")
        
        if user_input.lower() == 'exit':
            print("Exiting the program.")
            break
        
      
        query_embedding = embedding_model.encode([user_input])
        
      
        D, I = index.search(query_embedding, k=5)  # Get top 5 results
        results = [(all_chunks[i], D[0][j]) for j, i in enumerate(I[0])]

       
        if results:
            print("\nResults found:")
            for chunk, distance in results:
                print(f"\nChunk (Distance: {distance:.4f}):\n{chunk}\n")
            
           
            response = llm(f"Based on the following information: {results[0][0]}, answer the query: {user_input}", max_length=150, truncation=True)
            print("\nGenerated Response:\n", response[0]['generated_text'].strip())
        else:
            print("No results found for your query.")

if __name__ == "__main__":
    main()
