def generate_response(emotion, user_input=None, order_stage=None):
    
    greeting_responses = {
        "hello": "Hello! How can I assist you today?",
        "hi": "Hi there! What would you like to eat?",
        "hey": "Hey! How's your day going?",
        "good morning": "Good morning! What can I get for you?",
        "good afternoon": "Good afternoon! Ready for a meal?",
        "good evening": "Good evening! Hungry for something delicious?"
    }

    emotion_responses = {
        "sadness": "I’m really sorry to hear that. A warm meal and something sweet might help cheer you up.",
        "anger": "I'm really sorry you're feeling this way. A comforting meal might help. Here’s something warm and satisfying for you.",
        "love": "That’s so wonderful! Love and good food always go together. How about something delightful to celebrate?",
        "surprise": "Oh wow! Something unexpected? Let's go for a unique and exciting dish!",
        "joy": "I love hearing that! A delicious treat can make your day even better.",
        "fear": "That sounds tough. Maybe a warm meal and a relaxing drink can help ease your mind."
    }

    menu_suggestions = {
        "sadness": ["Hot chocolate", "Warm cookies", "Pancakes"],
        "anger": ["Comforting soup", "Spicy wings", "Cheesy pizza"],
        "love": ["Strawberry cheesecake", "Chocolate-dipped strawberries", "Romantic candlelight dinner"],
        "surprise": ["Chef’s mystery dish", "Exotic fusion platter", "Surprise dessert"],
        "joy": ["Chocolate lava cake", "Ice cream sundae", "Fruit smoothie"],
        "fear": ["Herbal tea", "Light soup", "Calming chamomile drink"]
    }

    if user_input and user_input.lower() in greeting_responses:
        return greeting_responses[user_input.lower()]
    
    if order_stage == "confirm_more":
        if user_input.lower() in ["yes", "sure", "why not"]:
            return "Great! What else would you like to add?"
        elif user_input.lower() in ["no", "that's all", "i'm done"]:
            return "Order placed! Your food will be ready soon. Enjoy!"
        else:
            return "I didn't quite get that. Do you want to add more items to your order?"

    if emotion in emotion_responses:
        response = emotion_responses[emotion]
        menu = menu_suggestions[emotion]
    else:
        response = "I'm not sure what to say, but I'm here to help with food suggestions."
        menu = ["Chef’s special", "A surprise dish!"]

    #response += f" Here are some recommendations: {', '.join(menu)}."


    return f"{response} Here’s a perfect menu for you: {', '.join(menu)}. What would you like to order?"
