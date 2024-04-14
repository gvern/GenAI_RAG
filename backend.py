import gradio as gr
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
from sentence_transformers import SentenceTransformer
import pinecone
import os
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv
from pinecone import Pinecone

# Load environment variables from .env file
load_dotenv()

# Fetch the API key from environment variables
api_key = os.getenv("PINECONE_API_KEY")
if not api_key:
    raise ValueError("PINECONE_API_KEY environment variable not set.")


# Create an instance of the Pinecone class
pc = Pinecone(api_key=api_key)

# Check if the index exists and create it if not
index_name = 'my_index'
namelist = pc.list_indexes()
index_names = [idx.name for idx in namelist]
if index_name not in index_names:
    pc.create_index(
        name=index_name,
        dimension=1536,  # Adjust dimension according to your vector embedding size
        metric='euclidean',  # Choose a metric suitable for your use case
        spec=ServerlessSpec(
            cloud='aws',  # or 'gcp', based on your preference or existing cloud infrastructure
            region='us-west-2'  # Choose the region closest to your users for faster performance
        )
    )

# Now you can use the `pc` object to interact with your index
index = pc.Index(index_name)


# Load the Sentence Transformer Model for Embeddings
embedder = SentenceTransformer('all-MiniLM-L6-v2')

# Load the LLM for content generation
tokenizer = AutoTokenizer.from_pretrained("gpt2")
model = AutoModelForSequenceClassification.from_pretrained("gpt2")

def embed_and_store_documents(docs):
    """ Embeds documents and stores them in Pinecone. """
    embeddings = embedder.encode(docs)
    ids = [str(i) for i in range(len(docs))]
    index.upsert(vectors=zip(ids, embeddings))

def generate_content(prompt):
    """ Generates content based on a user's prompt using an LLM. """
    inputs = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True)
    outputs = model.generate(**inputs, max_length=50)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

def query_index(query, top_k=5):
    """ Queries the Pinecone index for similar documents. """
    query_emb = embedder.encode([query])[0]
    return index.query([query_emb], top_k=top_k)

# Gradio Interface
def interface(prompt):
    results = query_index(prompt)
    content = generate_content(prompt)
    return results, content

with gr.Blocks() as app:
    gr.Markdown("## Query Interface")
    prompt_input = gr.Textbox(label="Enter your query")
    result_output = gr.Textbox(label="Query Results")
    content_output = gr.Textbox(label="Generated Content")
    submit_button = gr.Button("Submit")
    submit_button.click(interface, inputs=prompt_input, outputs=[result_output, content_output])

if __name__ == "__main__":
    app.launch()

