import transformers
from transformers import pipeline
from dataclasses import dataclass

# Load a pre-trained sentiment analysis model
sentiment_analyzer = pipeline("sentiment-analysis")


@dataclass
class Mood:
    label: str
    score: float


def get_mood(input_text: str) -> Mood:
    results = sentiment_analyzer(input_text)

    # Extract the label and score from the model's output
    label = results[0]['label']
    score = results[0]['score']

    return Mood(label, score)


if __name__ == "__main__":
    while True:
        text: str = input("Enter some text (or type 'exit' to quit): ")

        # Allow the user to exit the loop
        if text.lower() == 'exit':
            break

        try:
            mood: Mood = get_mood(text)
            print(f"Sentiment: {mood.label} (Score: {mood.score:.2f})")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
