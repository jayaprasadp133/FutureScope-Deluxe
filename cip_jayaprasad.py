import os
import requests
from datetime import datetime

# Optional color styling
try:
    from colorama import Fore, Style, init
    init(autoreset=True)
    COLOR = True
except ImportError:
    COLOR = False

# Your OpenRouter API key (keep secret)
API_KEY = "your_api_key"
HISTORY_FILE = "history.txt"

def color_text(text, color):
    if not COLOR:
        return text
    return f"{color}{text}{Style.RESET_ALL}"

def print_banner():
    banner = """
    ********************************************
    *                                          *
    *     🔮 Welcome to FutureScope Deluxe 🔮   *
    *                                          *
    ********************************************
    """
    print(color_text(banner, Fore.CYAN))

def get_user_info():
    print(color_text("\nAnswer these questions to unlock your future ✨\n", Fore.YELLOW))
    name = input("1. What is your name? ")
    mood = input("2. How are you feeling today (1 word)? ")
    favorite_food = input("3. What is your favorite food? ")
    dream_job = input("4. What job did you dream of as a kid? ")
    animal = input("5. If you were an animal, what would you be? ")
    secret_word = input("6. Say a random word that comes to mind: ")
    goal = input("7. What's one goal you'd like to achieve? ")

    return {
        "name": name.strip(),
        "mood": mood.strip(),
        "food": favorite_food.strip(),
        "job": dream_job.strip(),
        "animal": animal.strip(),
        "word": secret_word.strip(),
        "goal": goal.strip()
    }

def create_prompt(user_data):
    return f"""
    The user gave the following answers:
    - Name: {user_data['name']}
    - Mood: {user_data['mood']}
    - Favorite Food: {user_data['food']}
    - Childhood Dream Job: {user_data['job']}
    - Spirit Animal: {user_data['animal']}
    - Random Word: {user_data['word']}
    - Personal Goal: {user_data['goal']}

    Based on these answers, write a fun, creative, and fictional prediction of their future.
    Make it magical, funny, and slightly mysterious. This is for entertainment only.
    """

def ask_openrouter(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://yourdomain.com",  # optional, can be your GitHub repo or website
        "X-Title": "FutureScope-Deluxe"
    }

    payload = {
        "model": "openai/gpt-3.5-turbo",  # or try "anthropic/claude-3-haiku"
        "messages": [
            {"role": "system", "content": "You are a mystical AI fortune teller who gives fun, fictional, and creative future predictions."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.9,
        "max_tokens": 300
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"❌ Error generating prediction:\n\n{e}"

def save_to_history(name, story):
    with open(HISTORY_FILE, "a", encoding='utf-8') as file:
        file.write(f"\n{'='*50}\n")
        file.write(f"Name: {name}\nDate: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n{story}\n")

def show_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding='utf-8') as file:
            print(color_text("\n🕰️ Previous Predictions:\n", Fore.MAGENTA))
            print(file.read())
    else:
        print(color_text("\nNo history found yet.\n", Fore.RED))

def main_menu():
    while True:
        print(color_text("\nMain Menu:", Fore.GREEN))
        print("1. Get your fun AI fortune")
        print("2. View past predictions")
        print("3. Exit")

        choice = input("Choose an option (1-3): ").strip()
        if choice == "1":
            user_data = get_user_info()
            prompt = create_prompt(user_data)
            print(color_text("\n🔍 Consulting the AI oracle...\n", Fore.BLUE))
            story = ask_openrouter(prompt)
            print(color_text("\n🔮 Here's your AI-generated future:\n", Fore.CYAN))
            print(story)
            save_to_history(user_data['name'], story)
        elif choice == "2":
            show_history()
        elif choice == "3":
            print(color_text("\n👋 Thank you for using FutureScope Deluxe! Stay curious!\n", Fore.YELLOW))
            break
        else:
            print(color_text("❌ Invalid choice. Try again.", Fore.RED))

if __name__ == "__main__":
    print_banner()
    main_menu()
