import random
import re
from datetime import datetime

# 1. Rules: each rule is (regex pattern, list of possible replies)
RULES = [
    (r"\b(?:hi|hello|hey)\b",
     ["Hello! How can I help you?", "Hey there! What's on your mind?"]),
    (r"\bhow are you\b",
     ["I'm doing great, thanks for asking!", "All good! How about you?"]),
    (r"\bmy name is (?P<name>\w+)",
     ["Nice to meet you, {name}!", "Hello {name}, great to meet you!"]),
    (r"\b(?:time|clock)\b",
     ["The current time is {time}."]),
    (r"\b(?:date|day|today)\b",
     ["Today is {date}."]),
    (r"\b(?:joke|funny)\b",
     ["Why do programmers prefer dark mode? Because light attracts bugs!",
      "Why did the Python programmer wear glasses? Because he couldn't C!"]),
    (r"\b(?:thanks|thank you)\b",
     ["You're welcome!", "Happy to help!"]),
    (r"\b(?:bye|goodbye|exit|quit)\b",
     ["Goodbye! Have a great day!"]),
]

FALLBACKS = [
    "I'm not sure I understand. Could you rephrase that?",
    "Interesting! Tell me more.",
    "Sorry, I don't know how to answer that yet.",
]


def get_response(user_input, memory):
    """Find the first matching rule and build a reply."""
    text = user_input.lower().strip()

    for pattern, replies in RULES:
        match = re.search(pattern, text)
        if match:
            reply = random.choice(replies)

            # Remember the user's name (only the named group "name")
            groups = match.groupdict()
            if "name" in groups:
                groups["name"] = groups["name"].capitalize()
                memory["name"] = groups["name"]

            return reply.format(
                **groups,
                time=datetime.now().strftime("%I:%M %p"),
                date=datetime.now().strftime("%A, %d %B %Y"),
            )

    # No rule matched
    name = memory.get("name")
    fallback = random.choice(FALLBACKS)
    return f"{name}, {fallback}" if name else fallback


def main():
    memory = {}  # stores things like the user's name
    print("Bot: Hi! I'm PyBot. Type 'bye' to exit.")

    while True:
        user_input = input("You: ")
        if not user_input.strip():
            continue

        response = get_response(user_input, memory)
        print(f"Bot: {response}")

        if re.search(r"\b(bye|goodbye|exit|quit)\b", user_input.lower()):
            break


if __name__ == "__main__":
    main()
