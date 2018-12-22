###############################################################
# FILE : hangman.py
# WRITER : Harel Yacovian, harelyac, 311319990
# EXERCISE : intro2d cs ex4 2016-2017
# DESCRIPTION : This functions file used for the "Hangman Game"
# A game that let you guess word for arsenal of words. if you
# lose your character game will be hanged.
###############################################################

# Import the hangman_helper file
import hangman_helper

# Define constants
HIDDEN_SIGN = "_"
INPUT_TYPE = 0
INPUT_VALUE = 1


def update_word_pattern(word, pattern, letter):
    """
    Update the pattern accordingly and reveals the guessed words in it.
    """
    # make pattern string as list for changing object inside it
    pattern_list = list(pattern)
    # Go through the pattern and reveal the letters.
    for i in range(len(word)):
        # Check where the letter exist, and reveal it on the pattern.
        if word[i] == letter:
            pattern_list[i] = letter
    # Rejoin the list onto one string
    pattern = "".join(pattern_list)
    return pattern


def filter_words_list(words, pattern, wrong_guess_lst):
    """
    A functions thats get the words/guess list and pattern and
    return a new suitable word from the arsenal
    """
    check_pattern = "_" * len(pattern)

    # Define the sorted list
    sorted_list = []

    # Sort the words list to words that got same pattern size.
    for i in range(len(words)):
        if pattern != check_pattern:
            if len(words[i]) == len(pattern):
                # Run on each word in the words list
                for k in range(len(words[i])):
                    if pattern[k] == HIDDEN_SIGN:
                        continue
                    # Check if word contain same letters at the same indexes
                    # of pattern and if those letters dont exist in other
                    # indexes of word
                    elif words[i][k] == pattern[k] and words[i][k] \
                            not in words[i][k + 1:] and words[i][k] \
                            not in words[i][:k]:
                        # Check if the word dont contain guessed words
                        for j in range(len(wrong_guess_lst)):
                            if wrong_guess_lst[j] in words[i]:
                                break
                                # if everything is alright append the
                                # word to sorted list
                        else:
                            sorted_list.append(words[i])
        else:
            # Check if guess list is not empty
            if wrong_guess_lst != []:
                # Check if the word dont contain guessed words
                for j in range(len(wrong_guess_lst)):
                    if wrong_guess_lst[j] in words[i]:
                        break
                    # if everything is alright append the word to sorted list
                    else:
                        sorted_list.append(words[i])
            else:
                sorted_list = words
                break
    return sorted_list


# Define constant used for the two functions below
CHAR_A = 97


def letter_to_index(letter):
    """
    Return the index of the given letter in an alphabet list.
    """
    return ord(letter.lower()) - CHAR_A


def index_to_letter(index):
    """
    Return the letter corresponding to the given index.
    """
    return chr(index + CHAR_A)


def choose_letter(words, pattern):
    """
    This function gets list of suitable words after they were sorted and also
    pattern, and then calculate the char that shows the most in all chars.
    """
    # Initialize
    maximal_chars = [0] * 26
    alpha_index = 0
    chosen_letters = []
    alpha_char = ""
    # Iterate each word in word list
    for word in range(len(words)):
        # Iterate chars in each words
        for letter in range(len(words[word])):
            # check if letter is in the pattern already and don't count
            #  it and continue to next words
            if words[word][letter] in pattern:
                continue
            # Calling the "letter to index function"
            alpha_index = letter_to_index(words[word][letter])
            # change count value of each index that represent a char in
            # alphabetical order
            maximal_chars[alpha_index] += 1

    # Check the maximal indexes in the list
    for i in range(len(maximal_chars)):
        if maximal_chars[i] == max(maximal_chars):
            # reveal the index into a readable letter
            alpha_char = index_to_letter(i)
            chosen_letters.append(alpha_char)
    return chosen_letters[0]


def run_single_game(words_list):
    """
    A function that starts the game with given words list.
    """

    # Initialize parameters
    wrong_guess_count = 0
    wrong_guess_words = []
    already_chosed = []
    msg = ""

    # Get random name from the words list.
    random_word = hangman_helper.get_random_word(words_list)

    # Initialize the pattern
    pattern = len(random_word) * HIDDEN_SIGN

    # Print default message to user
    msg = hangman_helper.DEFAULT_MSG

    # the game wont stop until the pattern will be revealed or guess number
    # will cross the max errors available.
    while wrong_guess_count < hangman_helper.MAX_ERRORS and \
                    pattern != random_word:
        # display the current state in each iteration of the loop
        hangman_helper.display_state(pattern, wrong_guess_count,
                                     wrong_guess_words, msg)
        # Get input from user
        request = hangman_helper.get_input()

        # Check if the input is a guess
        if request[INPUT_TYPE] == hangman_helper.LETTER:

            # Check parameter validation
            if len(request[INPUT_VALUE]) != 1 or \
                    not request[INPUT_VALUE].islower():
                msg = hangman_helper.NON_VALID_MSG
                continue
            # Check if the letter already was chosen before.
            elif request[INPUT_VALUE] in already_chosed:
                msg = hangman_helper.ALREADY_CHOSEN_MSG + request[INPUT_VALUE]
            # If the guessed letter does exist in the word
            elif request[INPUT_VALUE] in random_word:
                # Updating the the word pattern accordingly
                pattern = update_word_pattern(random_word, pattern,
                                              request[INPUT_VALUE])
                msg = hangman_helper.DEFAULT_MSG
                already_chosed.append(request[INPUT_VALUE])
            else:
                wrong_guess_count += 1
                wrong_guess_words.append(request[INPUT_VALUE])
                msg = hangman_helper.DEFAULT_MSG
                already_chosed.append(request[INPUT_VALUE])

        elif request[INPUT_TYPE] == hangman_helper.HINT:
            # Call the filter words function
            sort = filter_words_list(words_list, pattern, wrong_guess_words)
            # Call the choose letter function
            chosen_letter = choose_letter(sort, pattern)
            # Initialize the msg variable
            msg = hangman_helper.HINT_MSG + chosen_letter

    # Initialise the display function in case winning
    if pattern == random_word:
        msg = hangman_helper.WIN_MSG
    # Initialise the display function in case of losing
    elif wrong_guess_count == hangman_helper.MAX_ERRORS:
        msg = hangman_helper.LOSS_MSG + random_word
    # Calling the display function
    hangman_helper.display_state(pattern, wrong_guess_count, wrong_guess_words,
                                 msg, ask_play=True)


def main():
    """
    The main/root function of the file
    """
    # Initialize words from specific file
    words_list = hangman_helper.load_words()
    # Run single game with given word list to choose from
    run_single_game(words_list)
    # Ask the user if he would like to play again
    request = hangman_helper.get_input()
    if request[INPUT_TYPE] == hangman_helper.PLAY_AGAIN:
        if request[INPUT_VALUE]:
            run_single_game(words_list)


if __name__ == "__main__":
    hangman_helper.start_gui_and_call_main(main)
    hangman_helper.close_gui()
