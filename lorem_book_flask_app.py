from flask import Flask, render_template, request, Response
from lorem_book_cipher import LoremBookCipher
from binascii import a2b_base64
import rsa

print(f"name: {__name__}")
app = Flask(__name__)


def init_keys():
    """
    Initialize the RSA keys
    """
    print("Generating key pair")
    (pubkey, privkey) = rsa.newkeys(2048)

    with open("private_key.pem", "wb") as f:
        f.write(privkey.save_pkcs1())

    with open("public_key.pem", "wb") as f:
        f.write(pubkey.save_pkcs1())

@app.route("/blog/<int:article_id>")
def blog(article_id):
    """
    View the lorem book for the specified seed article ID.

    The input box at the bottom of the page can be used to
    convert cipher text numbers into their plain text
    counterpart.
    """

    # initialize the cipher object
    lbc = LoremBookCipher(article_id)

    # render the web page, passing in the generated lorem book paragraphs.
    return render_template("blog-view.html", blog_content_paragraphs=lbc.book_paragraphs)


@app.route("/blog/edit/<int:article_id>", methods=["GET", "POST"])
def blog_edit(article_id):
    """
    Page used to encode a message into the cipher text numbers.
    The specified seed article ID is used to generate the
    lorem book text.

    The front end will encrypt the message with the public key.
    Once posted the message is decrypted with the matching
    private key and then encoded with the book cipher.
    """
    if request.method == "GET":

        # try to open the public key file
        try:
            with open("public_key.pem", "r") as f:
                # load the public key
                public_key = f.read()
        except FileNotFoundError:
            # if the key file doesn't exist then create it
            init_keys()

            # load the public key after it's been created
            with open("public_key.pem", "r") as f:
                public_key = f.read()

        # render the message encoding page, passing in the public key
        return render_template("blog-edit.html", public_key=public_key)

    elif request.method == "POST":

        # try to get the incoming data from the request
        try:
            inc_obj = request.json
        except ValueError:
            # error response if there is no data
            return Response("Invalid Input", status=400)

        if "email" not in inc_obj:
            # error response if no email key in the data
            return Response("Invalid Input", status=400)

        # initialize the book cipher object
        lbc = LoremBookCipher(article_id)

        # print(f"inc email: {inc_obj['email']}")

        # open the private key file
        with open("private_key.pem", "rb") as f:
            # load the private key
            privkey = rsa.PrivateKey.load_pkcs1(f.read())

            # decrypt the incoming message with the private key
            decrypted = rsa.decrypt(a2b_base64(inc_obj["email"]), privkey)

        # encrypt the clear text message with the lorem book cipher
        cipher_text_list = lbc.encrypt(decrypted.decode("utf-8"))

        # return the cipher text numbers
        return Response(", ".join([str(index) for index in cipher_text_list]), status=200)
