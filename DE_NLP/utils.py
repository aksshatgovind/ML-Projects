import re
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import cmudict
import string

import ssl
import os

ssl._create_default_https_context = ssl._create_unverified_context      #Bypass SSL verification

nltk_data_dir = os.path.expanduser('~/nltk_data')

if not os.path.exists(nltk_data_dir):
    os.makedirs(nltk_data_dir)

nltk.download('punkt', download_dir=nltk_data_dir)                      #Punkt tokenizer models, which are required for tokenization
nltk.download('cmudict', download_dir=nltk_data_dir)


class SentimentAnalyzer:
    def __init__(self, positive_words, negative_words):
        self.positive_words = self.load_words(positive_words)
        self.negative_words = self.load_words(negative_words)

    def load_words(self, file_path):
        with open(file_path, 'r', encoding='latin-1') as file:
            return set(file.read().splitlines())

    def analyze_sentiment(self, text):
        tokens = word_tokenize(text)                                                                        #Text tokens

        positive_score = sum(1 for token in tokens if token.lower() in self.positive_words)

        negative_score = sum(1 for token in tokens if token.lower() in self.negative_words)

        polarity_score = (positive_score - negative_score) / (positive_score + negative_score + 0.000001)

        subjectivity_score = (positive_score + negative_score) / (len(tokens) + 0.000001)

        return positive_score, negative_score, polarity_score, subjectivity_score

class StopWordsCleaner:
    def __init__(self, stopwords):
        self.stop_words = set()
        with open(stopwords, 'r', encoding='utf-8') as f:
            for line in f:
                stop_word = line.split('|')[0].strip().upper()                  #Extract stop word (before "|" if present)
                self.stop_words.add(stop_word)

    def clean_text(self, text):
        cleaned_text = text
        for stop_word in self.stop_words:
            pattern = r'\b' + re.escape(stop_word) + r'\b'                          #Find matching word, REGEX

            cleaned_text = re.sub(pattern, '', cleaned_text, flags=re.IGNORECASE)   #Remove stop words
        return cleaned_text.strip()


class WordSearch:
    def __init__(self, file):
        self.filename = file

    def search_word(self, word):
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                content = file.read()
                occur = content.lower().count(word.lower())
                return occur
        except FileNotFoundError:
            print(f"File '{self.filename}' not found.")
            return -1

class ReadabilityAnalyzer:
    def __init__(self):
        self.punctuation = set(['.', '!', '?'])

    def count_sentences(self, text):
        sentences = sent_tokenize(text)
        return len(sentences)

    def count_words(self, text):
        words = word_tokenize(text)
        return len(words)

    def count_complex_words(self, text):
        cmudict.ensure_loaded()  
        complex_words = 0
        for word in word_tokenize(text):
            syllables = self.count_syllables(word)
            if syllables >= 3:
                complex_words += 1
        return complex_words

    def count_syllables(self, word):
        try:
            return [len(list(y for y in x if y[-1].isdigit())) for x in cmudict.dict()[word.lower()]][0]
        except KeyError:
            return 0

    def calculate_readability(self, text):
        num_sentences = self.count_sentences(text)
        num_words = self.count_words(text)
        num_complex_words = self.count_complex_words(text)

        avg_sentence_length = num_words / num_sentences

        if num_words > 0:
            percent_complex_words = (num_complex_words / num_words) * 100
        else:
            percent_complex_words = 0

        fog_index = 0.4 * (avg_sentence_length + percent_complex_words)

        return avg_sentence_length, percent_complex_words, fog_index

class TextAnalyzer:
    def __init__(self, stopwords_file):
        self.stop_words = self.load_stopwords(stopwords_file)
        self.punctuation = set(string.punctuation)

    def load_stopwords(self, stopwords_file):
        with open(stopwords_file, 'r', encoding='utf-8') as file:
            return set(word.strip().lower() for word in file)

    def count_sentences(self, text):
        sentences = sent_tokenize(text)
        return len(sentences)

    def count_words(self, text):
        words = word_tokenize(text)
        return len(words)

    def count_syllables(self, word):
        if word.endswith(("es", "ed")):
            return 0

        vowels = 'aeiouy'
        num_syllables = sum(word.lower().count(vowel) for vowel in vowels)

        for i in range(len(word)-1):
            if word[i:i+2] in ['ai', 'au', 'ay', 'ea', 'ee', 'ei', 'eu', 'ey', 'oa', 'oe', 'oi', 'oo', 'ou', 'oy']:
                num_syllables -= 1

        if word.endswith('e'):
            num_syllables -= 1

        num_syllables = max(num_syllables, 1)
        
        return num_syllables
    
    def count_cleaned_words(self, text):
        cleaned_words = []
        for word in word_tokenize(text):
            word = ''.join(ch for ch in word if ch not in self.punctuation)
            if word.lower() not in self.stop_words and word:
                cleaned_words.append(word)
        return cleaned_words

    def find_complex_words(self, text):
        complex_words = []
        for word in word_tokenize(text):
            if self.count_syllables(word) > 2:
                complex_words.append(word)
        return complex_words

    def calculate_average_word_length(self, text):
        words = self.count_cleaned_words(text)
        total_characters = sum(len(word) for word in words)
        total_words = len(words)
        if total_words > 0:
            average_word_length = total_characters / total_words
        else:
            average_word_length = 0
        return average_word_length

    def analyze_text(self, text):
        num_sentences = self.count_sentences(text)
        num_words = self.count_words(text)

        avg_words_per_sentence = num_words / num_sentences if num_sentences > 0 else 0

        complex_words = self.find_complex_words(text)

        syllable_per_word = sum(self.count_syllables(word) for word in word_tokenize(text)) / num_words

        num_cleaned_words = len(self.count_cleaned_words(text))

        average_word_length = self.calculate_average_word_length(text)

        return avg_words_per_sentence, complex_words, syllable_per_word, num_cleaned_words, average_word_length

class PersonalPronounCounter:
    def __init__(self):
        self.pattern = re.compile(r'\b(?:I|we|my|ours|us)\b', flags=re.IGNORECASE)

    def count_personal_pronouns(self, text):
        matches = self.pattern.findall(text)

        count = len(matches)

        return count