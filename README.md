# 🍹 Cocktail Advisor Chat 🗨️

A smart **FastAPI-based** chat application that provides expert cocktail recommendations using **Retrieval-Augmented Generation (RAG)**. It combines **OpenAI's GPT-4** for intelligent responses with a **FAISS vector database** for precise ingredient-based lookups.

---

## **🚀 Features**

- **🤖 AI-Powered Bartender**: Ask detailed questions like *"What's a good spicy cocktail made with tequila?"* and get contextual answers.
- **🔍 Semantic Search**: Uses OpenAI embeddings to understand the *meaning* of your query, not just keyword matching.
- **🍹 Similar Cocktail Suggestions**: Returns a list of real similar cocktails from the dataset alongside the AI answer.
- **⚡ High Performance & Scalable**: Built with **Async FastAPI** and **Async OpenAI Clients** to handle concurrent requests efficiently without blocking, powered by **FAISS** for millisecond-level retrieval.
- **🐳 Dockerized**: Ready to deploy with a single command.

---

## **🏗️ Architecture**

The application enables a RAG workflow:
1. **User Query**: You ask a question.
2. **Embedding**: Your question is converted into a vector using `text-embedding-ada-002`.
3. **Retrieval**: FAISS searches the `cocktail_dataset.json` for the most relevant cocktails based on ingredients and descriptions.
4. **Augmentation**: The relevant cocktail data is injected into a prompt for GPT-4.
5. **Generation**: GPT-4 answers your question using the retrieved knowledge.

---

## **🛠️ Tech Stack**

- **Backend framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **LLM**: OpenAI GPT-4
- **Vector DB**: [FAISS](https://github.com/facebookresearch/faiss)
- **Embeddings**: OpenAI `text-embedding-ada-002`
- **Containerization**: Docker & Docker Compose

---

## **📋 Prerequisites**

Before running the application, ensure you have:
1. **OpenAI API Key**: Sign up at [platform.openai.com](https://platform.openai.com).
2. **Docker Desktop** (recommended) OR **Python 3.10+**.

---

## **📦 Installation & Setup**

### **Option 1: Run with Docker (Recommended)**

1. **Clone the repository:**
   ```bash
   git clone <repository_url>
   cd cocktail-advisor-chat
   ```

2. **Configure Environment Variables:**
   Create a `.env` file in the root directory:
   ```bash
   # Windows (PowerShell)
   New-Item .env -Value "OPENAI_API_KEY=sk-your-api-key-here"

   # Mac/Linux
   echo "OPENAI_API_KEY=sk-your-api-key-here" > .env
   ```

3. **Build and Run:**
   ```bash
   docker-compose up --build
   ```

4. **Access the App:**
   Open your browser and navigate to: [http://localhost:8000](http://localhost:8000)

---

### **Option 2: Run Locally (Python)**

If you prefer running without Docker:

1. **Create a virtual environment:**
   ```bash
   python -m venv venv
   # Windows
   .\venv\Scripts\activate
   # Mac/Linux
   source venv/bin/activate
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Environment Variable:**
   ```bash
   # Windows (CMD)
   set OPENAI_API_KEY=sk-your-api-key-here
   # Windows (PowerShell)
   $env:OPENAI_API_KEY="sk-your-api-key-here"
   # Mac/Linux
   export OPENAI_API_KEY=sk-your-api-key-here
   ```

4. **Run the Server:**
   ```bash
   uvicorn app.main:app --reload
   ```

---

## **⚠️ Important Note on Startup**

**Indexing Behavior:**
On the very first run (or if `faiss_index.bin` is deleted), the application will **regenerate the vector index**.
- This process converts all cocktails in `cocktail_dataset.json` into embeddings using OpenAI's API.
- **This will consume OpenAI API credits.** based on the dataset size (~200+ items).
- Subsequent restarts will load the cached `faiss_index.bin` instantly.

---

## **📡 API Usage**

You can interact with the API directly using tools like `curl` or Postman.

### **Chat Endpoint**
Get an AI answer based on cocktail knowledge.
- **URL**: `POST /api/chat`
- **Body**:
  ```json
  {
    "question": "What is a good cocktail with gin and lemon?"
  }
  ```

**Example Curl:**
```bash
curl -X 'POST' \
  'http://localhost:8000/api/chat' \
  -H 'Content-Type: application/json' \
  -d '{
  "question": "I want something sweet with rum."
}'
```

---

## **🤝 Contributing**

Feel free to open issues or submit pull requests if you have ideas for improvements, such as adding more cocktails to the dataset or improving the prompt engineering!