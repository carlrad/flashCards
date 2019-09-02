from google.cloud import translate
from flask import Flask
from flask import render_template
from flask import request
import sqlite3

app = Flask(__name__)

# Use flask to create the Web Site
@app.route("/translate", methods=['POST', 'GET'])
def view_translation():
    word = request.args.get('word')

    if request.method == "POST":
        word = request.form['word']
        translated_word = translator.translate(word)

        storeTranslation.store(word,translated_word)

        return render_template("index.html", translated_word=translated_word)
    else:
        return render_template("input_form.html")

@app.route("/flashCards", methods=['GET'])
def view_flash_cards():
    return render_template("flash_card_form.html")

# Class to write translations to the db
class storeTranslation(object):

    def __init__(self):
        self

    def store(word, translated_word):
        conn = sqlite3.connect('data/flashCards.db')
        c = conn.cursor()

        # check if word already exists in data
        words = c.execute("SELECT word from translations")
        formatted_word = (word,)
        if formatted_word in words:
            pass
        else:
            # Generate ID for new entry
            getId = c.execute("SELECT MAX(id) from translations")
            lastId = getId.fetchone()
            try:
                transId = lastId[0] + 1
            except:
                transId = 1
            translations = (transId, word, translated_word)

            c.execute("INSERT INTO translations VALUES (?, ?, ?)", translations)
            conn.commit()

        conn.close


# Class to run translation of words via the Google translate API
class translator(object):

    def __init__(self):
        self

    def translate(text, target='en'):
        translate_client = translate.Client()

        result = translate_client.translate(text, target_language=target)
        translation = result["translatedText"]

        return translation

if __name__ == "__main__":
    app.run()
