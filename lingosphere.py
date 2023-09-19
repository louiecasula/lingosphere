from helpers import clear_screen, color, highlight
from login import signup, login, logout, user_exists
from gtts import gTTS
from playsound import playsound
import re, sys, csv, os, random, hashlib

# Files:
USERS_FILE = "users.csv"
LEVELS = {"1": "words1.csv", "2": "words2.csv", "3": "words3.csv"}
AUDIO_FILE = "pronunciation.mp3"
ARCHIVES_FILE = "archives.csv"
# Messages:
    # Startup:
WELCOME_MESSAGE = "~~~~~~~~~~ Welcome to Lingosphere ~~~~~~~~~~~"


def main():
    if os.path.exists(AUDIO_FILE):
        os.remove(AUDIO_FILE)
    main_menu()


def main_menu():
    while True:
        print(WELCOME_MESSAGE)
        print("[1] Signup")
        print("[2] Login")
        print("[3] Exit")
        selection = input("Select an option: ")
        if selection in MAIN_MENU:
            clear_screen()
            MAIN_MENU[selection]()
        else:
            print("\nNot an option, try again.")


def wotd_menu():
    clear_screen()
    print(f"\nWelcome back, {current_user['username']}!")
    global todays_word
    todays_word = wotd()
    if not os.path.exists(AUDIO_FILE):
        save_sound()
    while True:
        print("Today's word is: " + color.BOLD + color.UNDERLINE + f"{todays_word['Word']}\n" + color.END)
        print("[1] Add to Favorites")
        print("[2] Learn more")
        print("[3] Exit")
        selection = input("Select an option: ")
        if selection in WOTD_MENU and selection != "1":
            clear_screen()
            WOTD_MENU[selection]()
        elif selection == "1":
            WOTD_MENU[selection](todays_word)
        else:
            print("\nNot an option, try again.")


def wotd():
    user_level = current_user["level"]
    with open(LEVELS[user_level], "r", encoding="utf8") as f:
        reader = csv.DictReader(f)
        todays_word = random.choice(list(reader))
    return todays_word


# def favorites_menu:
#     clear_screen()
#     print(f"\nWelcome back, {current_user['username']}!")
#     global todays_word
#     todays_word = wotd()
#     if not os.path.exists(AUDIO_FILE):
#         save_sound()
#     while True:
#         print("Today's word is: " + color.BOLD + color.UNDERLINE + f"{todays_word['Word']}\n" + color.END)
#         print("[1] Add to Favorites")
#         print("[2] Learn more")
#         print("[3] Exit")
#         selection = input("Select an option: ")
#         if selection in WOTD_MENU and selection != "1":
#             clear_screen()
#             WOTD_MENU[selection]()
#         elif selection == "1":
#             WOTD_MENU[selection](todays_word)
#         else:
#             print("\nNot an option, try again.")


def add_favorite(word):
    if os.path.exists(FAVORITES_FILE) and os.stat(FAVORITES_FILE).st_size > 0:
        with open(FAVORITES_FILE, "r", encoding="utf8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if word['Word'] == row['Word']:
                    return f"{word['Word']} is already in your favorites!"
    with open(FAVORITES_FILE, "a", encoding='utf8') as f:
        writer = csv.DictWriter(f, fieldnames=["Date","Word","Part of Speech","Definition","Pronunciation","Example", "Origin"])
        if os.stat(USERS_FILE).st_size == 0:
            writer.writeheader()
        writer.writerow({"Date": "TODAY","Word": word['Word'],"Part of Speech": word['Part of Speech'],"Definition": word['Definition'],"Pronunciation": word['Pronunciation'],"Example": word['Example'], "Origin": word['Origin']})
    print(f"*** {word['Word']} has been added to favorites! ***")


def remove_favorite(word):
    print(f"*** {word['Word']} has been removed to favorites. ***")


def learn_more():
    clear_screen()
    print("\nWhat would you like to know about " + color.BOLD + color.UNDERLINE + f"{todays_word['Word']}" + color.END + "?\n")
    while True:
        print("[1] Definition")
        print("[2] Example sentence")
        print("[3] Pronunciation")
        print("[4] Return to menu")
        selection = input("Select an option: ")
        if selection in LEARN_MENU:
            clear_screen()
            LEARN_MENU[selection]()
        else:
            print("\nNot an option, try again.")


def definition():
    print(f"{todays_word['Word']}: ({todays_word['Part of Speech']}) {todays_word['Definition']} {todays_word['Origin']}")
    input("\nPress enter to return...")
    learn_more()


def example():
    highlight(todays_word['Word'], todays_word['Example'])
    input("\nPress enter to return...")
    learn_more()


def pronunciation():
    while True:
        clear_screen()
        print(f"{todays_word['Pronunciation']}")
        playsound(AUDIO_FILE)
        choice = input("\nPress any key and enter to replay, \nPress only enter to return\n")
        if re.match(r'.+', choice):
            pass
        else:
            break
    learn_more()


def save_sound():
    text = todays_word['Word']
    audio = gTTS(text=text, lang='en', slow=False)
    audio.save(AUDIO_FILE)


def sign_in():
    global current_user
    current_user = login()
    global FAVORITES_FILE
    FAVORITES_FILE = f"{current_user['username']}_favorites.csv"
    wotd_menu()


def admin():
    global current_user
    current_user = {"username": "ADMIN", "level": "1"}
    global FAVORITES_FILE
    FAVORITES_FILE = f"{current_user['username']}_favorites.csv"
    wotd_menu()

# Menus:
MAIN_MENU = {"1": signup, "2": sign_in, "3": logout, "4": admin}
WOTD_MENU = {"1": add_favorite, "2": learn_more, "3": logout}
FAVORITE_MENU = {"1": definition, "2": example, "3": pronunciation, "4": wotd_menu, "5": remove_favorite}
LEARN_MENU = {"1": definition, "2": example, "3": pronunciation, "4": wotd_menu}


if __name__ == "__main__":
    clear_screen()
    main()
