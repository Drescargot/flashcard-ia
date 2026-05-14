import streamlit as st
import ollama
import pymupdf
import json

st.write("test")

st.set_page_config(page_title="Flashcards IA", page_icon="🃏", layout="centered")

st.title("🃏 Générateur de Flashcards")
st.markdown("Upload un cours PDF et génère des flashcards pour réviser.")

def extraire_texte(uploaded_file):
    if uploaded_file.name.endswith('.pdf'):
        doc = pymupdf.open(stream=uploaded_file.read(), filetype="pdf")
        texte = ""
        for page in doc:
            texte += page.get_text()
        return texte
    else:
        return uploaded_file.read().decode('utf-8')

def generer_flashcards(texte, nombre, model):
    prompt = f"""À partir du texte suivant, génère exactement {nombre} flashcards pour réviser.
Réponds UNIQUEMENT avec un JSON valide, sans texte avant ou après, sous ce format :
[
  {{"question": "...", "reponse": "..."}},
  {{"question": "...", "reponse": "..."}}
]

Texte :
{texte[:4000]}"""

    response = ollama.chat(model=model, messages=[
        {'role': 'user', 'content': prompt}
    ])
    
    contenu = response['message']['content']
    debut = contenu.find('[')
    fin = contenu.rfind(']') + 1
    return json.loads(contenu[debut:fin])

# Sidebar
with st.sidebar:
    st.markdown("### ⚙️ Paramètres")
    model = st.selectbox("Modèle", ["llama3.1:8b", "llama3.2:3b"], index=0)
    nombre = st.slider("Nombre de flashcards", 5, 20, 10)

# Main
uploaded_file = st.file_uploader("Uploade ton cours", type=['pdf', 'txt'])

if uploaded_file:
    if st.button("✨ Générer les flashcards"):
        with st.spinner("Génération en cours..."):
            texte = extraire_texte(uploaded_file)
            flashcards = generer_flashcards(texte, nombre, model)
            st.session_state.flashcards = flashcards
            st.session_state.index = 0
            st.session_state.retournee = False

if "flashcards" in st.session_state:
    flashcards = st.session_state.flashcards
    index = st.session_state.index
    carte = flashcards[index]

    st.divider()
    st.markdown(f"**Carte {index + 1} / {len(flashcards)}**")

    st.markdown(f"### ❓ {carte['question']}")

    if st.button("👁️ Voir la réponse"):
        st.session_state.retournee = True

    if st.session_state.retournee:
        st.success(f"✅ {carte['reponse']}")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Précédent") and index > 0:
            st.session_state.index -= 1
            st.session_state.retournee = False
            st.rerun()
    with col2:
        if st.button("Suivant ➡️") and index < len(flashcards) - 1:
            st.session_state.index += 1
            st.session_state.retournee = False
            st.rerun()

    st.divider()
    if st.button("💾 Exporter en JSON"):
        json_str = json.dumps(flashcards, ensure_ascii=False, indent=2)
        st.download_button("📥 Télécharger", json_str, "flashcards.json", "application/json")