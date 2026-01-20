import faiss
import numpy as np
import openai
import os
import json

# Load environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Set API key globally
openai.api_key = OPENAI_API_KEY
# Async Client for search queries
async_client = openai.AsyncOpenAI(api_key=OPENAI_API_KEY)

# Path to FAISS index
FAISS_INDEX_PATH = "faiss_index.bin"
COCKTAILS_JSON = "cocktail_dataset.json"

def embed_text(text: str) -> np.array:
    """Converts text into an embedding (Synchronous for initialization)."""
    response = openai.embeddings.create(
        model="text-embedding-ada-002",
        input=[text]
    )
    return np.array(response.data[0].embedding, dtype=np.float32)

async def embed_text_async(text: str) -> np.array:
    """Converts text into an embedding (Async for search)."""
    response = await async_client.embeddings.create(
        model="text-embedding-ada-002",
        input=[text]
    )
    return np.array(response.data[0].embedding, dtype=np.float32)

class FaissIndex:
    def __init__(self):
        self.index = None
        self.cocktail_data = []
        self.load_data()

    def load_data(self):
        """Load cocktail dataset and create FAISS index."""
        if os.path.exists(COCKTAILS_JSON):
            with open(COCKTAILS_JSON, "r", encoding="utf-8") as file:
                self.cocktail_data = json.load(file)

            # Generate OpenAI embeddings for all cocktails
            embeddings = np.array([embed_text(" ".join(c["ingredients"])) for c in self.cocktail_data], dtype=np.float32)
            self.index = faiss.IndexFlatL2(embeddings.shape[1])
            self.index.add(embeddings)

            # Save FAISS index
            faiss.write_index(self.index, FAISS_INDEX_PATH)

    async def search(self, query: str, k: int = 5):
        """Search FAISS index for similar cocktails (Async)."""
        if not os.path.exists(FAISS_INDEX_PATH):
            print("FAISS index not found. Please rebuild it.")
            return []

        # Load FAISS index if not already loaded
        if self.index is None:
            self.index = faiss.read_index(FAISS_INDEX_PATH)

        # Generate embedding asynchronously
        query_embedding = np.array([await embed_text_async(query)], dtype=np.float32)
        distances, indices = self.index.search(query_embedding, k)
        
        results = []
        for idx in indices[0]:
            if 0 <= idx < len(self.cocktail_data):
                results.append(self.cocktail_data[idx])
        
        return results

# Initialize FAISS index
faiss_index = FaissIndex()
