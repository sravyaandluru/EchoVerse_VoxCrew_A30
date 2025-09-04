# app.py
import streamlit as st
import pyttsx3
import PyPDF2
import io
import tempfile
import os
import math

# -----------------------
# Page config
# -----------------------
st.set_page_config(page_title="EchoVerse", page_icon="🎧", layout="centered")

# -----------------------
# Sidebar
# -----------------------
st.sidebar.title("🎧 EchoVerse")
theme_choice = st.sidebar.radio("Theme", ["🌞 Light Mode", "🌙 Dark Mode"])
st.sidebar.markdown("---")
if st.sidebar.button("🧹 Reset Preview"):
    st.session_state.preview_text = ""
if st.sidebar.button("❌ Clear All"):
    st.session_state.clear()

# -----------------------
# Color palette for headers/buttons
# -----------------------
# Light mode
LIGHT_BG = "#f3ecda"  # Cream
LIGHT_TEXT = "#c4ac95"  # Khaki
LIGHT_ACCENT = "#94553d"  # Tan
LIGHT_SECONDARY = "#ffcba4"  # Peach
LIGHT_CARD = "#ffffff"  # Card background

# Dark mode (adapted for readability)
DARK_BG = "#2b1e14"  # dark brown
DARK_TEXT = "#f3ecda"  # cream
DARK_ACCENT = "#ffcba4"  # Peach
DARK_SECONDARY = "#94553d"  # Tan
DARK_CARD = "#3b2a1f"  # Card background

# Neutral colors for widgets (Preview, Voice, Speed) for readability in both modes
NEUTRAL_BG_LIGHT = "#fefefe"
NEUTRAL_BG_DARK = "#2f2f2f"
NEUTRAL_TEXT_LIGHT = "#333333"
NEUTRAL_TEXT_DARK = "#fefefe"

# -----------------------
# Theme assignment
# -----------------------
if theme_choice == "🌙 Dark Mode":
    bg_color = DARK_BG
    text_color = DARK_TEXT
    ACCENT_COLOR = DARK_ACCENT
    SECONDARY_ACCENT = DARK_SECONDARY
    card_bg = DARK_CARD
    widget_bg = NEUTRAL_BG_DARK
    widget_text_color = NEUTRAL_TEXT_DARK
else:
    bg_color = LIGHT_BG
    text_color = LIGHT_TEXT
    ACCENT_COLOR = LIGHT_ACCENT
    SECONDARY_ACCENT = LIGHT_SECONDARY
    card_bg = LIGHT_CARD
    widget_bg = NEUTRAL_BG_LIGHT
    widget_text_color = NEUTRAL_TEXT_LIGHT

# -----------------------
# Custom CSS
# -----------------------
st.markdown(f"""
<style>
.stApp {{
    background-color: {bg_color};
    color: {text_color};
    font-family: 'Segoe UI', Roboto, sans-serif;
}}
.section-title {{
    background: linear-gradient(45deg, {ACCENT_COLOR}, {SECONDARY_ACCENT});
    color: white;
    padding: 12px 18px;
    border-radius: 12px;
    font-size: 1.3rem;
    font-weight: bold;
    margin-top: 25px;
    margin-bottom: 10px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
}}
textarea[role="textbox"], .stTextInput > div > div > input {{
    background-color: {widget_bg} !important;
    color: {widget_text_color} !important;
    border-radius: 10px;
    padding: 12px;
}}
.stSelectbox {{
    background-color: {widget_bg} !important;
    color: {widget_text_color} !important;
}}
.stFileUploader, .stDownloadButton button {{
    background-color: {card_bg} !important;
    color: {widget_text_color} !important;
    border: 1px solid {ACCENT_COLOR} !important;
    border-radius: 10px !important;
}}
.stDownloadButton button:hover {{
    background: {ACCENT_COLOR} !important;
    color: white !important;
}}
</style>
""", unsafe_allow_html=True)

# -----------------------
# Hero Title
# -----------------------
st.markdown(f"""
<div style="text-align:center; margin-top:1rem; margin-bottom:1rem;">
    <h1 style="font-size:3rem; font-weight:bold; color:{ACCENT_COLOR};">✨ EchoVerse ✨</h1>
    <p style="font-size:1.2rem; color:{text_color}; opacity:0.9;">Turn PDFs & text into audiobooks 🎶</p>
</div>
""", unsafe_allow_html=True)

