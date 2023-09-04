from textblob import TextBlob
from dataclasses import dataclass
import streamlit as st


@dataclass
class Mood:
    emoji: str
    sentiment: float


def get_mood(input_text: str, *, threshold: float) -> Mood:
    sentiment: float = TextBlob(input_text).sentiment.polarity

    if sentiment > threshold:
        return Mood("😄", sentiment)
    elif sentiment < -threshold:
        return Mood("😠", sentiment)
    else:
        return Mood("😐", sentiment)


def get_sentiment_label(sentiment: float) -> str:
    if sentiment > 0:
        return "positive"
    elif sentiment < 0:
        return "negative"
    else:
        return "neutral"


st.title("Sentiment Analysis Chatbot")

text = st.chat_input("Enter some text... ")

if text:
    try:
        mood: Mood = get_mood(text, threshold=0.05)
        sentiment_label = get_sentiment_label(mood.sentiment)
        mood_result = f"Sentiment: {sentiment_label} : {mood.emoji}"
        st.subheader(f"Result for: {text}")
        st.subheader(mood_result)
        st.subheader(f"Score: {mood.sentiment:.2f}")

    except Exception as e:
        st.write(f"An error occurred: {str(e)}")

hide_streamlit_style = """
                    <style>
                    # MainMenu {visibility: hidden;}
                    footer {visibility: hidden;}
                    footer:after {
                    content:''; 
                    visibility: visible;
    	            display: block;
    	            position: relative;
    	            # background-color: red;
    	            padding: 15px;
    	            top: 2px;
    	            }
                    </style>
                    """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
