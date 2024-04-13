import gradio as gr
from transformers import pipeline

def load_model(model_name, device):
    """
    Charge un modèle Hugging Face spécifié par l'utilisateur et le configure pour l'utilisation.
    """
    device_index = 0 if device == "GPU" else -1  # Utilise GPU si disponible et demandé, sinon CPU
    nlp_pipeline = pipeline("text-classification", model=model_name, device=device_index)
    return nlp_pipeline

def classify_text(model_pipeline, text):
    """
    Utilise la pipeline de classification de texte pour prédier la classe d'un texte donné.
    """
    predictions = model_pipeline(text)
    return str(predictions)

# Liste de modèles Hugging Face disponibles pour la sélection
models = [
    "distilbert-base-uncased",
    "bert-base-uncased",
    "gpt2"
]

with gr.Blocks() as model_app:
    with gr.Row():
        gr.Markdown("Sélection du modèle et classification de texte")
    
    with gr.Row():
        model_name = gr.Dropdown(label="Choisissez un modèle Hugging Face", choices=models, value=models[0])
        device = gr.Radio(choices=["CPU", "GPU"], label="Exécuter sur", value="CPU")
    
    with gr.Row():
        text_input = gr.Textbox(label="Texte à classifier")
        classify_button = gr.Button("Classer le texte")
        output = gr.Textbox(label="Résultat de la classification")
    
    def update_and_classify(model_name, device, text):
        model_pipeline = load_model(model_name, device)
        return classify_text(model_pipeline, text)

    classify_button.click(fn=update_and_classify, inputs=[model_name, device, text_input], outputs=output)

if __name__ == "__main__":
    model_app.launch()
