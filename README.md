# 🃏 Générateur de Flashcards IA

Un outil qui génère automatiquement des flashcards de révision 
à partir de tes cours PDF ou TXT. Tourne entièrement en local, 
sans API payante.

## Fonctionnalités
- Upload de fichiers PDF et TXT
- Génération automatique de questions/réponses
- Navigation entre les cartes
- Export des flashcards en JSON
- Choix du nombre de cartes (5 à 20)

## Prérequis
- [Ollama](https://ollama.com) installé avec le modèle `llama3.1:8b`
- Python 3.x

## Installation

1. Clone le repo
2. Installe les dépendances :
   pip install streamlit ollama pymupdf
3. Lance Ollama en arrière-plan
4. Lance l'app :
   streamlit run app.py