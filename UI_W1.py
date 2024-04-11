import gradio as gr

def chunk_text(text, chunk_size, overlap):
    words = text.split()
    if len(words) <= chunk_size:
        return [text]
    
    chunks = []
    current_start = 0
    
    while current_start < len(words):
        current_end = current_start + chunk_size
        chunks.append(" ".join(words[current_start:current_end]))
        current_start = current_end - overlap
        
        if current_start + chunk_size - overlap >= len(words) and current_start < len(words):
            chunks.append(" ".join(words[current_start:]))
            break
            
    return chunks

def process_chunking(file, chunk_size, overlap):
    # Lecture du fichier texte
    with open(file.name, "r", encoding="utf-8") as f:
        text = f.read()
    
    # Application de la fonction de chunking
    chunks = chunk_text(text, chunk_size, overlap)
    
    # Retourne les chunks sous forme de chaîne pour l'affichage
    return "\n\n---\n\n".join(chunks)

# Création de l'interface utilisateur avec Gradio
with gr.Blocks() as app:
    gr.Markdown("Configuration initiale du chunking")
    with gr.Row():
        file_input = gr.File(label="Charger un fichier texte")
        chunk_size = gr.Number(label="Taille de chunk (en mots)", value=100, step=1)
        overlap = gr.Slider(minimum=0, maximum=100, label="Pourcentage de chevauchement", value=0)
    submit_button = gr.Button("Démarrer le chunking")
    
    result_area = gr.Textbox(label="Résultat du chunking", lines=20)
    
    submit_button.click(fn=process_chunking, inputs=[file_input, chunk_size, overlap], outputs=result_area)

if __name__ == "__main__":
    app.launch()
