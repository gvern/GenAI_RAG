import gradio as gr
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import os

def load_model_from_hf(model_id, api_key, compute_resource):
    try:
        # Configuration des clés API
        os.environ["HF_HOME"] = ".cache/huggingface"
        os.environ["TRANSFORMERS_CACHE"] = ".cache/huggingface/transformers"
        os.environ["HF_DATASETS_CACHE"] = ".cache/huggingface/datasets"
        os.environ["HF_METRICS_CACHE"] = ".cache/huggingface/metrics"
        os.environ["HF_API_TOKEN"] = api_key

        # Détermination du device basé sur le choix de l'utilisateur
        device = "cuda" if compute_resource == "GPU" and torch.cuda.is_available() else "cpu"

        # Chargement du modèle et du tokenizer
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        model = AutoModelForCausalLM.from_pretrained(model_id).to(device)
        return f"Modèle chargé avec succès sur {device} : {model_id}"
    except Exception as e:
        return f"Erreur lors du chargement du modèle : {str(e)}"

with gr.Blocks() as app:
    with gr.Row():
        gr.Markdown("### Configuration du Modèle LLM")

    with gr.Row():
        model_id_input = gr.Textbox(label="Identifiant du modèle Hugging Face")
        api_key_input = gr.Textbox(label="Clé API Hugging Face", type="password")
        compute_resource = gr.Radio(label="Choisir la ressource de calcul", choices=["CPU", "GPU"], value="CPU")
        load_button = gr.Button("Charger le modèle")
        status_label = gr.Label()
        load_button.click(load_model_from_hf, inputs=[model_id_input, api_key_input, compute_resource], outputs=status_label)

app.launch()
