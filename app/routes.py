# app/routes.py
from fastapi import APIRouter
from pydantic import BaseModel
from app.faiss_db import faiss_index
from app.llm_service import ask_gpt

router = APIRouter()
# Request model for incoming chat messages
class CocktailQuery(BaseModel):
    question: str

@router.post("/chat")
async def chat_with_cocktail_advisor(request: CocktailQuery):
    # Step 1: Retrieve relevant cocktails from FAISS
    relevant_cocktails = await faiss_index.search(request.question, k=5)

    # Step 2: Build a context prompt for OpenAI
    context = "\n".join([f"- {c['name']} ({', '.join(c['ingredients'])})" for c in relevant_cocktails])
    prompt = f"Using the following cocktail knowledge:\n{context}\n\nAnswer the question: {request.question}"

    # Step 3: Get a response from OpenAI
    answer = await ask_gpt(prompt)

    return {"reply": answer, "relevant_cocktails": relevant_cocktails}


class CocktailSearchRequest(BaseModel):
    query: str

@router.post("/search")
async def search_cocktail(request: CocktailSearchRequest):
    results = await faiss_index.search(request.query, k=5)
    return {"cocktails": results}
