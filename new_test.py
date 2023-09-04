import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from dataclasses import dataclass
import streamlit as st

nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()

SENTIMENT_EMOJI_MAP = {
    'positive': '😄',
    'negative': '😠',
    'neutral': '😐'
}


@dataclass
class Mood:
    emoji: str
    sentiment: str
    score: float


def get_mood(input_text: str) -> Mood:
    sentiment_scores = sia.polarity_scores(input_text)

    sentiment_score = sentiment_scores['compound']
    if sentiment_score >= 0.05:
        sentiment = 'positive'
    elif sentiment_score <= -0.05:
        sentiment = 'negative'
    else:
        sentiment = 'neutral'

    emoji = SENTIMENT_EMOJI_MAP[sentiment]
    return Mood(emoji, sentiment, sentiment_score)


st.title("Sentiment Analysis Chatbot")

text = st.chat_input("Enter some text... ")

if text:
    try:
        mood: Mood = get_mood(text)
        mood_result = f"Mood: {mood.emoji} : {mood.sentiment.capitalize()}"
        score_result = f"Score: {mood.score:.3f}"
        st.subheader(f"Result for: {text}")
        st.subheader(mood_result)
        st.subheader(score_result)

    except Exception as e:
        st.write(f"An error occurred: {str(e)}")
