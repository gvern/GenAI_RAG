import gradio as gr
import os

def chunk_text(text, chunk_size, overlap, algorithm='simple'):
    words = text.split()
    chunks = []
    current_start = 0

    while current_start < len(words):
        current_end = current_start + chunk_size
        chunks.append(" ".join(words[current_start:current_end]))
        current_start = current_end - overlap

        if current_start + chunk_size - overlap >= len(words) and current_start < len(words):
            chunks.append(" ".join(words[current_start:]))
            break

    # Si vous avez un algorithme de chunking plus avancé, vous pouvez l'ajouter ici.
    return "\n\n---\n\n".join(chunks)

def process_chunking(file, chunk_size, overlap, algorithm, output_path):
    if file is None:
        return "Veuillez télécharger un fichier."
    if not output_path:
        return "Veuillez spécifier un chemin de sortie."
    if chunk_size <= 0 or overlap < 0:
        return "La taille du chunk doit être positive et le chevauchement doit être non-négatif."


    # Lecture du fichier texte
    text = file.read().decode("utf-8")

    # Application de la fonction de chunking
    chunks = chunk_text(text, chunk_size, overlap, algorithm)

    # Préparation du chemin de sortie et sauvegarde des chunks
    if not os.path.exists(output_path):
        os.makedirs(output_path, exist_ok=True)
    output_file_path = os.path.join(output_path, "chunked_dataset.txt")

    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(chunks)

    return f"Chunking terminé avec succès. Résultat sauvegardé à : {output_file_path}"

# Création de l'interface utilisateur avec Gradio
with gr.Blocks() as app:
    with gr.Row():
        gr.Markdown("Configuration initiale du chunking")
    with gr.Row():
        file_input = gr.File(label="Charger un fichier texte", type="binary", file_count="multiple")
        chunk_size = gr.Number(label="Taille de chunk (en mots)", value=100, step=1)
        overlap = gr.Slider(minimum=0, maximum=100, label="Pourcentage de chevauchement", value=0)
    with gr.Row():
        algorithm = gr.Dropdown(label="Choisissez un algorithme de chunking", choices=['simple', 'avancé'], value='simple')
        output_path = gr.Textbox(label="Chemin pour sauvegarder le dataset chunké", placeholder="/chemin/vers/sauvegarde")
    with gr.Row():
        process_button = gr.Button("Démarrer le chunking")
    
    result_area = gr.Textbox(label="Résultat du chunking", lines=4)
    
    process_button.click(fn=process_chunking, inputs=[file_input, chunk_size, overlap, algorithm, output_path], outputs=result_area)

if __name__ == "__main__":
    app.launch()
