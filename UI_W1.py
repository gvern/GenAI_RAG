import re
import os
import gradio as gr
from docx import Document
from io import BytesIO
import nltk
from nltk.tokenize import word_tokenize
import PyPDF2

nltk.download('punkt')

def guess_file_type_by_content(file_content):
    if file_content.startswith(b'%PDF-'):
        return 'pdf'
    elif file_content[0:4] == b'PK\x03\x04':  # DOCX files start with PK
        return 'docx'
    return 'unknown'

def extract_text_from_pdf(file_content):
    with BytesIO(file_content) as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        text = []
        for page in range(len(reader.pages)):
            page_text = reader.pages[page].extract_text()
            if page_text:
                text.append(page_text.replace('\n', ' '))  # Cleaning up text extraction
        return "\n".join(text)

def extract_text_from_docx(file_content):
    document = Document(BytesIO(file_content))
    extracted_text = "\n".join(paragraph.text.strip() for paragraph in document.paragraphs if paragraph.text.strip())
    print("DOCX Text Extraction Complete")  # Debug print
    return extracted_text

def chunk_text_by_words(text, chunk_size):
    words = word_tokenize(text)
    chunks = [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]
    print("Chunking by Words Complete")  # Debug print
    return chunks

def fixed_size_chunking(text, size):
    chunks = [text[i:i+size] for i in range(0, len(text), size)]
    print("Fixed Size Chunking Complete")  # Debug print
    return chunks

def recursive_chunking(text, size, separators):
    if not separators:
        return [text] if len(text) <= size else []
    sep = separators[0]
    chunks = text.split(sep)
    refined_chunks = []
    for chunk in chunks:
        if len(chunk) > size:
            refined_chunks.extend(recursive_chunking(chunk, size, separators[1:]))
        else:
            refined_chunks.append(chunk)
    print("Recursive Chunking Complete")  # Debug print
    return refined_chunks

def content_aware_chunking(text, size):
    code_chunks = re.split(r'```python\n.*?\n```', text, flags=re.DOTALL)
    markdown_chunks = re.split(r'#{1,6} .*', text)
    selected_chunks = code_chunks if len(''.join(code_chunks)) < len(''.join(markdown_chunks)) else markdown_chunks
    print("Content Aware Chunking Complete")  # Debug print
    return selected_chunks

def chunk_text(text, chunk_size, algorithm='Level 1: Fixed-size'):
    if algorithm == 'en mots':
        return chunk_text_by_words(text, chunk_size)
    elif algorithm == 'Level 1: Fixed-size':
        return fixed_size_chunking(text, chunk_size)
    elif algorithm == 'Level 2: Recursive':
        return recursive_chunking(text, chunk_size, ['\n\n', '. ', ', ', ' '])
    elif algorithm == 'Level 3: Content Aware':
        return content_aware_chunking(text, chunk_size)
    return "Algorithm not implemented."

def process_chunking(file_info, chunk_size, overlap, algorithm, output_path):
    if not file_info:
        return "Veuillez télécharger un fichier."
    if not output_path:
        return "Veuillez spécifier un chemin de sortie."
    if chunk_size <= 0:
        return "La taille du chunk doit être positive."

    try:
        file_data = file_info[0] if isinstance(file_info, list) else file_info
        file_content = file_data if isinstance(file_data, bytes) else file_data.get("content")
        file_name = "output" if isinstance(file_data, bytes) else file_data.get("name")

        file_type = guess_file_type_by_content(file_content)
        if file_type == 'docx':
            text = extract_text_from_docx(file_content)
        elif file_type == 'pdf':
            text = extract_text_from_pdf(file_content)
        else:
            return f"Format de fichier non pris en charge: {file_type}"

        chunks = chunk_text(text, chunk_size, algorithm)
        if not os.path.exists(output_path):
            os.makedirs(output_path, exist_ok=True)
        output_file_name = f"chunked_{file_name if file_name else 'output'}.txt"
        output_file_path = os.path.join(output_path, output_file_name)
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.write("\n\n---\n\n".join(chunks))
        print("Output file written successfully")  # Debug print
        return f"Chunking terminé avec succès. Résultat sauvegardé à : {output_file_path}"
    except Exception as e:
        return f"Une erreur est survenue lors du traitement du fichier : {str(e)}"

with gr.Blocks() as app:
    with gr.Row():
        gr.Markdown("### Configuration initiale du chunking")
    with gr.Row():
        file_input = gr.File(label="Charger un fichier", type="binary", file_types=["docx", "pdf"], file_count="multiple")
        chunk_size = gr.Number(label="Taille de chunk (en mots)", value=100, step=1)
        overlap = gr.Slider(minimum=0, maximum=50, label="Chevauchement (en mots)")
        algorithm_selector = gr.Dropdown(['Level 1: Fixed-size', 'Level 2: Recursive', 'Level 3: Content Aware', 'en mots'], label="Algorithme de chunking", value='Level 1: Fixed-size')
        output_path = gr.Textbox(label="Chemin de sortie", placeholder="Entrez le chemin de sortie ici")
    with gr.Row():
        submit_button = gr.Button("Commencer le chunking")
        output_text = gr.Textbox(label="Aperçu des chunks")
    submit_button.click(process_chunking, inputs=[file_input, chunk_size, overlap, algorithm_selector, output_path], outputs=output_text)

app.launch()
