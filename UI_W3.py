import gradio as gr
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch

# Supposons que le modèle ait déjà été chargé via une autre interface ou en arrière-plan
model_name = "facebook/bart-large-cnn"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
model.eval()

def generate_answer(prompt, vector_data):
    # Simulons l'utilisation des vecteurs de données pour sélectionner un contexte pertinent
    # Cette partie serait normalement plus complexe et intégrée avec le backend de gestion des données.
    context = "Contexte simulé basé sur les données vectorisées fournies."

    # Génération de la réponse en utilisant le modèle
    inputs = tokenizer.encode("Résumez: " + context + " " + prompt, return_tensors="pt", max_length=1024, truncation=True)
    outputs = model.generate(inputs, max_length=150, num_return_sequences=1)
    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return answer, context

with gr.Blocks() as app:
    with gr.Row():
        gr.Markdown("##Génération de Texte avec RAG")
    
    with gr.Row():
        vector_dataset = gr.Dropdown(label="Choisir le dataset de vecteurs", choices=['Dataset1', 'Dataset2', 'Dataset3'], value='Dataset1')
        user_prompt = gr.Textbox(label="Entrée du prompt utilisateur", placeholder="Entrez votre prompt ici...")
        submit_button = gr.Button("Démarrer le processus RAG")
    
    with gr.Row():
        generated_answer_display = gr.Textbox(label="Réponse générée", placeholder="La réponse générée s'affichera ici...", lines=6)
        retrieval_info_display = gr.Textbox(label="Informations de récupération", placeholder="Détails du contexte de récupération...", lines=6)

    submit_button.click(
        fn=generate_answer,
        inputs=[user_prompt, vector_dataset],
        outputs=[generated_answer_display, retrieval_info_display]
    )

app.launch()
