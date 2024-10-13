import secrets
import random

class BookCipher:
    """
    Super class that can be extended to make a BookCipher.
    https://en.wikipedia.org/wiki/Book_cipher

    Subclasses must implement the book_str property and make it
    return a string with the content of the book.
    """
    def __init__(self):
        # optional mapping of letter swaps to carry out before
        # encoding the character into the book index.
        self.swaps = {}

        # optional flag to force plain_text to uppercase
        # before encoding
        self.force_uppercase = False

    @property
    def book_str(self):
        """
        The content of the book to be used to encode messages.
        """
        raise NotImplementedError

    def encrypt(self, plain_text):
        """
        Encrypts the given plain text.
        :param plain_text: The plain text to be encrypted.
        """
        if self.force_uppercase:
            plain_text = plain_text.upper()
        cipher_text_list = []

        # a dictionary which will have keys equal to characters
        # in the book_str and values equal to a list containing
        # a numerical indexes within the book_str where that character
        # can be found. The list of indexes are in a randomized order.
        shuffled_letter_indexes = {}

        # a dictionary which will have keys equal to characters
        # in the book_str and values equal to the next index to use
        # within the lists in the values of shuffled_letter_indexes
        current_indexes = {}

        # Build up the shuffled_letter_indexes dictionary
        # with lists of indexes of each character
        for index, letter in enumerate(self.book_str):

            # if this character key has been initialized in the dictionary already
            if letter in shuffled_letter_indexes:
                # add the new index to the list at a random location
                shuffled_letter_indexes[letter].insert(secrets.randbelow(len(shuffled_letter_indexes[letter]) + 1), index)
            else:
                # initialize a list for this character holding the index
                shuffled_letter_indexes[letter] = [index]

            # initialize the current index for this letter to 0
            current_indexes[letter] = 0

        # loop thru characters in the plain_text
        for letter in plain_text:

            # if the character is in the swaps mapping
            if letter in self.swaps:
                # perform the swap
                letter = self.swaps[letter]

            # if letter is uppercase, and not in the book_str then change
            # it to lowercase
            if letter.upper() == letter and letter not in self.book_str:
                letter = letter.lower()

            # if the current character exists in the book_str (else, skip it)
            if letter in self.book_str:
                # append the current index within the shuffled list to the cipher_text_list
                cipher_text_list.append(shuffled_letter_indexes[letter][current_indexes[letter]])

                # increment the current index for this character
                current_indexes[letter] += 1

                # if the new index is past the end of our list
                if current_indexes[letter] >= len(shuffled_letter_indexes[letter]):
                    # shuffle the list so that the indexes are in a different order
                    shuffled_letter_indexes[letter] = BookCipher.shuffled_list(shuffled_letter_indexes[letter])
                    # reset the current index to 0
                    current_indexes[letter] = 0

        # return the list of indexes that makes up the cipher text
        return cipher_text_list

    @staticmethod
    def shuffled_list(list_to_shuffle):
        """
        return a copy of the given list with its elements shuffled.
        """
        shuffled_list = []
        while len(list_to_shuffle) > 0:
            picked_item = secrets.choice(list_to_shuffle)
            shuffled_list.append(picked_item)
            list_to_shuffle.remove(picked_item)
        return shuffled_list

    def decrypt(self, cipher_text_list):
        """
        Decrypts the given cipher text list back into plain text.
        """
        # list to hold the plain text characters
        plain_text_list = []

        # loop thru the indexes in the cipher text list
        for index in cipher_text_list:
            # find the character at the current index
            letter = self.book_str[index]

            # if this character is in the swaps mapping
            if letter in self.swaps:
                # perform the swap
                letter = self.swaps[letter]

            # add the plain text character to the list
            plain_text_list.append(letter)

        # join the plain text list into a string and return it
        return "".join(plain_text_list)
