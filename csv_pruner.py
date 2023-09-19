# Can we use this program to pull straight from Chat GPT?
    # We would have to make a function that checks for duplicate or morpholized words amongst the three level files...
        # Currently, there are 4 duplicates between level 2 and level 3. Fix that.
LEVELS = {"1": "words1.csv", "2": "words2.csv", "3": "words3.csv", "b": "beta.csv"}

words=[]

while True:
    selection = input("Sort which set of words? ")
    if selection in LEVELS:
        CURRENT_FILE = LEVELS[selection]
        with open(CURRENT_FILE, "r") as f:
            reader = csv.DictReader(f, fieldnames=["Word","Part of Speech","Definition","Pronunciation","Example","Origin"])
            for row in reader:
                # Skip copying the header
                if row["Part of Speech"] != "Part of Speech":
                    words.append(row)

        # Alphabetize words
        sorted_words = sorted(words, key=lambda x: x["Word"])

        # Remove any duplicate words
        matches = []
        while True:
            matches.clear()
            start_length = len(sorted_words)
            print(start_length)
            for word in sorted_words:
                if word["Word"] not in matches:
                    matches.append(word["Word"])
                else:
                    sorted_words.remove(word)
            end_length = len(sorted_words)
            print(end_length)
            if start_length == end_length:
                break

        with open(CURRENT_FILE, "w") as f:
            # Write header without quotes
            writer = csv.DictWriter(f, fieldnames=["Word","Part of Speech","Definition","Pronunciation","Example","Origin"])
            writer.writeheader()
            # Write each row with quotes around each value
            writer = csv.DictWriter(f, fieldnames=["Word","Part of Speech","Definition","Pronunciation","Example","Origin"], quoting=csv.QUOTE_ALL)
            for row in sorted_words:
                writer.writerow(row)
        words.clear()
        sorted_words.clear()
        break
