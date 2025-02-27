from langchain_community.document_loaders import PDFPlumberLoader
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file using PDFPlumberLoader."""
    loader = PDFPlumberLoader(pdf_path)
    docs = loader.load()
    text = "\n".join(doc.page_content for doc in docs)
    return text

def create_faiss_index(texts, embedding_model):
    """Generate FAISS vector store from extracted text."""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_text(texts)

    # Convert text chunks into Document objects
    documents = [Document(page_content=chunk) for chunk in chunks]

    # Create FAISS vector store properly
    vector_store = FAISS.from_documents(documents, embedding_model)
    
    #Save FAISS Index
    vector_store.save_local("faiss_index")

    return vector_store, chunks


