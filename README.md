# General Platform to RAG (Retrieval-Augmented Generation)

## Overview

This platform is designed to manage and interact with documents via a Retrieval-Augmented Generation system, enhancing document processing with advanced AI techniques. It allows users to import, manage, and interact with various types of documents, utilizing large language models for generating context-aware text based on the content of the documents.

## Features

- **Document Management**: Import and manage various document types including PDFs, DOCs, CSVs, and TXT files.
- **Model Integration**: Utilize models from Hugging Face's model hub or local models for text generation.
- **Customizable Chunking**: Customize document chunking parameters to optimize handling for different data types.
- **Interactive Prompts**: Use zero-shot or few-shot learning to interact with documents.
- **Information Retrieval**: Retrieve and display information such as direct answers, context, document references, and page numbers.

## System Architecture

The application includes four main UI Windows, each designed to handle different aspects of the document interaction and text generation process:

1. **UI Window 1**: Setup for document chunking.
2. **UI Window 2**: Model selection and parameter configuration.
3. **UI Window 3**: Main user interface for generating answers using RAG.
4. **UI Window 4**: Interface for augmenting context and generating new content from retrieved data.

## Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.8 or higher
- pip (Python package installer)

### Installation

Clone the repository to your local machine:

```bash
git clone https://github.com/your-github/GenAI_RAG.git
cd GenAI_RAG
Install the required packages:

bash
Copy code
pip install -r requirements.txt
Usage
To start the application, run the following command in the root directory of the project:

bash
Copy code
python main.py
This will launch the Gradio interface in your default web browser.

Development
Adding New Features
To add new features, create a branch from main, add your new feature, and then create a pull request describing your changes.