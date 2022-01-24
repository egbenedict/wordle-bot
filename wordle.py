import random

''' 
Strategy Outline:
    1. Tabulate character frequency and list in order
    2. Choose word that uses greatest total of frequencies of letters that are still viable
    3. If a letter is yellow, must include
    4. If a letter is green, must include in same spot
    5. Could also have a strategy that takes into account frequency of letter location!

'''

ANSWER_LETTER_FREQS = {'a': 979, 'b': 281, 'c': 477, 'k': 210, 's': 669, 'e': 1233, 't': 729, 'y': 425, 'o': 754, 'h': 389, 'r': 899, 'i': 671, 'd': 393, 'l': 719, 'u': 467, 'v': 153, 'n': 575, 'g': 311, 'p': 367, 'm': 316, 'f': 230, 'x': 37, 'w': 195, 'z': 40, 'j': 27, 'q': 29}

LETTERS = ['a', 'b', 'c', 'k', 's', 'e', 't', 'y', 'o', 'h', 'r', 'i', 'd', 'l', 'u', 'v', 'n', 'g', 'p', 'm', 'f', 'x', 'w', 'z', 'j', 'q']

SORTED_ANSWER_LETTERS = ['e', 'a', 'r', 'o', 't', 'l', 'i', 's', 'n', 'c', 'u', 'y', 'd', 'h', 'p', 'm', 'g', 'b', 'f', 'k', 'w', 'v', 'z', 'x', 'q', 'j']

# Calculate the frequency of each letter in wordle-answers-alphabetical.txt
def calculate_letter_frequencies(filename):
    # Open file
    with open(filename, 'r') as f:
        # Read file
        data = f.read()
        # Split into words
        words = data.split()
        # Create dictionary to store letter frequencies
        letter_frequencies = {}
        # Loop through words
        for word in words:
            # Loop through letters
            for letter in word:
                # If letter is in dictionary, increment frequency
                if letter in letter_frequencies:
                    letter_frequencies[letter] += 1
                # If letter is not in dictionary, add to dictionary
                else:
                    letter_frequencies[letter] = 1
    # Return dictionary
    return letter_frequencies

# Sum the frequencies of each unique letter in the given word
def sum_letter_frequencies(word, letter_frequencies):
    # Create variable to store sum of letter frequencies
    sum = 0
    seen_letters = []
    # Loop through letters in word
    for letter in word:
        if letter not in seen_letters:
            # Add letter frequency to sum
            sum += letter_frequencies[letter]
            # Add letter to seen_letters
            seen_letters.append(letter)
    # Return sum
    return sum


class BasicSolver:

    def __init__(self):
        self.possible_letters = LETTERS[:]
        with open("wordle-answers-alphabetical.txt", 'r') as f:
            self.possible_words = f.read().split()
        self.solved = False

    # Finds the most likely possible word using the possible letters
    def find_most_likely_word(self):
        # Create dictionary to store word frequencies
        word_frequencies = {}
        # Loop through possible words
        for word in self.possible_words:
            # Create variable to store sum of letter frequencies
            word_frequencies[word] = sum_letter_frequencies(word, ANSWER_LETTER_FREQS)
        # Return most likely word
        return max(word_frequencies, key=word_frequencies.get)

    # Interacts with the user to solve the puzzle
    def solve(self):
        count = 1
        while not self.solved:
            guess = self.find_most_likely_word()
            print("Guess " + str(count) + ": " + guess.upper())

            # Ask user how guess scores
            score = input("How does this guess score?\n").strip()

            if score == "22222":
                break

            # Modify possible letters and possible words based on user input
            self.modify_possible_letters(guess, score)
            self.modify_possible_words(guess, score)
            count += 1
        print("Ha!")
        
            

    # Modifies the possible letters based on the user's input
    def modify_possible_letters(self, guess, score):
        for i in range(len(guess)):
            if score[i] == '0':
                self.possible_letters.remove(guess[i])

    # Modifies the possible words based on the user's input
    def modify_possible_words(self, guess, score):
        ok_letters = []
        for i in range(len(guess)):
            if score[i] == '1':
                ok_letters.append((guess[i], i))

        good_letters = []
        for i in range(len(guess)):
            if score[i] == '2':
                good_letters.append((guess[i], i))

        bad_letters = []
        for i in range(len(guess)):
            if score[i] == '0':
                if guess[i] not in [x[0] for x in ok_letters] and guess[i] not in [x[0] for x in good_letters]:
                    bad_letters.append(guess[i])

        # print(bad_letters, ok_letters, good_letters)

        new_possible_words = []

        for word in self.possible_words:
            bad = False
            for letter in bad_letters:
                if letter in word:
                    bad = True
            for letter, i in ok_letters:
                if letter not in word:
                    bad = True
                if word[i] == letter:
                    bad = True
            for letter, i in good_letters:
                if letter not in word:
                    bad = True
                if word[i] != letter:
                    bad = True 

            if not bad:
                new_possible_words.append(word)

        self.possible_words = new_possible_words

     











def __main__():
    s = BasicSolver()
    s.solve()






if __name__ == "__main__":
    __main__()
