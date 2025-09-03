import streamlit as st
from textblob import TextBlob
from nltk.corpus import wordnet
import nltk
from PIL import Image
from gtts import gTTS
import os

# Download WordNet
nltk.download('wordnet', quiet=True)

# -----------------------------
# Helper Functions
# -----------------------------
def get_antonyms(word):
    antonyms = []
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            if lemma.antonyms():
                antonyms.append(lemma.antonyms()[0].name())
    return antonyms

def make_positive_sentence(text):
    words = text.split()
    new_words = []
    for w in words:
        lw = w.lower().strip(".,!?")
        antonyms = get_antonyms(lw)
        if antonyms:
            new_words.append(antonyms[0])
        else:
            new_words.append(w)
    return " ".join(new_words)

def sentiment_analysis(text):
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0.1:
        return "POSITIVE", round(polarity*100, 2)
    elif polarity < -0.1:
        return "NEGATIVE", round(abs(polarity)*100, 2)
    else:
        return "NEUTRAL", 0

def speak_text(text):
    """Generate audio using gTTS and play in Streamlit"""
    try:
        tts = gTTS(text=text, lang='en')
        tts.save("temp.mp3")
        audio_file = open("temp.mp3", "rb")
        st.audio(audio_file.read(), format="audio/mp3")
        audio_file.close()
        os.remove("temp.mp3")
    except Exception as e:
        st.warning("🔊 Audio feedback not available in this environment.")

# -----------------------------
# Streamlit Page Config & Styling
# -----------------------------
st.set_page_config(page_title="Creative Sentiment Analyzer", page_icon="💬", layout="wide")

# Background image
def set_bg(png_file):
    st.markdown(
        f"""
        <style>
        .stApp {{
        background-image: url("data:image/png;base64,{open(png_file, "rb").read().encode("base64").decode()}");
        background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# If you have background image file
# set_bg("background.png")  # Uncomment if background image is available

st.markdown("""
<style>
body {
    background-color: #f0f8ff;
}
h1 {
    color: #ff4b4b;
}
.stButton>button {
    background-color: #4CAF50;
    color: white;
    height: 3em;
    width: 100%;
    font-size: 16px;
}
</style>
""", unsafe_allow_html=True)

st.title("💬 Creative Sentiment Analyzer")
st.markdown("Type your sentence and get instant sentiment analysis with **positive suggestions** and audio feedback!")

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.header("Settings")
show_positive_suggestion = st.sidebar.checkbox("Show Positive Suggestions", True)
enable_animations = st.sidebar.checkbox("Enable Fun Animations", True)
enable_audio = st.sidebar.checkbox("Enable Audio Feedback", True)

# -----------------------------
# Main Layout
# -----------------------------
col1, col2 = st.columns([1,1])

with col1:
    st.header("📝 Enter Text")
    user_input = st.text_area("Type your sentence here:", height=200)

with col2:
    st.header("📊 Sentiment Analysis")
    if st.button("Analyze") and user_input.strip():
        sentiment_label, score = sentiment_analysis(user_input)
        
        if sentiment_label == "POSITIVE":
            st.markdown(f"<div style='padding:10px; background-color:#d4edda; border-radius:10px'>😊 Positive ({score}%)</div>", unsafe_allow_html=True)
            if enable_audio:
                speak_text("Great! Your sentence is positive!")
            if enable_animations:
                st.balloons()
        elif sentiment_label == "NEGATIVE":
            st.markdown(f"<div style='padding:10px; background-color:#f8d7da; border-radius:10px'>😡 Negative ({score}%)</div>", unsafe_allow_html=True)
            if show_positive_suggestion:
                speak_text("Oop's! Your sentence is negative!")
                positive_version = make_positive_sentence(user_input)
                st.info("💡 Suggested Positive Version:")
                st.write(positive_version)
                if enable_audio:
                    speak_text(Your Suggested Positive Version: positive_version)
            if enable_animations:
                st.snow()
        else:
            st.markdown(f"<div style='padding:10px; background-color:#fff3cd; border-radius:10px'>😐 Neutral</div>", unsafe_allow_html=True)
            if enable_audio:
                speak_text("Your sentence is neutral.")
    else:
        st.warning("⚠️ Please enter some text first!")

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.markdown("© 2025 Creative Sentiment Analyzer | Built with Python & Streamlit 💻")
