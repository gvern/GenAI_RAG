import os
from fastapi import FastAPI, File, UploadFile
from starlette.responses import JSONResponse
import uvicorn
from retrieval_system import DocumentStore, retrieve_context
from model import load_model, generate_text

# Initialisation de l'API
app = FastAPI()

# Configuration de l'espace de stockage des documents
doc_store = DocumentStore()

# Chargement du modèle
model = load_model(model_name="gpt-3.5-turbo")

@app.post("/upload/")
async def create_upload_files(file: UploadFile = File(...)):
    content = await file.read()
    doc_store.add_document(content)
    return {"filename": file.filename}

@app.post("/generate/")
async def generate(prompt: str):
    context = retrieve_context(doc_store, prompt)
    response = generate_text(model, prompt, context)
    return JSONResponse(content={"response": response})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
