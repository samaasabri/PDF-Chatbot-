# 📄 AI PDF Chatbot 🤖

## 🚀 Overview
A **Python-based application** that uses **AI/ML techniques** to create a **chatbot capable of answering user questions** based on **information extracted from PDF documents**.  

The application enables users to:  
✅ **Upload documents**  
✅ **Interact with the chatbot** through a **simple, accessible interface**  

### **How It Works**
1️⃣ **Extracts text from PDFs**  
2️⃣ **Stores embeddings in FAISS** for efficient retrieval  
3️⃣ **Uses LLaMA3 (via Groq API)** to generate responses  
4️⃣ **Provides an interactive chat UI** for user interaction  

---

## 🔧 Features
✅ Upload PDF documents  
✅ Extract text & store embeddings in FAISS  
✅ Query documents using LLaMA3 (Groq API)  
✅ Interactive Streamlit chat UI  
✅ FastAPI backend for API requests  
✅ Dockerized for easy deployment  

---

## 🔧 Setup Instructions
### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/your-username/chatbot-project.git
cd chatbot-project
```

### **2️⃣ Install Dependencies**
```bash
pip install -r requirements.txt
```

### 3️⃣ Set Up Environment Variables
Replace `your_api_key_here` with your actual Groq API key.
```bash
export GROQ_API_KEY="your_api_key_here"  # Linux/macOS
set GROQ_API_KEY=your_api_key_here       # Windows CMD
```

## 4️⃣ Run the Application Manually
### Start the FastAPI backend:
```bash
uvicorn backend:app --reload
```
### Start the Streamlit frontend:
```bash
streamlit run main.py
```
Now, open:
- **FastAPI Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **Streamlit UI:** [http://localhost:8501](http://localhost:8501)

---

## 🐳 Docker Deployment
### **1️⃣ Build and Run with Docker**
```bash
docker-compose up --build
```
This will start:
- **FastAPI backend** on `http://localhost:8000`
- **Streamlit frontend** on `http://localhost:8501`

### **2️⃣ Stop Docker Containers**
```bash
docker-compose down
```

---

## 📡 API Endpoints
| Method | Endpoint   | Description                         |
|--------|-----------|-------------------------------------|
| POST   | `/upload/` | Upload PDF and store embeddings    |
| POST   | `/chat/`   | Query documents and get responses  |




