# interface.py

import streamlit as st
from main import run_pipeline
import whisper   # for voice-to-text (OpenAI Whisper)
import numpy as np

st.set_page_config(page_title="AI Creative Partner", layout="wide")
st.title("AI Creative Partner 🤖🎨🚀")

# Input method: text or voice
mode = st.radio("Input Mode", ["Text", "Voice"])
if mode == "Text":
    user_input = st.text_input("Enter your creative prompt:")
else:
    st.write("Click below and speak your prompt:")
    audio_data = st.audio_input("🎤 Record your prompt")
    if audio_data:
        # Convert audio bytes to text via Whisper
        with open("temp.wav", "wb") as f:
            f.write(audio_data)
        model = whisper.load_model("base")
        res = model.transcribe("temp.wav")
        user_input = res["text"]
        st.write("Interpreted prompt:", user_input)
    else:
        user_input = ""

if user_input:
    # Display a running indicator
    with st.spinner("Generating..."):
        img_path, model_path = run_pipeline(user_input)
    # Show outputs
    st.subheader("Generated Image")
    st.image(img_path, use_column_width=True)
    st.subheader("Generated 3D Model")
    st.write(f"3D model saved to `{model_path}` (OBJ format).")
    st.success("Generation complete! Prompt stored in memory.")

    # Memory retrieval demo (similar past prompts)
    st.subheader("Similar Past Creations")
    sims = retrieve_similar(user_input, k=3) # type: ignore
    for sim in sims:
        st.markdown(f"- **Prompt:** {sim['prompt']}")
        st.image(sim['image_path'], width=200, caption="Previous image")

