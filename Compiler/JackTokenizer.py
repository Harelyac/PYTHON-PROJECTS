import re

keywords_list = ["class", "constructor", "function", "method", "field",
                 "static",
                 "var", "int", "char", "boolean", "void", "true", "false",
                 "null", "this",
                 "let", "do", "if", "else", "while", "return"]
symbols_list = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '/',
                '*', '>', '<', '&','=', '~', '|']

exceptions = ["<", ">", "\"", "&"]

class JackTokenizer:
    string_list = []

    def __init__(self, file_text):
        self.index = 0  # token index
        self.text = file_text.readlines()  # the original jack commands
        self.tokenized_text = []  # the tokenized text include only tokens
        # which the engine will work on.
        self.current_token = None
        self.TokenizingProccess(self.text) # the whole process starts here

    def TokenizingProccess(self, text):
        # ignoring all kind of comments and replacing and saving all strings("") in special list
        inside_comment = False
        inside_string = False

        for line in text:
            line = line.lstrip()
            if line == "" or line[0:2] == "//" or line == "\n":
                continue
            if line[0:2] == "/*":
                inside_comment = True
            if inside_comment and "*/" in line:  # if start comment and close comment on the same line
                inside_comment = False
                two_sides = line.split("*/")
                if two_sides[1] != "\n":
                    line = two_sides[1]
                else:
                    continue
            elif inside_comment:  # if we dont see the light the end of the tunnel
                continue
            # if the line is not a kind of comment - check if it is any other object and add it to tokenizd text
            if not inside_comment:
                temp = ""
                for index, char in enumerate(line):

                    if char == "\"":
                        # if we are about to close a string
                        if inside_string:
                            inside_string = False
                            temp += str(char)
                            self.tokenized_text.append(temp)
                            temp = ""
                            continue
                        # if we in string
                        elif not inside_string and temp != "":
                            self.tokenized_text.append(temp)
                            temp = ""
                            temp += str(char)
                            inside_string = True
                            continue
                        elif not inside_string and temp == "":
                            temp += str(char)
                            inside_string = True
                            continue

                    if inside_string:
                        temp += char

                    # if we are not in a string
                    else:
                        if char == "/":
                            if line[index + 1] == "/":
                                temp = ""
                                break
                            elif line[index + 1] == "*":
                                inside_comment = True
                                break
                            else:
                                # if its the "/" symbol and continue iteration
                                self.tokenized_text.append(char)
                                temp = ""
                                continue

                        if char == "\n":
                            break
                        # if its a normal char
                        if char != " " and char not in symbols_list:
                            temp += str(char)
                        # if the char is whitespace so we just finished read a token
                        elif char == " " and temp != "":
                            self.tokenized_text.append(temp)
                            temp = ""
                        # if we deal with one of the symbol
                        elif char in symbols_list and temp != "":
                            self.tokenized_text.append(temp)
                            self.tokenized_text.append(char)
                            temp = ""
                        elif char in symbols_list and temp == "":
                            self.tokenized_text.append(char)

        # another cleaner of the tokens which keep up for reserved words and
        # lstrip them all
        for index,token in enumerate(self.tokenized_text):
            self.tokenized_text[index] = token.lstrip()
            if token in exceptions:
                if token == "<":
                    self.tokenized_text[index] = "&lt;"
                elif token == ">":
                    self.tokenized_text[index] = "&gt;"
                elif token == "\"":
                    self.tokenized_text[index] = "&quot;"
                elif token == "&":
                    self.tokenized_text[index] = "&amp;"


    def advance(self):
        "advancing the next token in the tokenized_text list"
        if self.hasMoreTokens():
            self.current_token = self.tokenized_text[
                self.index].lstrip()  # remove whitespace maybe unneeded
            self.index += 1

    def hasMoreTokens(self):
        if self.index == len(self.tokenized_text):
            return False
        return True

    # resposnsible to return the type of tokens only - job of the tokenizer
    def typeOfToken(self):
        int_pattern = '^\d+$'
        string_pattern = '^\".*\"$'
        identifier_pattern = '^[^0-9]\w*$'

        if self.current_token in keywords_list:
            return "keyword"

        if self.current_token in symbols_list:
            return "symbol"

        if re.match(int_pattern, self.current_token):
            return "int_constant"

        if re.match(string_pattern, self.current_token):
            return "string_constant"
        # if none of the above - so it must be an identifier
        if re.match(identifier_pattern, self.current_token):
            return "identifier"

    def getNextToken(self):
        """returns the next token without advancing the engine (for ll(1) purposes
        """
        if self.hasMoreTokens():
            return self.tokenized_text[self.index]

    def getCurrentToken(self):
        "returns the current token which the compilationEngine is working on"
        return self.current_token

    def showNextToken(self):
        """very useful method which used for ll(1) problem"""
        if self.hasMoreTokens():
            return self.tokenized_text[self.index]
        return True


    def previousToken(self):
        """get the previous token"""
        if self.index>1:
            self.current_token = self.tokenized_text[self.index -2]
            self.index -= 1