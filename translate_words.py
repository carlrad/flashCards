from google.cloud import translate
# from flask import flask
# from flask import render_template
# from flask import request
#
# app = Flask(__name__)
#
# @app.route("/translate", methods=['POST', 'GET'])

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
