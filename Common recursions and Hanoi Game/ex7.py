###############################################################
# FILE : ex7.py
# WRITER : Harel Yacovian, harelyac, 311319990
# EXERCISE : intro2d cs ex7 2016-2017
# DESCRIPTION : This functions file used for making the some
# recursions functions and the Hanoi game engine.
###############################################################

POWER = 0.5


def print_to_n(n):
    """
    prints all the z numbers up to n we get as input. from bottom to up.
    :param n: the chosen n to print number until we reach it
    :return: prints all the number up to n
    """
    # Make sure we work with right Z numbers
    if n < 1:
        return None
    elif n == 1:
        print(n)
    else:
        print_to_n(n - 1)
        print(n)


def print_reversed(n):
    """
    prints the number up until n via reversed way order
    :param n: the n chosen number to work with
    :return: prints all the number untill in reversed order
    """
    if n < 1:
        return None
    if n == 1:
        print(n)
    else:
        print(n)
        print_reversed(n - 1)


def has_divisor_smaller_than(n, i):
    """
    this function check the divisors of n number
    :param n: the given number
    :param i: the index which run on all the optional divisors.
    :return: a boolean value that return True if
    there is a certain divisor and false if not
    """
    if i == 1:
        return False
    elif n % i == 0:
        return True
    else:
        return has_divisor_smaller_than(n, i - 1)


def is_prime(n):
    """
    check if n number is a prime number - means that it divides only with
    itself and 1.
    :param n: the checked number
    :return: an answer to the questions if n is a prime number or not
    """
    if n <= 1:
        return False
    else:
        return not has_divisor_smaller_than(n, n - 1)


def check_divisors(lst, n, i):
    """
    check all divisors of n number and put them all inside a list and print it
    :param lst: the list to be printed
    :param n: the number which will be checked for divisors
    :param i: an index which go over all the optional divisors.
    :return: the full list after appending.
    """

    # Check case where n is just zero value
    if n == 0:
        return []
    # Check case where i has reached the max value permitted
    elif i == n or i == -n:
        lst.append(i)
        return lst
    # The middle case in between which check the division
    elif n % i == 0:
        lst.append(i)
        return check_divisors(lst, n, i + 1)
    # The case where its not divide as we want and still need
    # to make another recursion call
    else:
        return check_divisors(lst, n, i + 1)


def divisors(n):
    """
    the main function of the divisors. it will call the check divisors
    functions to help find and append all the divisors onto a list.
    :param n:
    :return:
    """
    list_of_divisors = list()
    return check_divisors(list_of_divisors, n, 1)


def factorial(n):
    """
    calculate the factorial of a certain number n.
    :param n: the number to be check for factorial value
    :return: return the value of factorial.
    """
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)


def power_of_number(n, x):
    """
    check the power of a number.
    :return: return the power itself
    """
    if n == 0:
        return 1
    else:
        return x * power_of_number(n - 1, x)


def exp_n_x(n, x):
    """
    check the exp value of certain number means that it will be equal to e
    power x at the end of it.
    :param n: the size of the sum. how many times we will sun the whole number.
    :param x: parameter indicate the valuer of e.
    :return: the result which gives the exponential sum.
    """
    if n == 0 or x == 0:
        return 1
    else:
        # Calc factorial of a number
        fact = factorial(n)
        # Calc the power of a number
        number_power = power_of_number(n, x)
        # Divide the both results.
        result = number_power / fact
        return result + exp_n_x(n - 1, x)


def play_hanoi(hanoi, n, src, dest, temp):
    """
    This function resolve the hanoi game! step by step with recursions calls!
    :param hanoi: an object which indicate the hanoi game
    :param n: n is the number of disks to be moved.
    :param src: the source peg
    :param dest: the obj peg
    :param temp: the middle peg
    :return: the wanted result. when all the disks will be ordered as should
    be on the obj peg.
    """

    # Base case
    if n == 1:
        hanoi.move(src, dest)
    elif n == 0:
        pass
    else:
        # This game consist of three basic recursions calls!
        # move n - 1 disks to middle peg
        play_hanoi(hanoi, n - 1, src, temp, dest)
        # move last peg to obj peg
        play_hanoi(hanoi, 1, src, dest, temp)
        # move all rest n - 1 disks to the obj peg
        play_hanoi(hanoi, n - 1, temp, dest, src)


def print_binary_sequences_with_prefix(n, prefix):
    """
    prints all binary sequences of 1,0 with n length.
    :param n: the length of the sequence
    :param prefix: the start point of the sequences - each time it will raise
    and at the end it will complete the full sequence.
    :return: return all the possible sequences.
    """
    # Base case
    if n == 0:
        print(prefix)
    else:
        # Consist of two basics recursions calls!
        print_binary_sequences_with_prefix(n - 1, prefix + "1")
        print_binary_sequences_with_prefix(n - 1, prefix + "0")


def print_binary_sequences(n):
    """
    will print the binary sequences as described in the upper function.
    :param n:
    :return:
    """
    prefix = ""
    print_binary_sequences_with_prefix(n, prefix)


def print_sequences_with_prefix(n, char_list, prefix):
    """
    prints all sequeces with char and not with 1,0 as before.
    :param n: the length of each sequences.
    :param char_list: the list of char to be chosen as each char in the
    sequences
    :param prefix: the start point of each sequence will build the
    whole sequence
    :return:
    """
    if n == 0:
        print(prefix)
    else:
        for char in range(len(char_list)):
            print_sequences_with_prefix(n - 1, char_list,
                                        prefix + char_list[char])


def print_sequences(char_list, n):
    """
    print all the sequences with given char list if sequence of size n
    :param char_list: the full char list
    :param n: the length
    :return: return all the sequences
    """
    prefix = ""
    print_sequences_with_prefix(n, char_list, prefix)


def print_no_repetition_sequences_with_prefix(n, char_list, prefix):
    """
    prints same sequences witout repetitions.
    :param n: length
    :param char_list: the list of chars
    :param prefix: the start point and the builder of the sequence.
    :return: return all the sequences.
    """
    if n == 0:
        print(prefix)
    else:
        for char in range(len(char_list)):
            temp_list = char_list[:]
            del temp_list[char]
            print_no_repetition_sequences_with_prefix(n - 1, temp_list, prefix
                                                      + char_list[char])


def print_no_repetition_sequences(char_list, n):
    """
    same as above and just call it.
    :param char_list:
    :param n:
    :return:
    """
    prefix = ""
    print_no_repetition_sequences_with_prefix(n, char_list, prefix)


def no_repetition_sequences_list_with_prefix(n, char_list, prefix, new_list):
    """
    same prints sequences with given char list with no repetitions and appends
    all to a list.
    :param n: the lenth of the sequence
    :param char_list: the list of chars
    :param prefix: the builder of the sequence
    :param new_list: new list in order to not change the indexes
    :return:
    """
    if n == 0:
        new_list.append(prefix)
    else:
        for char in range(len(char_list)):
            temp_list = char_list[:]
            del temp_list[char]
            no_repetition_sequences_list_with_prefix(n - 1, temp_list,
                                                     prefix + char_list[char],
                                                     new_list)

    return new_list


def no_repetition_sequences_list(char_list, n):
    """
    call the above function and act the same.
    :param char_list: full char list
    :param n: the length of sequences
    :return: return all the sequences.
    """
    prefix = ""
    new_list = []
    return no_repetition_sequences_list_with_prefix(n, char_list, prefix,
                                                    new_list)

