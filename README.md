# ProjGen Setup Guide

This guide provides clear steps to set up **ProjGen** with backend, frontend, and RAG integration using **Ollama** and **Qdrant**.

---

## 1. Prerequisites

- **Ollama** (Download from [ollama.ai](https://ollama.ai/))  
- **Docker Desktop** (Download from [docker.com](https://www.docker.com/products/docker-desktop/))  
- **Python 3.12.7** installed on your system  

---

## 2. Running Ollama

1. Install and launch Ollama.  
2. Pull and run the LLaMA model:  

   ```bash
   ollama pull llama3.2:3b
   ollama run llama3.2:3b
   ```

Ensure it runs correctly before continuing.

---

## 3. Clone Repository & Environment Setup

1. Clone the repository and navigate into the folder:

   ```bash
   git clone https://github.com/rspraneethk2076/ProjGen.git
   cd GenMaya3s
   ```

2. Create a Python virtual environment:

   ```bash
   python -m venv env
   ```

3. Activate the environment:  

   - **Windows**:  
     ```bash
     .\env\Scripts\activate
     ```  
   - **MacOS/Linux**:  
     ```bash
     source env/bin/activate
     ```
4. Install the libraries:  
     ```bash
     pip install -r requirements.txt
     ```  

---

## 4. Running Backend and Frontend

1. Start backend service:

   ```bash
   cd GenMaya3s/Code_gen
   python gencode.py
   ```

2. In another terminal (same environment), run frontend:

   ```bash
   cd GenMaya3s/Frontend
   streamlit run front_code.py
   ```

Both services must be running simultaneously.  
Port numbers are predefined in the code.

---

## 5. Setting Up Qdrant with Docker

Run the following in your terminal:

```bash
docker pull qdrant/qdrant
docker run -p 6333:6333 -v .:/qdrant/storage qdrant/qdrant
```


![Screenshot 2025-09-28 094144](https://github.com/user-attachments/assets/9bc4d69b-4dcb-4189-9e54-5e58d53cfc77)

---

## 6. Code Correction Service

If code generation fails, start the **Code Corrector** service:

```bash
cd GenMaya3s/Code_correcter
python code.py
```

When you click **Check Code** in the UI, corrections will be applied, and regenerated files will be produced.

---

## 7. Notes

- If a file is not generated correctly in the first attempt, **re-run the request** or re-submit the project details.  
- Ensure both **Qdrant** and **Ollama** are active before using RAG.  

---

✅ With this setup, you are ready to work with GenMaya3s and implement Retrieval-Augmented Generation (RAG).
