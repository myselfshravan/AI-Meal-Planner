from textblob import TextBlob
from dataclasses import dataclass
import streamlit as st


@dataclass
class Mood:
    emoji: str
    sentiment: float


def get_mood(input_text: str, *, threshold: float) -> Mood:
    sentiment: float = TextBlob(input_text).sentiment.polarity

    friendly_threshold: float = threshold
    hostile_threshold: float = -threshold

    if sentiment >= friendly_threshold:
        return Mood("😄", sentiment)
    elif sentiment <= hostile_threshold:
        return Mood("😠", sentiment)
    else:
        return Mood("😐", sentiment)


st.title("Sentiment Analysis Chatbot")

text = st.chat_input("Enter some text... ")

if text:
    try:
        mood: Mood = get_mood(text, threshold=0.05)
        mood_result = f"Mood: {mood.emoji} : {mood.sentiment:.2f}"
        st.subheader(f"Result for: {text}")
        st.subheader(mood_result)

    except Exception as e:
        st.write(f"An error occurred: {str(e)}")
