import gradio as gr
from transformers import AutoModelForCausalLM, AutoTokenizer
import os

def load_model_from_hf(model_id, api_key):
    try:
        # Configuration des clés API
        os.environ["HF_HOME"] = ".cache/huggingface"
        os.environ["TRANSFORMERS_CACHE"] = ".cache/huggingface/transformers"
        os.environ["HF_DATASETS_CACHE"] = ".cache/huggingface/datasets"
        os.environ["HF_METRICS_CACHE"] = ".cache/huggingface/metrics"
        os.environ["HF_API_TOKEN"] = api_key

        # Chargement du modèle et du tokenizer
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        model = AutoModelForCausalLM.from_pretrained(model_id)
        return f"Modèle chargé avec succès : {model_id}"
    except Exception as e:
        return f"Erreur lors du chargement du modèle : {str(e)}"

def load_model_from_local(file_info):
    # Simulé: Chargement d'un modèle local
    return f"Modèle local chargé: {file_info['name']}"

with gr.Blocks() as app:
    with gr.Row():
        gr.Markdown("### Configuration du Modèle LLM")

    with gr.Row():
        model_id_input = gr.Textbox(label="Identifiant du modèle Hugging Face")
        api_key_input = gr.Textbox(label="Clé API Hugging Face", type="password")
        load_button = gr.Button("Charger le modèle")
        status_label = gr.Label()

    load_button.click(load_model_from_hf, inputs=[model_id_input, api_key_input], outputs=status_label)

    with gr.Row():
        local_file = gr.File(label="Choisir un modèle sur PC", type="binary")
        local_load_button = gr.Button("Charger le modèle local")
        local_status_label = gr.Label()

    local_load_button.click(load_model_from_local, inputs=[local_file], outputs=local_status_label)

    with gr.Row():
        compute_resource = gr.Radio(label="Choisir la ressource de calcul", choices=["CPU", "GPU"], value="CPU")

app.launch()
