# GenMaya 3s

Welcome to **GenMaya 3s**, a project designed to streamline code generation and testing workflows with ease. This README provides step-by-step instructions to set up, run, and use the project effectively.

## Prerequisites

- Ensure you have Python 3.13 installed on your system.
- A Python virtual environment is recommended for dependency isolation.
- Install [Streamlit](https://streamlit.io/) in your Python environment.

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/2000030859-saipraneeth/GenMaya3s.git
cd GenMaya3s 
```

### 2. Checkout to Main Branch

```bash
git checkout main
```

### 3. Create a Python Virtual Environment
```bash
python -m venv env
```

### 4. Activate the Virtual Environment
#### Windows:
```bash
.\env\Scripts\activate
```
#### MacOS/Linux:
```bash
source env/bin/activate
```

### 5. Install Dependencies
```bash

pip install -r requirements.txt
```
#### 6. Run the Frontend
Navigate to the Frontend folder and start the Streamlit application:

```bash
cd Frontend
streamlit run front_code.py
```

# Setting Up RAG Implementation

This guide provides step-by-step instructions to set up the environment for implementing Retrieval-Augmented Generation (RAG) using Docker Desktop and Ollama.

---

## Prerequisites

1. **Docker Desktop**  
   Ensure Docker Desktop is installed and running on your system. You can download it [here](https://www.docker.com/products/docker-desktop/).

2. **Ollama**  
   Install Ollama for managing LLaMA models on Windows. You can download Ollama [here](https://ollama.ai/).

---

## Setting Up Qdrant with Docker

1. Open Docker Desktop and ensure it is running.
2. Run the following commands in your terminal or command prompt:

### Pull the Qdrant Image
   ```bash
   docker pull qdrant/qdrant
   docker run -p 6333:6333 -v .:/qdrant/storage qdrant/qdrant
```

1. Setting Up LLaMA with Ollama
2. Install Ollama on your Windows system.

Open Command Prompt and execute the following commands:

### Pull the LLaMA Model
```bash

ollama pull llama3.2:3b
ollama run llama3.2:3b
```

#### Ready to Work with RAG
Once the Qdrant container and the LLaMA model are running, you can start using the RAG workflow with your setup. Ensure both services (Qdrant and Ollama) are operational for seamless integration.
Enjoy your RAG journey! 




