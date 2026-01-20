import openai
import os

# Load environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client (Async for FastAPI)
client = openai.AsyncOpenAI(api_key=OPENAI_API_KEY)

async def ask_gpt(prompt: str) -> str:
    """Send a query to OpenAI GPT-4 efficiently (non-blocking)."""
    response = await client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a witty and knowledgeable cocktail expert. Provide concise and helpful answers."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content
