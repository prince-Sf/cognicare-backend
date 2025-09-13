import openai

openai.api_key = "YOUR_OPENAI_API_KEY"


def generate_ai_response(conversation_history):
    # Craft system prompt that defines the caring, empathetic chatbot role
    system_prompt = (
        "You are Cognicare, an AI chatbot that supports youth mental wellness with empathy and care. "
        "Always respond in a caring, non-judgmental tone. "
        "When user is feeling down or stressed, express empathy, ask gentle follow-up questions like "
        "'What happened?', 'Would you like to talk more about it?', or 'How can I support you?'."
    )
    # Prepare messages for the chat completion endpoint
    messages = [{"role": "system", "content": system_prompt}] + conversation_history

    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=messages,
        temperature=0.7,
        max_tokens=150,
        n=1,
        stop=None,
    )
    return response.choices[0].message['content']


# Example usage
if __name__ == "__main__":
    chat_history = []
    print("🤖 Cognicare AI Chatbot: Here to support you 💙")
    while True:
        user_msg = input("You: ")
        if user_msg.lower() in ["exit", "quit"]:
            print("Cognicare: Take care, and remember you are not alone 💙")
            break
        chat_history.append({"role": "user", "content": user_msg})
        bot_reply = generate_ai_response(chat_history)
        print("Cognicare:", bot_reply)
        chat_history.append({"role": "assistant", "content": bot_reply})
