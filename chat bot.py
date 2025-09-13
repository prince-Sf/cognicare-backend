import random
from transformers import pipeline
from textblob import TextBlob

# Load NLP Pipelines
sentiment_analyzer = pipeline("sentiment-analysis",model="distilbert/distilbert-base-uncased-finetuned-sst-2-english")

emotion_analyzer = pipeline("text-classification",
                            model="bhadresh-savani/distilbert-base-uncased-emotion")

# Distress keywords (expand as needed)
DISTRESS_KEYWORDS = ["suicide", "self-harm", "kill myself", "end it", "worthless", "no reason to live"]


def analyze_message(message):
    sentiment = sentiment_analyzer(message)[0]['label']
    emotion = emotion_analyzer(message)[0]['label']

    # Keyword distress check
    distress_detected = any(kw in message.lower() for kw in DISTRESS_KEYWORDS)

    return sentiment, emotion, distress_detected

def decide_response_type(sentiment, emotion, distress_detected):
    if distress_detected:
        return "crisis"
    elif sentiment in ["POSITIVE"] or emotion in ["joy", "love"]:
        return "positive"
    elif emotion in ["sadness", "fear", "anger", "anxiety"] or sentiment == "NEGATIVE":
        return "supportive"
    else:
        return "neutral"

def generate_response(message):
    sentiment, emotion, distress_detected = analyze_message(message)
    response_type = decide_response_type(sentiment, emotion, distress_detected)

    if response_type == "positive":
        responses = [
            "That’s amazing progress! Even small wins matter, and you should feel proud. 🌟",
            "I love how you’re moving forward—keep celebrating your journey!",
            "Your energy is inspiring, keep going with this positive vibe!"
        ]

    elif response_type == "supportive":
        responses = [
            "I hear you—it’s completely okay to feel like this. 💙 Want me to share a quick breathing exercise?",
            "That sounds tough. Remember, you don’t have to go through it alone.",
            "It’s okay to slow down and take care of yourself. Maybe a short walk or journaling could help."
        ]

    elif response_type == "crisis":
        responses = [
            "I’m really concerned about how you’re feeling. You’re not alone in this. Please consider reaching out to a trusted friend, counselor, or calling a crisis helpline immediately. 💙",
            "You are important and your life matters. If you’re in danger of harming yourself, please contact your local emergency number right now.",
            "I’m here with you. It may help to talk with someone trained to give you the right support—please reach out to a mental health professional or a helpline."
        ]

    else:
        responses = [
            "How has your day been so far? Anything on your mind?",
            "I’d love to hear more about what you’re thinking.",
            "I’m here to listen. What’s been on your mind today?"
        ]

    return random.choice(responses)

if __name__ == "__main__":
    print("🤖 Cognicare Chatbot: Supporting with empathy 🌸")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit", "exit"]:
            print("Cognicare: Take care of yourself 💙. Talk soon!")
            break
        bot_reply = generate_response(user_input)
        print("Cognicare:", bot_reply)
