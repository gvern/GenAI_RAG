# General Platform to RAG (Retrieval-Augmented Generation) (French Below)

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


git clone https://github.com/gvern/GenAI_RAG.git
cd GenAI_RAG
Install the required packages:
pip install -r requirements.txt

###Usage
To start the application, run the following command in the root directory of the project:
python main.py
This will launch the Gradio interface in your default web browser.

###Development
Adding New Features
To add new features, create a branch from main, add your new feature, and then create a pull request describing your changes.


# Plateforme Générale pour RAG (Retrieval-Augmented Generation)

## Présentation

Cette plateforme est conçue pour gérer et interagir avec des documents via un système de génération augmentée par recherche (RAG), améliorant le traitement des documents grâce à des techniques avancées d'IA. Elle permet aux utilisateurs d'importer, de gérer et d'interagir avec divers types de documents, en utilisant de grands modèles de langage pour générer du texte conscient du contexte basé sur le contenu des documents.

## Fonctionnalités

- **Gestion de documents** : Importation et gestion de divers types de documents incluant des PDF, DOCs, CSVs, et fichiers TXT.
- **Intégration de modèles** : Utilisation de modèles provenant du hub de modèles de Hugging Face ou de modèles locaux pour la génération de texte.
- **Fragmentation personnalisable** : Personnalisation des paramètres de fragmentation des documents pour optimiser la gestion pour différents types de données.
- **Interactions interactives** : Utilisation de l'apprentissage zero-shot ou few-shot pour interagir avec les documents.
- **Récupération d'informations** : Récupération et affichage d'informations telles que les réponses directes, le contexte, les références documentaires et les numéros de pages.

## Architecture du système

L'application comprend quatre principales fenêtres UI, chacune conçue pour gérer différents aspects de l'interaction avec les documents et du processus de génération de texte :

1. **Fenêtre UI 1** : Configuration pour la fragmentation des documents.
2. **Fenêtre UI 2** : Sélection et configuration des modèles.
3. **Fenêtre UI 3** : Interface utilisateur principale pour la génération de réponses utilisant RAG.
4. **Fenêtre UI 4** : Interface pour l'augmentation du contexte et la génération de nouveaux contenus à partir des données récupérées.

## Mise en route

### Prérequis

Avant de commencer, assurez-vous d'avoir installé :
- Python 3.8 ou supérieur
- pip (installateur de paquets Python)

### Installation

Clonez le dépôt sur votre machine locale :

git clone https://github.com/your-github/GenAI_RAG.git
cd GenAI_RAG

###Installez les bibliothèques requises :

pip install -r requirements.txt

###Utilisation
Pour démarrer l'application, exécutez la commande suivante dans le répertoire racine du projet :

python main.py
Cela lancera l'interface Gradio dans votre navigateur web par défaut.

###Développement
Ajout de nouvelles fonctionnalités
Pour ajouter de nouvelles fonctionnalités, créez une branche à partir de main, ajoutez votre nouvelle fonctionnalité, puis créez une demande de tirage (pull request) décrivant vos changements.