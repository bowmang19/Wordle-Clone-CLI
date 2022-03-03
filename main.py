import random
import json
from termcolor import colored
import re


def load_historic_scores():
    with open('scores.json') as json_file:
        score_dict = json.load(json_file)
    return score_dict


def save_historic_scores(score_dict):
    with open('scores.json', 'w') as json_file:
        json.dump(score_dict, json_file)


def display_historic_scores(score_dict):
    values = score_dict.values()
    total = sum(values)
    print("HISTORIC SCORES")
    for i in range(1, 8):
        if i == 7:
            print(f"Incomplete: {round(((score_dict[str(i)])/total)*100)}%")
        else:
            print(f"Guess {i}: {round(((score_dict[str(i)])/total)*100)}%")


def load_words():
    filtered_word_bank = []
    full_word_bank = []
    with open("filteredwords.txt", 'r') as f:
        for line in f:
            line = line.split(",")
            for i in range(len(line)):
                line[i] = re.sub(r'[^A-Za-z]', '', line[i])
                if line[i] != "":
                    filtered_word_bank.append(line[i])
    with open("fullwords.txt", 'r') as f:
        for line in f:
            line = line.split(",")
            for i in range(len(line)):
                line[i] = re.sub(r'[^A-Za-z]', '', line[i])
                if line[i] != "":
                    full_word_bank.append(line[i])
    return filtered_word_bank, full_word_bank


def check_status(guess, target):
    if guess == target:
        return True
    else:
        return False


def check_guess(guess, target, result):
    checked = {}
    for i in guess:
        checked[i] = 0
    for i in range(len(guess)):
        if guess[i] == target[i]:
            checked[guess[i]] = checked[guess[i]] + 1
            print(colored(guess[i], 'green'), end='')
            result += "🟩"
        elif guess[i] in target:
            if guess.count(guess[i]) == target.count(guess[i]):
                print(colored(guess[i], 'yellow'), end='')
                result += "🟨"
            elif guess.count(guess[i]) > target.count(guess[i]):
                if checked[guess[i]] < target.count(guess[i]):
                    checked[guess[i]] = checked[guess[i]] + 1
                    print(colored(guess[i], 'yellow'), end='')
                    result += "🟨"
                else:
                    print(guess[i], end='')
                    result += "⬜"
            else:
                print(colored(guess[i], 'yellow'), end='')
                result += "🟨"
        else:
            print(guess[i], end='')
            result += "⬜"
    return result


def play(count, full_word_bank, filtered_word_bank):
    guess = input(f"\nEnter guess ({count+1}/6): ")
    while guess not in full_word_bank and guess not in filtered_word_bank:
        print("Guess not in word bank.")
        guess = input(f"\nEnter guess ({count+1}/6): ")
    return guess


def main():
    filtered_word_bank, full_word_bank = load_words()
    play_status = "y"
    score_dict = load_historic_scores()
    while play_status == "y":
        result = ""
        target = filtered_word_bank[random.randint(0, len(filtered_word_bank))]
        print(f"TARGET: {target}")
        win_status = False
        count = 0
        while win_status == False and count <= 5:
            guess = play(count, full_word_bank, filtered_word_bank)
            win_status = check_status(guess, target)
            result = check_guess(guess, target, result)
            result += "\n"
            count += 1
        print("\n\n")
        if count < 6:
            print(f"Score: {count}/6")
            score_dict[str(count)] += 1
        else:
            print("You lost.")
            print(f"Answer: {target}")
            score_dict["7"] += 1
        print(result)
        display_historic_scores(score_dict)
        play_status = input("\nPlay again? (y/n): ")
    save_historic_scores(score_dict)


if __name__ == "__main__":
    main()
