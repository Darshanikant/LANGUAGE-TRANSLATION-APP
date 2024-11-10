# Import necessary libraries
import streamlit as st
from deep_translator import GoogleTranslator  # Use GoogleTranslator from deep-translator
import pandas as pd
from gtts import gTTS  # Google Text-to-Speech
import base64
import os

# Load the language dataset
data = pd.read_csv("language.csv")  # Make sure language.csv is in the same directory
data.dropna(inplace=True)
lang = data['name'].to_list()
langlist = tuple(lang)
langcode = data['iso'].to_list()

# Map language names to their codes
lang_array = {lang[i]: langcode[i] for i in range(len(langcode))}

# Frontend layout
st.title("Language Translation App")

# App description
st.write(""" ### Language Interpretation App

This app provides real-time language translation to help users communicate across different languages. 
It detects the input language and translates text into the selected target language, making it ideal for 
multilingual communication, cross-cultural interaction, and understanding content in various languages. """)

# Input text area
inputtext = st.text_area("Write Your Text", height=100)
options = list(langlist)
selected_option = st.selectbox("Select Language to Translate:", options)

# Supported speech languages for gTTS
speech_langs = {
    "af": "Afrikaans",
    "ar": "Arabic",
    "bg": "Bulgarian",
    "bn": "Bengali",
    "bs": "Bosnian",
    "ca": "Catalan",
    "cs": "Czech",
    "cy": "Welsh",
    "da": "Danish",
    "de": "German",
    "el": "Greek",
    "en": "English",
    "eo": "Esperanto",
    "es": "Spanish",
    "et": "Estonian",
    "fi": "Finnish",
    "fr": "French",
    "gu": "Gujarati",
    "hi": "Hindi",
    "hr": "Croatian",
    "hu": "Hungarian",
    "id": "Indonesian",
    "is": "Icelandic",
    "it": "Italian",
    "ja": "Japanese",
    "jw": "Javanese",
    "km": "Khmer",
    "kn": "Kannada",
    "ko": "Korean",
    "la": "Latin",
    "lv": "Latvian",
    "mk": "Macedonian",
    "ml": "Malayalam",
    "mr": "Marathi",
    "my": "Myanmar (Burmese)",
    "ne": "Nepali",
    "nl": "Dutch",
    "no": "Norwegian",
    "pl": "Polish",
    "pt": "Portuguese",
    "ro": "Romanian",
    "ru": "Russian",
    "si": "Sinhala",
    "sk": "Slovak",
    "sq": "Albanian",
    "sr": "Serbian",
    "su": "Sundanese",
    "sv": "Swedish",
    "sw": "Swahili",
    "ta": "Tamil",
    "te": "Telugu",
    "th": "Thai",
    "tl": "Filipino",
    "tr": "Turkish",
    "uk": "Ukrainian",
    "ur": "Urdu",
    "vi": "Vietnamese",
    "zh-CN": "Chinese"
}

# Translation and Text-to-Speech Conversion
if st.button("Convert"):
    # Function to create download link for audio file
    def get_binary_file_downloader_html(bin_file, file_label='File'):
        with open(bin_file, 'rb') as f:
            df = f.read()
        bin_str = base64.b64encode(df).decode()
        href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Download {file_label}</a>'
        return href

    c1, c2 = st.columns([4, 3])

    # I/O operations
    if len(inputtext) > 0:
        try:
            # Perform translation using deep-translator
            target_lang_code = lang_array[selected_option]
            output = GoogleTranslator(source='auto', target=target_lang_code).translate(inputtext)

            # Display translated text
            with c1:
                st.text_area("TRANSLATED TEXT", output, height=200)

            # If speech support is available, create audio file
            if target_lang_code in speech_langs:
                with c2:
                    aud_file = gTTS(text=output, lang=target_lang_code, slow=False)
                    aud_file.save("lang.mp3")
                    with open("lang.mp3", "rb") as audio_file:
                        audio_bytes = audio_file.read()
                    st.audio(audio_bytes, format='audio/mp3')
                    st.markdown(get_binary_file_downloader_html("lang.mp3", 'Audio File'), unsafe_allow_html=True)
        except Exception as e:
            st.error(f"An error occurred: {e}")

# Footer
st.markdown("""
    ---
    &copy; 2024 Created By Darshanikanta. No copyright
""")
