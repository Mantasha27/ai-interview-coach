import speech_recognition as sr
from gtts import gTTS
import tempfile
import streamlit as st
import os

recognizer = sr.Recognizer()

def speak_text(text):
    """
    Convert text to speech using Google Text-to-Speech
    Displays audio player in Streamlit
    """
    try:
        tts = gTTS(text)
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(tmp.name)
        st.audio(tmp.name, format="audio/mp3")
        # Clean up temp file after a delay
        try:
            os.remove(tmp.name)
        except:
            pass
    except Exception as e:
        st.error(f"Error generating speech: {e}")


def recognize_speech_with_retry(audio_data, max_retries=3):
    """
    Enhanced speech recognition with retry logic
    
    Args:
        audio_data: Audio data to recognize
        max_retries: Number of retry attempts
        
    Returns:
        str: Recognized text or None if failed
    """
    recognizer = sr.Recognizer()
    
    for attempt in range(max_retries):
        try:
            text = recognizer.recognize_google(audio_data)
            return text
        except sr.UnknownValueError:
            if attempt < max_retries - 1:
                st.warning(f"⚠️ Audio unclear. Retry {attempt + 1}/{max_retries}")
            else:
                st.error("❌ Could not understand audio after 3 attempts")
                return None
        except sr.RequestError as e:
            st.error(f"❌ Speech Recognition Service Error: {e}")
            return None
        except Exception as e:
            st.error(f"❌ Unexpected error: {e}")
            return None


def start_recording():
    """
    Start recording audio from microphone
    Stores recognizer and microphone in session state
    """
    try:
        st.session_state.recognizer = sr.Recognizer()
        st.session_state.mic = sr.Microphone()

        with st.session_state.mic as source:
            st.session_state.recognizer.adjust_for_ambient_noise(source)
            st.session_state.audio = st.session_state.recognizer.listen(source, timeout=30)
        
        st.success("✅ Recording completed")
    except Exception as e:
        st.error(f"❌ Error during recording: {e}")


def stop_recording():
    """
    Stop recording and convert audio to text
    
    Returns:
        str: Recognized text or error message
    """
    try:
        if 'audio' not in st.session_state:
            return "No audio recorded"
        
        text = st.session_state.recognizer.recognize_google(
            st.session_state.audio
        )
        return text
    except sr.UnknownValueValue:
        return "Could not understand audio. Please speak clearly."
    except sr.RequestError as e:
        return f"Speech Recognition Service Error: {e}"
    except Exception as e:
        return f"Error: {e}"
