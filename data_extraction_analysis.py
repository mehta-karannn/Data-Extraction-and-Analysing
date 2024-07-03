import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
import nltk
import pyphen
nltk.download('punkt')

# Define paths
base_path = os.path.expanduser("~/Desktop/Assignment")
input_file_path = os.path.join(base_path, "Input.xlsx")
articles_dir = os.path.join(base_path, "articles")
output_file_path = os.path.join(base_path, "output.xlsx")

# Create articles directory if it doesn't exist
os.makedirs(articles_dir, exist_ok=True)

# Load input data
input_data = pd.read_excel(input_file_path)
urls = input_data['URL']

# Function to extract article text
def extract_article_text(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.find('h1').get_text() if soup.find('h1') else ''
        paragraphs = soup.find_all('p')
        article_text = ' '.join([p.get_text() for p in paragraphs])
        return title, article_text
    except Exception as e:
        print(f"Error extracting {url}: {e}")
        return "", ""

# Extract and save article text
for idx, url in enumerate(urls):
    title, article_text = extract_article_text(url)
    file_name = f"{input_data.URL_ID[idx]}.txt"
    file_path = os.path.join(articles_dir, file_name)
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(f"{title}\n{article_text}")

# Load extracted texts
article_texts = {}
for filename in os.listdir(articles_dir):
    file_path = os.path.join(articles_dir, filename)
    with open(file_path, 'r', encoding='utf-8') as file:
        article_texts[filename] = file.read()

# Function to count syllables
def count_syllables(word):
    dic = pyphen.Pyphen(lang='en')
    hyphenated = dic.inserted(word)
    return max(1, hyphenated.count('-') + 1)

# Function to perform text analysis
def analyze_text(text):
    blob = TextBlob(text)
    sentences = blob.sentences

    positive_score = sum([sentence.sentiment.polarity for sentence in sentences if sentence.sentiment.polarity > 0])
    negative_score = sum([sentence.sentiment.polarity for sentence in sentences if sentence.sentiment.polarity < 0])
    polarity_score = blob.sentiment.polarity
    subjectivity_score = blob.sentiment.subjectivity
    avg_sentence_length = sum([len(sentence.words) for sentence in sentences]) / len(sentences) if sentences else 0
    complex_words = [word for word in blob.words if count_syllables(word) > 2]
    percentage_complex_words = len(complex_words) / len(blob.words) * 100 if blob.words else 0
    fog_index = 0.4 * (avg_sentence_length + percentage_complex_words)
    avg_words_per_sentence = len(blob.words) / len(sentences) if sentences else 0
    complex_word_count = len(complex_words)
    word_count = len(blob.words)
    syllables_per_word = sum([count_syllables(word) for word in blob.words]) / len(blob.words) if blob.words else 0
    personal_pronouns = sum([1 for word in blob.words if word.lower() in ['i', 'we', 'my', 'ours', 'us']])
    avg_word_length = sum([len(word) for word in blob.words]) / len(blob.words) if blob.words else 0

    return {
        'POSITIVE SCORE': positive_score,
        'NEGATIVE SCORE': negative_score,
        'POLARITY SCORE': polarity_score,
        'SUBJECTIVITY SCORE': subjectivity_score,
        'AVG SENTENCE LENGTH': avg_sentence_length,
        'PERCENTAGE OF COMPLEX WORDS': percentage_complex_words,
        'FOG INDEX': fog_index,
        'AVG NUMBER OF WORDS PER SENTENCE': avg_words_per_sentence,
        'COMPLEX WORD COUNT': complex_word_count,
        'WORD COUNT': word_count,
        'SYLLABLE PER WORD': syllables_per_word,
        'PERSONAL PRONOUNS': personal_pronouns,
        'AVG WORD LENGTH': avg_word_length
    }

# Perform analysis and compile results
results = []
for url_id, text in article_texts.items():
    analysis_results = analyze_text(text)
    analysis_results['URL_ID'] = url_id.split('.')[0]
    results.append(analysis_results)

# Merge results with input data and save output
output_df = pd.DataFrame(results)
output_df = pd.merge(input_data, output_df, on='URL_ID')
output_df.to_excel(output_file_path, index=False)

print(f"Data extraction and analysis completed successfully. Output saved to {output_file_path}")
