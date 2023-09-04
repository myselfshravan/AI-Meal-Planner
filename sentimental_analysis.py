from textblob import TextBlob
from dataclasses import dataclass


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


if __name__ == "__main__":
    while True:
        text: str = input("Enter some text: ")
        mood: Mood = get_mood(text, threshold=0.3)

        print(f"Mood: {mood.emoji} ({mood.sentiment})")
