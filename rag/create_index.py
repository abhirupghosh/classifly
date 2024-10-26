import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from inference.embeddings.openai import get_embedding

def create_index(df, column, model=None):
    # Extract the specified column as a list of strings
    texts = df[column].tolist()
    
    # Encode the texts into embeddings
    from concurrent.futures import ThreadPoolExecutor, as_completed
    
    with ThreadPoolExecutor() as executor:
        future_to_text = {executor.submit(get_embedding, text): text for text in texts}
        embeddings = [future.result() for future in as_completed(future_to_text)]
    
    # Ensure the embeddings are in float32 format
    embeddings = np.array(embeddings, dtype=np.float32)
    
    # Get the dimensionality of the embeddings
    d = embeddings.shape[1]
    
    # Create a FAISS index
    index = faiss.IndexFlatL2(d)
    
    # Add the embeddings to the index
    index.add(embeddings)

    print(index)
    
    return index, model
