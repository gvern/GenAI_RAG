import gradio as gr
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

# Initialisation du tokenizer et du modèle
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")

def generate_text(user_prompt, batch_size, max_length, use_gpu):
    # Validation des paramètres d'entrée
    if batch_size > 32:
        return "La taille du batch ne peut pas dépasser 32", "Veuillez ajuster la taille du batch."
    if max_length > 512:
        return "La longueur maximale ne peut pas dépasser 512", "Veuillez ajuster la longueur de la séquence."

    # Configuration du modèle pour utiliser GPU ou CPU
    device = "cuda" if use_gpu and torch.cuda.is_available() else "cpu"
    model.to(device)

    # Génération de texte
    inputs = tokenizer.encode(user_prompt, return_tensors="pt").to(device)
    outputs = model.generate(inputs, max_length=max_length, num_return_sequences=batch_size)
    generated_texts = [tokenizer.decode(output, skip_special_tokens=True) for output in outputs]

    return '\n\n'.join(generated_texts), "Processus de génération complété avec succès."

# Configuration de l'interface utilisateur avec Gradio
with gr.Blocks() as app:
    gr.Markdown("## Interface Utilisateur Principale pour la Génération de Texte")

    with gr.Row():
        user_prompt = gr.Textbox(label="Prompt Utilisateur", placeholder="Entrez votre prompt ici...")
        batch_size = gr.Number(label="Taille du Batch", value=1, step=1, minimum=1, maximum=32)
        max_length = gr.Number(label="Longueur de Séquence Maximale", value=50, step=1, minimum=5, maximum=512)
        use_gpu = gr.Checkbox(label="Utiliser le GPU si disponible", value=True)

    with gr.Row():
        start_rag_process = gr.Button("Générer du Texte")
        generated_answer_display = gr.Textbox(label="Texte Généré", interactive=False, placeholder="La réponse générée s'affichera ici...", lines=10, visible=True)
        process_info_display = gr.Textbox(label="Informations du Processus", interactive=False, placeholder="Détails du processus...", lines=3, visible=True)

    start_rag_process.click(
        fn=generate_text,
        inputs=[user_prompt, batch_size, max_length, use_gpu],
        outputs=[generated_answer_display, process_info_display]
    )

app.launch()
