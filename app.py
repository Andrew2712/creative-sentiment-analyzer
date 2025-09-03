import streamlit as st
from textblob import TextBlob
from nltk.corpus import wordnet
import nltk
import pyttsx3

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
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# -----------------------------
# Streamlit Page Config
# -----------------------------
st.set_page_config(page_title="Creative Sentiment Analyzer", page_icon="💬", layout="wide")

# -----------------------------
# Sidebar: Theme & Settings
# -----------------------------
st.sidebar.header("Settings")
show_positive_suggestion = st.sidebar.checkbox("Show Positive Suggestions", True)
enable_animations = st.sidebar.checkbox("Enable Fun Animations", True)
theme_choice = st.sidebar.radio("Theme", ["Light", "Dark"])

# -----------------------------
# Theme CSS
# -----------------------------
if theme_choice == "Dark":
    gradient_bg = "linear-gradient(to bottom right, #1e1e1e, #333333);"
    card_bg = "#333333"
    text_color = "white"
    positive_bg = "#145214"
    negative_bg = "#7a1414"
    neutral_bg = "#665c00"
else:
    gradient_bg = "linear-gradient(to bottom right, #f0f8ff, #cce7ff);"
    card_bg = "#f0f8ff"
    text_color = "black"
    positive_bg = "#d4edda"
    negative_bg = "#f8d7da"
    neutral_bg = "#fff3cd"

st.markdown(f"""
<style>
body {{
    background: {gradient_bg};
    color: {text_color};
}}
.stButton>button {{
    background-color: #4CAF50;
    color: white;
    height: 3em;
    width: 100%;
    font-size: 16px;
}}
div.stTextArea>div>textarea {{
    background-color: {card_bg};
    color: {text_color};
}}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# App Title
# -----------------------------
st.title("💬 Creative Sentiment Analyzer")
st.markdown("Type your sentence and get instant sentiment analysis with **positive suggestions** and audio feedback!")

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
            st.markdown(f"<div style='padding:10px; background-color:{positive_bg}; border-radius:10px'>😊 Positive ({score}%)</div>", unsafe_allow_html=True)
            response_text = "Great! Keep it up!"
            st.info(f"💬 Response: {response_text}")
            speak_text(response_text)  # Audio feedback for positive text
            if enable_animations:
                st.balloons()

        elif sentiment_label == "NEGATIVE":
            st.markdown(f"<div style='padding:10px; background-color:{negative_bg}; border-radius:10px'>😡 Negative ({score}%)</div>", unsafe_allow_html=True)
            if show_positive_suggestion:
                positive_version = make_positive_sentence(user_input)
                st.info("💡 Suggested Positive Version:")
                st.write(positive_version)
                speak_text(positive_version)  # Audio feedback for positive suggestion
            if enable_animations:
                st.snow()

        else:
            st.markdown(f"<div style='padding:10px; background-color:{neutral_bg}; border-radius:10px'>😐 Neutral</div>", unsafe_allow_html=True)
    else:
        st.warning("⚠️ Please enter some text first!")

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.markdown("© 2025 Creative Sentiment Analyzer | Built with Python & Streamlit 💻")