# -----------------------
# Upload PDF
# -----------------------
st.markdown('<div class="section-title">📂 Upload your PDF</div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload PDF (text-based)", type=["pdf"])
full_text, pdf_reader, num_pages = "", None, 0

if uploaded_file:
    try:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        num_pages = len(pdf_reader.pages)
        parts = [pdf_reader.pages[p].extract_text() for p in range(num_pages) if pdf_reader.pages[p].extract_text()]
        full_text = "\n".join(parts)
        st.success(f"✅ Loaded {num_pages} pages")
    except Exception as e:
        st.error(f"❌ Could not read PDF. Error: {e}")

# -----------------------
# Page selection
# -----------------------
if uploaded_file:
    st.markdown('<div class="section-title">📑 Select Pages</div>', unsafe_allow_html=True)
    cols = st.columns(3)
    start_page = cols[0].number_input("Start", min_value=1, max_value=max(1, num_pages), value=1)
    end_page = cols[1].number_input("End", min_value=1, max_value=max(1, num_pages), value=num_pages)
    load_preview = cols[2].button("Load into Preview")

    if "preview_text" not in st.session_state:
        st.session_state.preview_text = ""

    if load_preview:
        s, e = int(start_page) - 1, int(end_page)
        if s >= e:
            st.warning("⚠️ Start must be less than End")
        else:
            sel_parts = [pdf_reader.pages[p].extract_text() for p in range(s, e) if pdf_reader.pages[p].extract_text()]
            st.session_state.preview_text = "\n".join(sel_parts)
            st.success(f"Loaded pages {s+1} - {e}")

# -----------------------
# Editable Preview
# -----------------------
st.markdown('<div class="section-title">📝 Preview & Edit</div>', unsafe_allow_html=True)
if "preview_text" not in st.session_state or not st.session_state.preview_text:
    st.session_state.preview_text = full_text[:2000] + ("..." if len(full_text) > 2000 else "")

preview_text = st.text_area("Preview (editable)", value=st.session_state.preview_text, height=250)
st.session_state.preview_text = preview_text

# Show word count & estimated audio time
word_count = len(preview_text.split())
est_time_min = math.ceil(word_count / 150)
st.info(f"📝 Words: {word_count} | ⏱️ Estimated audio length: {est_time_min} min")

if word_count > 10000:
    st.warning("⚠️ Large text detected. Consider splitting into smaller parts.")

# -----------------------
# Voice & Speed
# -----------------------
st.markdown('<div class="section-title">🎙️ Voice & Speed</div>', unsafe_allow_html=True)
voice_option = st.selectbox("Voice", ["Male", "Female"])
speed = st.selectbox("Speed", ["0.5x Very Slow", "0.75x Slow", "1x Normal", "1.25x Fast", "1.5x Faster", "2x Turbo"])

# -----------------------
# Conversion Function
# -----------------------
def convert_text_to_mp3_bytes(text_to_convert: str):
    mp3_io = io.BytesIO()
    if not text_to_convert.strip():
        return None, "No text to convert."

    try:
        engine = pyttsx3.init()
        voices = engine.getProperty("voices")
        if voice_option == "Male" and len(voices) > 0:
            engine.setProperty("voice", voices[0].id)
        elif voice_option == "Female" and len(voices) > 1:
            engine.setProperty("voice", voices[1].id)

        multipliers = {"0.5x Very Slow": 0.5, "0.75x Slow": 0.75, "1x Normal": 1.0,
                       "1.25x Fast": 1.25, "1.5x Faster": 1.5, "2x Turbo": 2.0}
        new_rate = engine.getProperty("rate") * multipliers.get(speed, 1.0)
        engine.setProperty("rate", new_rate)

        tmp_path = os.path.join(tempfile.gettempdir(), "audiobook.mp3")
        engine.save_to_file(text_to_convert, tmp_path)
        engine.runAndWait()

        with open(tmp_path, "rb") as f:
            mp3_io.write(f.read())
        mp3_io.seek(0)

    except Exception as e:
        return None, f"Conversion failed: {e}"
    finally:
        if 'tmp_path' in locals() and os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except:
                pass

    return mp3_io, None

# -----------------------
# Convert Buttons
# -----------------------
st.markdown('<div class="section-title">🎧 Convert</div>', unsafe_allow_html=True)
cols = st.columns(2)

with cols[0]:
    if st.button("Convert Preview ✨"):
        with st.spinner("🎶 Generating audio..."):
            mp3_io, err = convert_text_to_mp3_bytes(st.session_state.preview_text)
            if err:
                st.error(err)
            else:
                st.success("Preview converted! 🎉")
                st.audio(mp3_io, format="audio/mp3")
                st.download_button(
                    "⬇ Download Preview",
                    data=mp3_io,
                    file_name="preview.mp3",
                    mime="audio/mp3"
                )

with cols[1]:
    if st.button("Convert Full 📚"):
        with st.spinner("🎶 Generating full audiobook..."):
            mp3_io, err = convert_text_to_mp3_bytes(full_text)
            if err:
                st.error(err)
            else:
                st.success("Full document converted! 🎉")
                st.audio(mp3_io, format="audio/mp3")
                st.download_button(
                    "⬇ Download Full",
                    data=mp3_io,
                    file_name="full.mp3",
                    mime="audio/mp3"
                )