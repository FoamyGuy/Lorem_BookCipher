from book_cipher import BookCipher
import random
import string
from lorem_text import lorem

class LoremBookCipher(BookCipher):
    MIN_COUNT = 10

    def __init__(self, seed):
        super().__init__()
        # seed the randomness in the lorem generator so that the output is
        # deterministic based on the seed
        random.seed(seed)

        # a list to hold paragraphs of lorem ipsum content
        self._book_paragraphs = []

        # loop for how many paragraphs we want
        for i in range(6):
            # add a new paragraph
            self.book_paragraphs.append(lorem.paragraph())

        # enforce the MIN_COUNT occurrences for each character
        LoremBookCipher.ensure_letter_count(self.book_paragraphs, seed)

        # set the lorem content in a string to be used as the book_str
        self.lorem_content = " ".join(self.book_paragraphs)

    @property
    def book_paragraphs(self):
        """
        The paragraphs of lorem ipsum content
        """
        return self._book_paragraphs

    @book_paragraphs.setter
    def book_paragraphs(self, new_paragraphs_list):
        self._book_paragraphs = new_paragraphs_list

    @property
    def book_str(self):
        """
        The book content as a string. Messages will be encoded into indexes
        within this book content.
        """
        return self.lorem_content

    @staticmethod
    def letter_usage_histogram(paragraphs):
        """
        return a histogram of character usage within the given paragraphs
        """
        hist = {}
        for paragraph in paragraphs:
            for char in paragraph.lower():
                if char in hist:
                    hist[char] += 1
                else:
                    hist[char] = 1
        return hist

    @staticmethod
    def ensure_letter_count(paragraphs, random_seed):
        """
        Ensure there are at least MIN_COUNT of each character in the paragraphs.
        For any characters that are short of the MIN_COUNT add random instances of
        them in order to get up to MIN_COUNT
        """
        # set the seed so that the resulting book content is deterministic
        random.seed(random_seed)
        # get the histogram of character usage counts
        usage_hist = LoremBookCipher.letter_usage_histogram(paragraphs)

        # we care about lower case alphabet plus space, comma, and period
        alphabet = string.ascii_lowercase + " ,."

        # loop thru the characters we want to ensure counts of
        for char in alphabet:
            # if this character doesn't have at least MIN_COUNT occurences
            if char not in usage_hist or usage_hist[char] <= LoremBookCipher.MIN_COUNT:

                # calculate how many instances we need insert to reach MIN_COUNT
                if char not in usage_hist:
                    loop_count = LoremBookCipher.MIN_COUNT
                else:
                    loop_count = LoremBookCipher.MIN_COUNT - usage_hist[char]

                # loop as many times as we need
                for i in range(loop_count):

                    # get a random paragraph index
                    insert_paragraph_index = random.randint(0, len(paragraphs) - 1)

                    # get a random character index to use within that paragraph
                    insert_char_index = random.randint(0, len(paragraphs[insert_paragraph_index]) - 1)

                    # convert the paragraph to a list
                    paragraph_list = list(paragraphs[insert_paragraph_index])

                    # if the character is not a period
                    if char != ".":
                        # insert an instance of the character at the decided location
                        paragraph_list.insert(insert_char_index, char)

                    else:  # the character is a period
                        # insert a period and a space to avoid a random period in the middle of a word
                        paragraph_list.insert(insert_char_index, f". ")
                    # print(f"inserting {char} at {insert_paragraph_index} : {insert_char_index}")

                    # join the paragraph list back into a string and
                    # put it back in the paragraphs list
                    paragraphs[insert_paragraph_index] = "".join(paragraph_list)


if __name__ == '__main__':

    seed = 23894756
    lbc = LoremBookCipher(seed)
    print(lbc.book_str)

    cipher_text_list = lbc.encrypt("secret message")
    print(cipher_text_list)

    plain_text = lbc.decrypt(cipher_text_list)
    print(plain_text)
