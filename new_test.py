import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from dataclasses import dataclass

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


if __name__ == "__main__":
    while True:
        text: str = input("Enter some text (or type 'exit' to quit): ")

        if text.lower() == 'exit':
            break

        try:
            mood: Mood = get_mood(text)
            print(f"Mood: {mood.emoji} ({mood.sentiment.capitalize()})")
            print(f"Score: {mood.score:.2f}")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
