import os
from langchain.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chat_models import init_chat_model

# Load FAISS Index
INDEX_PATH = "faiss_index"
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")



# Load Groq API Key from environment
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is not set. Please set it as an environment variable.")



# Initialize Chat Model (Groq LLaMA3)
llm = init_chat_model("llama3-8b-8192", model_provider="groq")

def get_chat_response(question: str) -> str:
    """Retrieve the most relevant document chunks and generate a chatbot response."""
    try:
        
        if os.path.exists(INDEX_PATH):
            vector_store = FAISS.load_local(INDEX_PATH, embedding_model,allow_dangerous_deserialization=True)
        else:
            raise RuntimeError("FAISS index not found. Please upload and index documents first.")
        
        # Search FAISS for relevant documents
        docs = vector_store.similarity_search_with_score(question, k=3)

        if not docs:
            return "I couldn't find relevant information in the uploaded documents."

        # Concatenate retrieved text to form context
        context = "\n".join([doc[0].page_content for doc in docs])

        # Generate response using LLaMA3
        prompt = f"Based on the following information, answer the user's question:\n\n{context}\n\nUser: {question}\nAI:"
        response = llm.invoke(prompt)

        return response.content
    except Exception as e:
        return f"Error generating response: {str(e)}"

