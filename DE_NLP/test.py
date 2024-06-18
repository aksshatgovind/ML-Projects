import os
import pandas as pd
from utils import StopWordsCleaner, SentimentAnalyzer, ReadabilityAnalyzer, TextAnalyzer, PersonalPronounCounter

def extract_parameters(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    #Clean text
    stopwords = 'Stopwords.txt'
    cleaner = StopWordsCleaner(stopwords)
    cleaned_text = cleaner.clean_text(text)

    #Sentiment Analysis
    positive_words = 'positive-words.txt'
    negative_words = 'negative-words.txt'

    sentiment_analyzer = SentimentAnalyzer(positive_words, negative_words)
    positive_score, negative_score, polarity_score, subjectivity_score = sentiment_analyzer.analyze_sentiment(cleaned_text)

    #Readability Analysis
    readability_analyzer = ReadabilityAnalyzer()
    avg_sentence_length, percentage_complex_words, fog_index = readability_analyzer.calculate_readability(cleaned_text)

    #Text Analysis
    text_analyzer = TextAnalyzer(stopwords)
    avg_words_per_sentence, complex_words, syllable_per_word, word_count, avg_word_length = text_analyzer.analyze_text(cleaned_text)

    #Personal Pronoun Count
    pronoun_counter = PersonalPronounCounter()
    personal_pronouns_count = pronoun_counter.count_personal_pronouns(cleaned_text)

    return [positive_score, negative_score, polarity_score, subjectivity_score, 
            avg_sentence_length, percentage_complex_words, fog_index, 
            avg_words_per_sentence, len(complex_words), word_count, 
            syllable_per_word, personal_pronouns_count, avg_word_length]


extracted_articles = 'Extracted_Articles'
url_ids = [file_name.split('.')[0] for file_name in os.listdir(extracted_articles)]


columns = ['URL_ID', 'POSITIVE SCORE', 'NEGATIVE SCORE', 'POLARITY SCORE', 
           'SUBJECTIVITY SCORE', 'AVG SENTENCE LENGTH', 'PERCENTAGE OF COMPLEX WORDS', 
           'FOG INDEX', 'AVG NUMBER OF WORDS PER SENTENCE', 'COMPLEX WORD COUNT', 
           'WORD COUNT', 'SYLLABLE PER WORD', 'PERSONAL PRONOUNS', 'AVG WORD LENGTH']
data = pd.DataFrame(columns=columns)


for url_id in url_ids:
    file = os.path.join(extracted_articles, f"{url_id}.txt")
    param = [url_id] + extract_parameters(file)
    data = data.append(pd.Series(param, index=columns), ignore_index=True)

url_data = pd.read_excel('Input.xlsx')                                             #Contains URL_ID and URL only

data = pd.merge(data, url_data, on='URL_ID', how='left')

data = data[['URL_ID', 'URL', 'POSITIVE SCORE', 'NEGATIVE SCORE', 'POLARITY SCORE', 
             'SUBJECTIVITY SCORE', 'AVG SENTENCE LENGTH', 'PERCENTAGE OF COMPLEX WORDS', 
             'FOG INDEX', 'AVG NUMBER OF WORDS PER SENTENCE', 'COMPLEX WORD COUNT', 
             'WORD COUNT', 'SYLLABLE PER WORD', 'PERSONAL PRONOUNS', 'AVG WORD LENGTH']]


data.to_excel('Article_Sentiments.xlsx', index=False)
