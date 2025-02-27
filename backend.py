from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from document_loader import extract_text_from_pdf, create_faiss_index
from langchain_huggingface import HuggingFaceEmbeddings
from chat import get_chat_response
from pydantic import BaseModel  
import os

# Initialize FastAPI app
app = FastAPI()

# Define directory for storing uploaded PDFs
UPLOAD_DIR = "uploaded_pdfs"
os.makedirs(UPLOAD_DIR, exist_ok=True)  # Create directory if it doesn't exist

# Initialize the embedding model for text vectorization
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


@app.post("/upload/")
async def upload_pdf(file: UploadFile = File(...)):
    """
    API endpoint to upload a PDF, extract its text, and index it in FAISS.
    
    Steps:
    1. Validate that the uploaded file is a PDF.
    2. Save the file in the "uploaded_pdfs" directory.
    3. Extract text from the PDF.
    4. Create and store embeddings using FAISS.
    5. Return a success response.
    """

    # Check if the uploaded file is a valid PDF
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDFs are accepted.")

    # Define the file path where the PDF will be saved
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())  # Save file asynchronously

    try:
        # Extract text from the uploaded PDF
        text = extract_text_from_pdf(file_path)

        # Generate and store FAISS index
        faiss_store, chunks = create_faiss_index(text, embeddings)

        # Return a success response with details
        return JSONResponse(content={"message": f"PDF '{file.filename}' processed and indexed successfully.",
                                     "chunks": len(chunks)})
    except Exception as e:
        # Handle any errors during processing
        raise HTTPException(status_code=500, detail=f"Error processing the file: {str(e)}")
    

# Define request model for chatbot input
class ChatRequest(BaseModel):
    question: str  # User's query


# Define response model for chatbot output
class ChatResponse(BaseModel):
    answer: str  # AI-generated response


@app.post("/chat/", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    API endpoint to handle chatbot queries.

    Steps:
    1. Receive user question from request.
    2. Retrieve relevant document chunks using FAISS.
    3. Generate a response using LLaMA3.
    4. Return the response.
    """
    response = get_chat_response(request.question)
    return ChatResponse(answer=response)


@app.get("/")
async def root():
    """
    Root API endpoint for testing.

    Returns a welcome message.
    """
    return {"message": "Welcome to the FAISS-powered chatbot backend!"}
