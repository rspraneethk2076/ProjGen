from pathlib import Path

# Establish the base directory
BASE_DIR = Path(__file__).resolve().parent

# Folder paths
CODE_ENCODE_DIR = BASE_DIR / 'Code_encode'
CODE_GEN_DIR = BASE_DIR / 'Code_gen'
FRONTEND_DIR = BASE_DIR / 'Frontend'
LLAMA_RAG_DIR = BASE_DIR / 'Llama_RAG'
FILES_DIR = BASE_DIR / 'files'
PAGES_DIR = FRONTEND_DIR / 'pages'

# File paths
FORMAT_FOLDERS_PY = CODE_ENCODE_DIR / 'format_folders.py'
REMOVE_NOISE_PY = CODE_ENCODE_DIR / 'remove_noise.py'
GENCODE_PY = CODE_GEN_DIR / 'Gencode.py'
FRONT_CODE_PY = FRONTEND_DIR / 'front_code.py'
CODE_GEN_PY = PAGES_DIR / 'code_Gen.py'
CODE_TEST_PY = PAGES_DIR / 'Code_test.py'
MAIN_SERVER_PY = PAGES_DIR / 'Main Server.py'
RUN_PROJECT_SERVER_PY = PAGES_DIR / 'Run The project Server.py'
CHATBOT_PY = LLAMA_RAG_DIR / 'chatbot.py'
NEW_PY = LLAMA_RAG_DIR / 'new.py'
VECTORS_PY = LLAMA_RAG_DIR / 'vectors.py'
LOG_FUNCTION_PY = BASE_DIR / 'log_function.py'
LOG_FILE_PATH = FRONTEND_DIR / 'app.log'
PROJECTS_DIR = BASE_DIR / 'projects'
ZIP_FILES_DIR = BASE_DIR / 'zip_files'