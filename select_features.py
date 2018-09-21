import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import nltk

def get_word_map(word_freq):
    word = word_freq["word"].tolist()
    freq = word_freq["freq"].tolist()
    word_map = { }
    for i in range(len(word_freq)):
        word_map[word[i]] = freq[i]
    return word_map

def remove_values(df, column_name, value_set):
    filter_column = [ ]
    column = df[column_name].tolist()
    for item in column:
        if item in value_set:
            filter_column.append(False)
        else:
            filter_column.append(True)
    return df[filter_column]
    
def chi_square(word, reviews_text, ratings):
    N = len(reviews_text)
    A = 0
    B = 0
    C = 0
    D = 0
    A = A + 1
    C = C + 1
    for i in range(len(reviews_text)):
        review = reviews_text[i]
        rating = ratings[i]
        if review.find(word) >= 0:
            if rating >= 3: # positive
                A = A + 1
            else:
                B = B + 1
        else:
            if rating >= 3:
                C = C + 1
            else:
                D = D + 1
    chi_sq = (N * (A * D - B * C) ** 2 ) / ((A + C) * (B + D) * (A + B) * (C + D))
    return chi_sq
  
def tagging(df):
    id = range(len(df))
    df["id"] = id
    return df

def get_word_frequency(df, id_list):
    word_dict = { }
    reviews_text = df["reviews.text"].tolist()
    for id in id_list:
        review = reviews_text[id]
        for word in nltk.word_tokenize(review):
            if word in word_dict:
                word_dict[word] += 1
            else:
                word_dict[word] = 1
    word_dict_keys = list(word_dict.keys())
    word_dict_tag = [ nltk.pos_tag(word) for word in word_dict_keys ]
    word_dict_values = [ word_dict[key] for key in word_dict_keys ]
    return pd.DataFrame({"word": word_dict_keys,
                  "tag": word_dict_tag,
                  "freq": word_dict_values})

def select_reviews_by_id(df, id_list):
    reviews_text = df["reviews.text"].tolist()
    return [ reviews_text[id] for id in id_list ]

def column_vec_to_list(matrix):
    result = [ ]
    nrows, ncols = matrix.shape
    for i in range(nrows):
        result.append(matrix[i][0])
    return result

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

def generate_data_file(X, Y, reviews_text, word_importance_train):
    result = []
    words = word_importance_train["word"].tolist()
    for review in reviews_text:
        vec = [ ]
        for word in words:
            if review.find(word) >= 0:
                vec.append(1)
            else:
                vec.append(0)
        result.append(vec)
    df = pd.DataFrame(np.array(result), columns = words)
    df["id"] = column_vec_to_list(X)
    df["rating"] = column_vec_to_list(Y)
    return df
    
    
df = pd.read_csv("hotel_reviews4.csv")
print("len(df) = ", len(df))
max_ratings = df.groupby("name").agg(np.max)["reviews.rating"]
df = remove_values(df, "name", set(max_ratings[max_ratings != 5].index.tolist()))
print("len(df) = ", len(df))
df = tagging(df)
df.to_csv("hotel_reviews5.csv", index = False)

X = df[["id"]].values
Y = df[["reviews.rating"]].values
Y = Y >= 3
Y = Y.astype(np.int)

X_train, X_test, Y_train, Y_test = train_test_split(
        X, Y, test_size=0.33, random_state=42)

word_importance_train = get_word_frequency(df, column_vec_to_list(X_train))


print("calculating chi_sq")
chi_sq_list = [ ]

reviews_text_train = select_reviews_by_id(df,
                                    column_vec_to_list(X_train))
word_list = word_importance_train["word"].tolist()
for word in word_list:
    chi_sq = chi_square(word, reviews_text_train, column_vec_to_list(Y_train))
    chi_sq_list.append(chi_sq)

word_importance_train["chi_sq"] = chi_sq_list
word_importance_train = remove_non_letter_word(word_importance_train)
word_importance_train.to_csv("word_importance_train.csv", index = False)

word_importance_train = pd.read_csv("word_importance_train.csv")
word_importance_train = word_importance_train[word_importance_train["freq"] > 20]
word_importance_train = word_importance_train.sort_values(by = "chi_sq", ascending = False)

print("start generating data file")
generate_data_file(X_train, Y_train, reviews_text_train, word_importance_train[0:500]).to_csv("train.csv", index = False)

reviews_text_test = select_reviews_by_id(df,
                                    column_vec_to_list(X_test))
generate_data_file(X_test, Y_test, reviews_text_test, word_importance_train[0:500]).to_csv("test.csv", index = False)