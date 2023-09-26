from helpers import clear_screen, color, highlight
from login import signup, login, logout, user_exists
from csv_pruner import format, present, remove, word_exists, set_word, today_exists, set_today, generate_wordpool, remove_from_pool
from gtts import gTTS
from playsound import playsound
from datetime import date
import re, sys, csv, os, random, hashlib, time


# Files:
USERS_FILE = "users.csv"
LEVELS = {"1": "words1.csv", "2": "words2.csv", "3": "words3.csv"}
TODAY_AUDIO = "today.mp3"
CURRENT_AUDIO = "current.mp3"
ARCHIVES_FILE = "archives.csv"
# Messages:
    # Startup:
WELCOME_MESSAGE = "~~~~~~~~~~ Welcome to Lingosphere ~~~~~~~~~~~"


def main():
    main_menu()


def main_menu():
    clear_screen()
    global current_menu
    current_menu = MAIN_MENU
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
            time.sleep(1)
            main_menu()


def wotd():
    user_level = current_user["level"]
    global today
    today = str(date.today())
    global todays_word
    if today_exists(today, ARCHIVES_FILE):
        todays_word = set_today(today, ARCHIVES_FILE)
    else:
        with open(POOL_FILE, "r", encoding="utf8") as f:
            reader = csv.DictReader(f)
            todays_word = random.choice(list(reader))
            remove_from_pool(todays_word, POOL_FILE)
            format(POOL_FILE)
        with open(ARCHIVES_FILE, "a", encoding="utf8", newline='') as f:
            fieldnames = ["Date", "Word", "Part of Speech", "Definition", "Pronunciation", "Example",
                          "Origin"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            if os.stat(ARCHIVES_FILE).st_size == 0:
                writer.writeheader()
            writer.writerow({"Date": today, "Word": todays_word["Word"], "Part of Speech": todays_word["Part of Speech"], "Definition": todays_word["Definition"], "Pronunciation": todays_word["Pronunciation"], "Example": todays_word["Example"], "Origin": todays_word["Origin"]})
        format(ARCHIVES_FILE)
    if os.path.exists(TODAY_AUDIO):
        os.remove(TODAY_AUDIO)
    save_sound(todays_word,TODAY_AUDIO)


def wotd_menu():
    clear_screen()
    global current_menu
    current_menu = WOTD_MENU
    print(f"Welcome back, {current_user['username']}!")
    while True:
        print("Today's word is: " + color.BOLD + color.UNDERLINE + f"{todays_word['Word']}\n" + color.END)
        print("[1] Add to Favorites")
        print("[2] Learn more")
        print("[3] Go to Favorites")
        print("[4] Exit")
        selection = input("Select an option: ")
        if selection in WOTD_MENU and selection != "1":
            clear_screen()
            WOTD_MENU[selection]()
        elif selection == "1":
            WOTD_MENU[selection](todays_word)
        else:
            print("\nNot an option, try again.")
            time.sleep(1)
            wotd_menu()


def favorites_list():
    clear_screen()
    global current_menu
    current_menu = FAVORITES_MENU
    if os.path.exists(FAVORITES_FILE) and os.stat(FAVORITES_FILE).st_size > 0:
        present(FAVORITES_FILE)
        while True:
            choice = input("Enter a word to learn more or just hit enter to return: ")
            if choice == "":
                wotd_menu()
            elif word_exists(choice, FAVORITES_FILE):
                global current_word
                current_word = set_word(choice, FAVORITES_FILE)
                if os.path.exists(CURRENT_AUDIO):
                    os.remove(CURRENT_AUDIO)
                save_sound(current_word, CURRENT_AUDIO)
                favorites_menu()
                break
            else:
                print("That word isn't in your Favorites")
    else:
        print("You haven't favorited any words yet!")
        input("Press enter to continue")
        wotd_menu()


def favorites_menu():
    clear_screen()
    while True:
        print(f"What would you like know about {current_word['Word']}?")
        print("[1] Definition")
        print("[2] Example sentence")
        print("[3] Pronunciation")
        print("[4] Remove from favorites")
        print("[5] Return to menu")
        selection = input("Select an option: ")
        if selection in FAVORITES_MENU and selection != "3" and selection != "5":
            clear_screen()
            FAVORITES_MENU[selection](current_word)
        elif selection == "3":
            clear_screen()
            FAVORITES_MENU[selection](current_word, CURRENT_AUDIO)
        elif selection == "5":
            clear_screen()
            FAVORITES_MENU[selection]()
        else:
            print("\nNot an option, try again.")
            time.sleep(1)
            favorites_menu()


def add_favorite(word):
    clear_screen()
    if word_exists(word['Word'], FAVORITES_FILE):
        print(f"{word['Word']} is already in your favorites!")
        return
    with open(FAVORITES_FILE, "a", encoding='utf8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["Date","Word","Part of Speech","Definition","Pronunciation","Example", "Origin"])
        if os.stat(FAVORITES_FILE).st_size == 0:
            writer.writeheader()
        writer.writerow({"Date": today,"Word": word['Word'],"Part of Speech": word['Part of Speech'],"Definition": word['Definition'],"Pronunciation": word['Pronunciation'],"Example": word['Example'], "Origin": word['Origin']})
    format(FAVORITES_FILE)
    print(f"*** {word['Word']} has been added to favorites! ***")


def remove_favorite(word):
    clear_screen()
    remove(word, FAVORITES_FILE)
    format(FAVORITES_FILE)
    print(f"*** {word['Word']} has been removed to favorites. ***")
    favorites_menu()


def learn_more():
    clear_screen()
    global current_menu
    current_menu = LEARN_MENU
    print("What would you like to know about " + color.BOLD + color.UNDERLINE + f"{todays_word['Word']}" + color.END + "?\n")
    while True:
        print("[1] Definition")
        print("[2] Example sentence")
        print("[3] Pronunciation")
        print("[4] Return to menu")
        selection = input("Select an option: ")
        if selection in LEARN_MENU and selection != "3" and selection != "4":
            clear_screen()
            LEARN_MENU[selection](todays_word)
        elif selection == "3":
            clear_screen()
            LEARN_MENU[selection](todays_word, TODAY_AUDIO)
        elif selection == "4":
            clear_screen()
            LEARN_MENU[selection]()
        else:
            print("\nNot an option, try again.")
            time.sleep(1)
            learn_more()


def definition(word):
    print(color.BOLD + f"{word['Word']} " + color.END + f"({word['Part of Speech'].lower()}): {word['Definition']} {word['Origin']}")
    input("\nPress enter to return")
    if current_menu == LEARN_MENU:
        learn_more()
    if current_menu == FAVORITES_MENU:
        favorites_menu()


def example(word):
    highlight(word['Word'], word['Example'])
    input("\nPress enter to return")
    if current_menu == LEARN_MENU:
        learn_more()
    if current_menu == FAVORITES_MENU:
        favorites_menu()


def pronunciation(word, file):
    while True:
        clear_screen()
        print(f"{word['Pronunciation']}")
        playsound(file)
        choice = input("\nPress any key and enter to replay, \nPress only enter to return\n")
        if re.match(r'.+', choice):
            pass
        else:
            break
    if current_menu == LEARN_MENU:
        learn_more()
    if current_menu == FAVORITES_MENU:
        favorites_menu()


def save_sound(word, file):
    text = word['Word']
    audio = gTTS(text=text, lang='en', slow=False)
    audio.save(file)


def sign_in():
    global current_user
    try:
        current_user = login()
    except TypeError:
        clear_screen()
        print("Invalid username or password")
    else:
        global FAVORITES_FILE
        FAVORITES_FILE = f"{current_user['username']}_favorites.csv"
        global ARCHIVES_FILE
        ARCHIVES_FILE = f"{current_user['username']}_archives.csv"
        global POOL_FILE
        POOL_FILE = f"{current_user['username']}_wordpool.csv"
        initialize()
        wotd()
        wotd_menu()


def admin():
    global current_user
    current_user = {"username": "ADMIN", "level": "1"}
    global FAVORITES_FILE
    FAVORITES_FILE = f"{current_user['username']}_favorites.csv"
    global ARCHIVES_FILE
    ARCHIVES_FILE = f"{current_user['username']}_archives.csv"
    global POOL_FILE
    POOL_FILE = f"{current_user['username']}_wordpool.csv"
    initialize()
    wotd()
    wotd_menu()


def initialize():
    if not os.path.exists(POOL_FILE) or os.stat(POOL_FILE).st_size == 0:
        generate_wordpool(current_user['level'], POOL_FILE)


# Menus:
MAIN_MENU = {"1": signup, "2": sign_in, "3": logout, "4": admin}
WOTD_MENU = {"1": add_favorite, "2": learn_more, "3": favorites_list, "4": logout}
FAVORITES_MENU = {"1": definition, "2": example, "3": pronunciation, "4": remove_favorite, "5": favorites_list}
LEARN_MENU = {"1": definition, "2": example, "3": pronunciation, "4": wotd_menu}


if __name__ == "__main__":
    clear_screen()
    main()
