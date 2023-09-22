import csv, os
from tabulate import tabulate


LEVELS = {"1": "words1.csv", "2": "words2.csv", "3": "words3.csv"}

# Can we use this program to pull straight from Chat GPT or elsewhere?
    # We would have to make a function that checks for duplicate or morpholized words amongst the three level files...
        # Currently, there are 4 duplicates between level 2 and level 3. Fix that.


# Only works for "..._favorites.csv" or "words....csv"
def format(file):
    words = []
    dated = False
    if "favorites" in file or "archives" in file:
        dated = True
        fieldnames = ["Date","Word","Part of Speech","Definition","Pronunciation","Example","Origin"]
    else:
        fieldnames = ["Word","Part of Speech","Definition","Pronunciation","Example","Origin"]
    with open(file, "r", encoding='utf8') as f:
        reader = csv.DictReader(f, fieldnames=fieldnames)
        for row in reader:
            # Skip copying the header
            if row["Part of Speech"] != "Part of Speech":
                words.append(row)

    # Sort words
    if dated:
        sorted_words = sorted(words, key=lambda x: x["Date"])
    else:
        sorted_words = sorted(words, key=lambda x: x["Word"])

    # Remove any duplicate words
    matches = []
    while True:
        matches.clear()
        start_length = len(sorted_words)
        # start_length = len(words)
        # print(start_length)
        for word in sorted_words:
        # for word in words:
            if word["Word"] not in matches:
                matches.append(word["Word"])
            else:
                sorted_words.remove(word)
                # words.remove(word)
        end_length = len(sorted_words)
        # end_length = len(words)
        # print(end_length)
        if start_length == end_length:
            break

    with open(file, "w", encoding='utf8', newline='') as f:
        # Write header without quotes
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        # Write each row with quotes around each value
        writer = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
        for row in sorted_words:
        # for row in words:
            writer.writerow(row)
    words.clear()
    sorted_words.clear()


def present(file):
    words = []
    with open(file, encoding='utf8') as f:
        reader = csv.DictReader(f, fieldnames=["Date","Word","Part of Speech","Definition","Pronunciation","Example","Origin"])
        for row in reader:
            if row["Date"] != "Date":
                word = {"Date": row["Date"], "Word": row["Word"]}
                words.append(word)
    print(tabulate(words, headers='keys', tablefmt='fancy_grid'))


def remove(word, file):
    words = []
    fieldnames = ["Date","Word","Part of Speech","Definition","Pronunciation","Example","Origin"]
    with open(file, "r", encoding='utf8') as f:
        reader = csv.DictReader(f, fieldnames=fieldnames)
        for row in reader:
            # Skip copying the header
            if row["Part of Speech"] != "Part of Speech":
                words.append(row)

    with open(file, "w", encoding='utf8', newline='') as f:
        # Write header without quotes
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        # Write each row with quotes around each value
        writer = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
        for row in words:
            if row != word:
                writer.writerow(row)
    words.clear()


def word_exists(word, file):
    if os.path.exists(file) and os.stat(file).st_size > 0:
        with open(file, "r", encoding='utf8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if word.lower() == row["Word"].lower():
                    return True
            return False


def set_word(word, file):
    with open(file, "r", encoding='utf8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if word.lower() == row["Word"].lower():
                return row


def today_exists(today, file):
    if os.path.exists(file) and os.stat(file).st_size > 0:
        with open(file, "r", encoding="utf8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['Date'] == str(today):
                    return True
            return False


def set_today(today, file):
    with open(file, "r", encoding="utf8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['Date'] == today:
                return row


def generate_wordpool(level, pool_file):
    file = LEVELS[level]
    words = []
    fieldnames = ["Word", "Part of Speech", "Definition", "Pronunciation", "Example", "Origin"]
    with open(file, "r", encoding='utf8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['Part of Speech'] != "Part of Speech":
                words.append(row)
    with open(pool_file, "w", encoding='utf8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in words:
            writer.writerow(row)


def remove_from_pool(word, pool_file):
    words = []
    fieldnames = ["Word", "Part of Speech", "Definition", "Pronunciation", "Example", "Origin"]
    with open(pool_file, "r", encoding='utf8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if word['Word'] != row['Word']:
                words.append(row)
    with open(pool_file, "w", encoding='utf8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        for row in words:
            writer.writerow(row)
