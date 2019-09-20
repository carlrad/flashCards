from nose.tools import *
import sys
from flashCards import translate_words
import sqlite3

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

    rv = web.get('/flashCards', follow_redirects=True)
    assert_equal(rv.status_code, 200)
    assert_in(b"Click to get a flash card and start learning!", rv.data)

    data = {'word': 'Hallo Welt'}
    rv = web.post('/translate', follow_redirects=True, data = data)
    assert_in(b"Hello World", rv.data)

# test the database connection
def test_database_interaction():
    # Given a word and translation
    word = "Wort"
    translated_word = "Word"

    # When the word and translated word are added to the the database
    translate_words.storeTranslation.store(word, translated_word)

    # Then the word and translation can be recalled from the database
    conn = sqlite3.connect('data/flashCards.db')
    c = conn.cursor()
    query_result = c.execute("SELECT word, translation from translations")
    stored_words = query_result.fetchall()
    assert_in((word, translated_word), stored_words)
    conn.close

# test duplicate words are not stored
def test_duplicates_not_stored():
    # Given a word which has already been translated and stored
    conn = sqlite3.connect('data/flashCards.db')
    c = conn.cursor()
    duplicate_test_word = "Test Unique"
    # When the same word is translated and stored
    translated_word = translate_words.translator.translate(duplicate_test_word)
    translate_words.storeTranslation.store(duplicate_test_word,translated_word)
    # Then only one entry for the word is in the database
    data = c.execute("SELECT word from translations")
    words = data.fetchall()
    assert_equal(words.count((duplicate_test_word,)), 1)
    conn.close

# test that a previously translated word is shown on the flashcard page
def test_word_on_flashcard_page():
    conn = sqlite3.connect('data/flashCards.db')
    c = conn.cursor()
    # Given a user is on the flashcard URL
    # When the page loads
    rv = web.get('/flashCards?', follow_redirects=True)
    # Then a German word is on the page
    # And the word is in the database
    c.execute("SELECT word from translations")
    flash_card_words = c.fetchall()
    i = 0
    for word in flash_card_words:
        flash_card_word = word[0]
        flash_card_word_bytes = flash_card_word.encode('utf-8')
        if flash_card_word_bytes in rv.data:
            i += 1
        else:
            pass
    assert_greater(i, 0)
    conn.close

    # test that a translation is shown on the flashcard page
    def test_translation_on_flashcard_page():
        conn = sqlite3.connect('data/flashCards.db')
        c = conn.cursor()
        # Given a user is on the flashcard URL
        # When the page loads
        rv = web.get('/flashCards?', follow_redirects=True)
        # Then translation is on the page
        # And the translation is in the database
        c.execute("SELECT translation from translations")
        flash_card_translations = c.fetchall()
        i = 0
        for translation in flash_card_translations:
            flash_card_translation = translation[0]
            flash_card_translation_bytes = flash_card_translation.encode('utf-8')
            if flash_card_translation_bytes in rv.data:
                i += 1
            else:
                pass
        assert_greater(i, 0)
        # and the translation is accurate
