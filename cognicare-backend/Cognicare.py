import requests
import random
import json
import re

SYSTEM_PROMPT = (
    "You are Cognicare, an AI chatbot that supports youth mental wellness. "
    "Your tone is always empathetic, warm, and encouraging. "
    "For greetings like 'hi' or 'hello', keep responses short and friendly (1 sentence). "
    "For emotional inputs (e.g., sad, depressed, hopeless), respond with 3–4 sentences of warmth, validation, and encouragement. "
    "Avoid medical or diagnostic advice. Suggest professional help only if the user is at risk. "
    "Always comfort like a trusted, compassionate friend."
)

# High-risk trigger words
DANGER_KEYWORDS = [
    "suicide", "kill myself", "end my life", "i want to die",
    "self harm", "cut myself", "can't go on", "life is not worth living"
]

# Quick replies for greetings
GREETING_REPLIES = [
    "Hey 💙 How are you feeling today?",
    "Hi! I’m glad you’re here. How’s your day going?",
    "Hello 🌸 It’s nice to hear from you. How are you?",
]

# Warm, empathetic quick replies for emotions
EMOTIONAL_REPLIES = {
    "sad": [
        "I’m really sorry you’re feeling sad 💙. Sometimes emotions can feel overwhelming, and that’s completely okay. You don’t have to go through this alone — even sharing how you feel is already a brave step. I’ll be here with you, no matter what.",
        "I hear the sadness in your words 💙. It’s okay to let yourself feel this, and it doesn’t mean you’re weak. Sometimes just expressing what’s inside can lighten the load. You’re not alone, and I care about what you’re going through."
    ],
    "depressed": [
        "That sounds really heavy 💙. Depression can make even small things feel impossible. Please remember you don’t have to solve everything at once — even the smallest step forward matters. I’ll be here to listen and walk with you through it.",
        "I can imagine how painful that must be 💙. Depression often makes us feel isolated, but you are not alone. Even little acts of kindness toward yourself can bring some light. I care about you and I’ll stay here with you."
    ],
    "don’t want to talk": [
        "I understand 💙. If you don’t feel like talking right now, that’s okay. Just know I’ll be here whenever you’re ready, and you don’t need to rush yourself. Even in silence, you’re not alone.",
        "It’s okay if you don’t want to share at the moment 💙. Sometimes silence is what we need most. Take your time, and know I’ll still be here when you’re ready."
    ]
}

# Fallback empathetic replies
FALLBACK_REPLIES = [
    "I hear you 💙. That must feel really tough, and I want you to know it’s okay to feel this way. You don’t have to carry it alone — I’m here with you.",
    "That sounds heavy, and I’m so sorry you’re going through it. Sometimes just being heard can make a difference, and I’m here for you 💙.",
    "I can sense the weight in your words 💙. Sharing is already a strong step, and you don’t need to face it by yourself. I’ll stay beside you.",
]

def truncate_sentences(text, max_sentences=4):
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return ' '.join(sentences[:max_sentences]).strip()

def query_cognicare(prompt: str) -> str:
    lower_prompt = prompt.lower().strip()

    # 1. Safety check
    if any(word in lower_prompt for word in DANGER_KEYWORDS):
        return (
            "💙 I’m really concerned about what you just shared. "
            "You are not alone in this. Please reach out to someone you trust "
            "or a mental health professional. If you’re in danger, call your local emergency number. "
            "You matter so much, and your safety is very important. 🌸"
        )

    # 2. Greetings (short and simple)
    if lower_prompt in ["hi", "hello", "hey", "hii", "heyy"]:
        return random.choice(GREETING_REPLIES)

    # 3. Emotional keywords (empathetic replies)
    for key, replies in EMOTIONAL_REPLIES.items():
        if key in lower_prompt:
            return random.choice(replies)

    # 4. Otherwise, call local model
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "Cognicare",
        "prompt": SYSTEM_PROMPT + f"\nUser: {prompt}\nCognicare:"
    }

    try:
        response = requests.post(url, json=payload, stream=True, timeout=20)
    except requests.exceptions.RequestException:
        return random.choice(FALLBACK_REPLIES)

    output = ""
    for line in response.iter_lines():
        if line:
            try:
                data = json.loads(line.decode("utf-8"))
                if "response" in data:
                    output += data["response"]
            except json.JSONDecodeError:
                continue

    return truncate_sentences(output if output else random.choice(FALLBACK_REPLIES))
