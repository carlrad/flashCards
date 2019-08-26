from google.cloud import translate
from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

@app.route("/translate", methods=['POST', 'GET'])
def view_translation():
    word = request.args.get('word')

    if request.method == "POST":
        word = request.form['word']
        translated_word = translator.translate(word)
        return render_template("index.html", translated_word=translated_word)
    else:
        return render_template("input_form.html")



# Class to run translation of words via the Google translate API
class translator(object):

    def __init__(self):
        self

    def translate(text, target='en'):
        translate_client = translate.Client()

        result = translate_client.translate(text, target_language=target)
        translation = result["translatedText"]

        return translation

text = 'Hallo Welt'
translator.translate(text)

if __name__ == "__main__":
    app.run()
