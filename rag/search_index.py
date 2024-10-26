import numpy as np
from inference.embeddings.openai import get_embedding

def search_index(index, model, query, k):
    # Encode the query string into an embedding
    query_embedding = get_embedding(query)
    
    # Ensure the query embedding is in the correct format (float32 and 2D)
    query_embedding = np.array(query_embedding, dtype=np.float32).reshape(1, -1)
    
    # Perform the search
    distances, indices = index.search(query_embedding, k)
    
    return distances[0], indices[0]
