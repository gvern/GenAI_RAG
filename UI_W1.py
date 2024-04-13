# Import des bibliothèques nécessaires
import os
import gradio as gr
from docx import Document
import PyPDF2
from io import BytesIO
import nltk
from nltk.tokenize import sent_tokenize

# Téléchargement des données nécessaires pour nltk
nltk.download('punkt')

# Extraction du texte des documents DOCX
def extract_text_from_docx(file_content):
    document = Document(BytesIO(file_content))
    return "\n".join([paragraph.text for paragraph in document.paragraphs if paragraph.text])

# Extraction du texte des documents PDF
def extract_text_from_pdf(file_content):
    reader = PyPDF2.PdfFileReader(BytesIO(file_content))
    text = []
    for page in range(reader.numPages):
        page_text = reader.getPage(page).extract_text()
        if page_text:
            text.append(page_text)
    return "\n".join(text)

# Fonction pour découper le texte en chunks
def chunk_text(text, chunk_size, overlap, algorithm='simple'):
    chunks = []
    if algorithm == 'simple':
        words = text.split()
        current_start = 0
        while current_start < len(words):
            current_end = current_start + chunk_size
            chunks.append(" ".join(words[current_start:current_end]))
            current_start = current_end - overlap
            if current_start + chunk_size - overlap >= len(words) and current_start < len(words):
                chunks.append(" ".join(words[current_start:]))
                break
    elif algorithm == 'advanced':
        sentences = sent_tokenize(text)
        current_start = 0
        while current_start < len(sentences):
            current_end = min(current_start + chunk_size, len(sentences))
            chunks.append(" ".join(sentences[current_start:current_end]))
            current_start = current_end
    else:
        return "Algorithm not implemented."
    return "\n\n---\n\n".join(chunks)

# Traitement des fichiers téléchargés, chunking et sauvegarde
def process_chunking(file_info, chunk_size, overlap, algorithm, output_path):
    if not file_info:
        return "Veuillez télécharger un fichier."
    if not output_path:
        return "Veuillez spécifier un chemin de sortie."
    if chunk_size <= 0 or overlap < 0:
        return "La taille du chunk doit être positive et le chevauchement doit être non-négatif."

    try:
        file_content = file_info['content']
        file_name = file_info['name']

        if file_name.endswith('.docx'):
            text = extract_text_from_docx(file_content)
        elif file_name.endswith('.pdf'):
            text = extract_text_from_pdf(file_content)
        else:
            return "Format de fichier non supporté."

        chunks = chunk_text(text, chunk_size, overlap, algorithm)
        if not os.path.exists(output_path):
            os.makedirs(output_path, exist_ok=True)
        output_file_path = os.path.join(output_path, "chunked_text.txt")
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.write(chunks)
        return f"Chunking terminé avec succès. Résultat sauvegardé à : {output_file_path}"
    except Exception as e:
        return f"Une erreur est survenue lors du traitement du fichier : {str(e)}"

# Configuration de l'interface Gradio
with gr.Blocks() as app:
    with gr.Row():
        gr.Markdown("### Configuration initiale du chunking")
    with gr.Row():
        file_input = gr.File(label="Charger un fichier", type="binary", file_types=["docx", "pdf"], file_count="multiple")
        chunk_size = gr.Number(label="Taille de chunk (en mots)", value=100, step=1)
        overlap = gr.Slider(minimum=0, maximum=50, label="Chevauchement (en mots)")
        algorithm_selector = gr.Dropdown(['simple', 'advanced'], label="Algorithme de chunking", value='simple')
        output_path = gr.Textbox(label="Chemin de sortie", placeholder="Entrez le chemin de sortie ici")
    with gr.Row():
        submit_button = gr.Button("Commencer le chunking")
        output_text = gr.Textbox(label="Aperçu des chunks")
    submit_button.click(process_chunking, inputs=[file_input, chunk_size, overlap, algorithm_selector, output_path], outputs=output_text)

app.launch()
