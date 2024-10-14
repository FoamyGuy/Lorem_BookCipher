# Lorem Book Cipher

Hide messages inside of lorem ipsum with a [book cipher](https://en.wikipedia.org/wiki/Book_cipher).

## Basic Usage of the Python Class

The `lorem-text` module is required. Install it with pip:

```shell
pip install lorem-text
```

```python
from lorem_book_cipher import LoremBookCipher

seed = 23894756
lbc = LoremBookCipher(seed)
print(lbc.book_str)

cipher_text_list = lbc.encrypt("secret message")
print(cipher_text_list)

plain_text = lbc.decrypt(cipher_text_list)
print(plain_text)
```


## Usage of the Flask Server

The flask server is provided as an example of a graphical interface for the Lorem Book Cipher.

It requires `Flask`, `rsa`, and `lorem-text` modules install them with pip.

```shell
pip install -r requirements.txt
```

Run the server
```shell
flask --app lorem_book_flask_app run
```

### Encrypt a Message

Select a random seed number and then use it to encode your message using the "blog edit" page.

Open your browser to `http://localhost:5000/blog/edit/<seed-number>`

e.g. `http://localhost:5000/blog/edit/123456789`

Enter your message into the "email subscription" input box at the bottom of the page and press
the subscribe button.

The cipher text numbers will be put into the very bottom of the page in some hidden text
that you must highlight in order to see.

Now you can share the seed number and the cipher text numbers with the message recipient.

## Decrypt a Message

To decrypt a message you must have the seed number and the cipher text numbers.

Open your browser to `http://localhost:5000/blog/<seed-number>`

e.g. `http://localhost:5000/blog/123456789`

The generated lorem ipsum text is shown on the page. Scroll to the bottom past all 
the paragraphs. Enter or paste the cipher text numbers into the "email subscription"
input box at the bottom of the page and press the subscribe button.

The clear text will be put into the very bottom of the page in some hidden text
that you must highlight in order to see.