import gradio as gr
from transformers import pipeline, set_seed
import os

# Fonction pour initialiser et utiliser un modèle LLM pour la génération de contenu
def generate_content(model_name, context, prompt, creativity_level, tone, output_length):
    """
    Utilise un modèle LLM spécifié pour générer du contenu basé sur un contexte et un prompt donnés.
    Les paramètres supplémentaires permettent de personnaliser la sortie générée.
    """
    # Configuration de base du modèle
    generator = pipeline('text-generation', model=model_name)
    set_seed(42)  # Pour la reproductibilité
    
    # Adaptation du prompt avec le contexte
    full_prompt = f"{context}\n\n{prompt}"
    
    # Génération du contenu
    generated_outputs = generator(full_prompt, max_length=output_length, num_return_sequences=1, 
                                   temperature=creativity_level)
    
    # Extraction du texte généré
    generated_text = generated_outputs[0]['generated_text']
    
    # Formatage du texte généré selon la tonalité (exemplatif)
    if tone == "Formel":
        generated_text = generated_text.replace('!', '.')
    elif tone == "Ludique":
        generated_text = f"😄 {generated_text} 😄"
    # Le traitement pour "Informel" serait similaire.
    
    return generated_text

# Construction de l'interface Gradio
with gr.Blocks() as app:
    gr.Markdown("## Interface d'Augmentation du Contexte")
    
    with gr.Group():
        with gr.Tab(label="Contexte Récupéré"):
            retrieved_context = gr.Textbox(label="Contexte Récupéré", placeholder="Le contexte récupéré s'affiche ici...", lines=6)
        with gr.Tab(label="Créez votre prompt"):
            prompt_creation = gr.Textbox(label="Créez votre prompt", placeholder="Entrez votre prompt ici...", lines=4)
    
    with gr.Group():
        model_name = gr.Dropdown(label="Sélectionnez un modèle LLM", choices=["gpt2", "EleutherAI/gpt-neo-2.7B"], value="gpt2")
        creativity_level = gr.Slider(minimum=0.5, maximum=1.0, step=0.01, label="Niveau de créativité", value=0.7)
        tone = gr.Radio(choices=["Formel", "Informel", "Ludique"], label="Tonalité", value="Informel")
        output_length = gr.Number(label="Longueur de Sortie", value=150, step=10)
    
    generate_button = gr.Button("Générer le Contenu")
    generated_content_display = gr.Textbox(label="Contenu Généré", placeholder="Le contenu généré s'affichera ici...", lines=10)

    generate_button.click(
        fn=generate_content,
        inputs=[model_name, retrieved_context, prompt_creation, creativity_level, tone, output_length],
        outputs=generated_content_display
    )

if __name__ == "__main__":
    app.launch()
