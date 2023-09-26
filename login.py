from pwinput import pwinput
import re, sys, csv, os, hashlib

# Files:
USERS_FILE = "users.csv"
# Regular Expressions:
USERNAME_REGEX = r"^[a-z0-9]{5,15}$"
PASSWORD_REGEX = r"^[a-z0-9!@#$%^&*()?~]{8,15}$"
# Messages:
    # Signup:
CREATE_USERNAME = "Create username: "
INVALID_USERNAME = "Username must be between 5 and 15 alphanumeric characters"
USERNAME_TAKEN = "Username already exists"
CREATE_PASSWORD = "Create password: "
INVALID_PASSWORD = "Password must be between 8 and 15 alphanumeric or special characters"
CONFIRM_PASSWORD = "Confirm password: "
NO_MATCH = "Passwords don't match!"
SELECT_LEVEL = "Which level of words do you wish to receive each day? You can always change this in settings."
LEVEL_1_EXPLANATION = "    Level 1 is for those that are new to English and want to start small"
LEVEL_2_EXPLANATION = "    Level 2 is for those that are decent with English and want to see some more complicated words"
LEVEL_3_EXPLANATION = "    Level 3 is for those at are fluent in English and looking to beef up their vocabulary"
SIGNUP_SUCCESS = "You're all set!"
    # Logout:
EXIT_MESSAGE = "See you tomorrow!"


def signup():
    # Create a username
    while True:
        username = input(CREATE_USERNAME)
        # Check for valid format
        if not re.match(USERNAME_REGEX, username, re.IGNORECASE):
            print(INVALID_USERNAME)
            continue
        # Check for existing username
        if user_exists(username):
            print(USERNAME_TAKEN)
            continue
        else:
            break
    # Create a password
    while True:
        password = pwinput(CREATE_PASSWORD)
        # Check for valid format
        if re.match(PASSWORD_REGEX, password, re.IGNORECASE):
            break
        else:
            print(INVALID_PASSWORD)
    # Confirm password
    while True:
        confirm_password = pwinput(CONFIRM_PASSWORD)
        if password == confirm_password:
            break
        else:
            print(NO_MATCH)
    encoder = confirm_password.encode()
    hash1 = hashlib.md5(encoder).hexdigest()
    # Select word level
    print(SELECT_LEVEL)
    print(LEVEL_1_EXPLANATION)
    print(LEVEL_2_EXPLANATION)
    print(LEVEL_3_EXPLANATION)
    while True:
        try:
            level = int(input())
            if level < 1 or level > 3:
                print("Not a valid choice. Try again.")
        except ValueError("Not a valid choice. Try again."):
            pass
        else:
            print(f"You chose level {level}!")
            break
    # Save user data into users.csv
    with open(USERS_FILE, "a", encoding='utf8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["username","password","level"])
        if os.stat(USERS_FILE).st_size == 0:
            writer.writeheader()
            writer.writerow({"username": "ADMIN", "password": "PASSWORD", "level": "1"})
        writer.writerow({"username": username, "password": hash1, "level": level})
    print(SIGNUP_SUCCESS)


def login():
    global current_user
    current_user = {}
    username = input("Enter username: ")
    password = pwinput("Enter password: ")
    authorize = password.encode()
    authorize_hash = hashlib.md5(authorize).hexdigest()
    with open(USERS_FILE, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if username == row["username"] and authorize_hash == row["password"]:
                current_user["username"], current_user["level"] = row["username"], row["level"]
                return {"username": row["username"], "level": row["level"]}
            else:
                # print("Invalid username or password")
                raise TypeError("Invalid username or password")


def logout():
    return sys.exit(EXIT_MESSAGE)


def user_exists(username):
    if os.path.exists(USERS_FILE) and os.stat(USERS_FILE).st_size > 0:
            with open(USERS_FILE, "r", encoding='utf8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if username == row['username']:
                        return True
                return False
