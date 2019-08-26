from nose.tools import *
import sys
from flashCards import translate_words

translate_words.app.config['TESTING'] = True
web = translate_words.app.test_client()

# Valid translation
def test_translation_via_googleTranslate():
    text = "Hallo Welt"
# When a translation is run
    translation = translate_words.translator.translate(text)
# Then the correct English word is returned
    assert_equal(translation, "Hello World")

# Connect to Google translate API
# Note: this test needs to be mocked once dev complete to avoid incurring api usage charges!!

# test the web Form
def test_index():

    rv = web.get('/', follow_redirects=True)
    assert_equal(rv.status_code, 404)

    rv = web.get('/translate', follow_redirects=True)
    assert_equal(rv.status_code, 200)
    assert_in(b"Enter a word for translation", rv.data)

    data = {'word': 'Hallo Welt'}
    rv = web.post('/translate', follow_redirects=True, data = data)
    assert_in(b"Hello World", rv.data)
