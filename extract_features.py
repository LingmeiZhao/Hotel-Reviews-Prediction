import pandas as pd
import nltk 
from nltk.corpus import stopwords

pd.options.display.max_columns = 9999

def remove_stop_words(words):
    newWords = [ ]
    stop_words_set = set(stopwords.words("english"))
    for word in words:
        if not (word in stop_words_set):
            newWords.append(word)
    return newWords

def get_all_words(reviews):
    all_words = [ ]
    for review in reviews:
        for word in review:
            all_words.append(word)
    all_words = set(all_words)
    all_words = list(all_words)
    all_words = remove_stop_words(all_words)
    return all_words

def get_word_dict(all_words):
    word_dict = { }
    for word in all_words:
        word_dict[word] = 0
    
    for review in reviews:
        for word in review:
            if word in word_dict:
                word_dict[word] += 1
    return word_dict

def is_word_with_letters(word):
    for c in word:
        if c.isalpha():
            pass
        else:
            return False
    return True

def remove_non_letter_word(word_freq):
    words = word_freq["word"].tolist()
    filter_column = [ ]
    for word in words:
        if str(word) == "nan":
            filter_column.append(False)
        else:
            filter_column.append(is_word_with_letters(word))
    return word_freq[filter_column]

def select_by_pos(words, tag):
    tokens = nltk.pos_tag(words)
    selected_words = [ ]
    for token in tokens:
        (w, t) = token
        if t == tag:
            selected_words.append(w)
    return selected_words


df = pd.read_csv("hotel_reviews3_english.csv")

reviews_text = df["reviews.text"].tolist()
reviews_title = df["reviews.title"].tolist()

reviews = [ ]
for i in range(len(df)):
    reviews.append(nltk.word_tokenize(reviews_title[i]) + nltk.word_tokenize(reviews_text[i]))

all_words = get_all_words(reviews)
#selected_words = select_by_pos(all_words, "JJ") + select_by_pos(all_words, "NN")
word_dict = get_word_dict(all_words)

word_dict_keys = list(word_dict.keys())
word_dict_values = [ ]
for key in word_dict_keys:
    word_dict_values.append(word_dict[key])

word_freq = pd.DataFrame({"word":word_dict_keys, "freq":word_dict_values})
word_freq = word_freq.sort_values(by = "freq", ascending = False)

word_freq = remove_non_letter_word(word_freq)

word_freq.to_csv("word_freq.csv", index = False)

df.to_csv("hotel_reviews4.csv", index = False)