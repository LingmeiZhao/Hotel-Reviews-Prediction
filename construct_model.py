import pandas as pd
import numpy as np

def construct_matrix(words, reviews):
    result = [ ]
    for review in reviews:
        vec = [ review.find(word) >= 0 for word in words ]
        result.append(vec)
    return np.array(result)

df = pd.read_csv("hotel_reviews5.csv")
word_importance = pd.read_csv("word_importance.csv")
word_importance = word_importance[word_importance["freq"] > 100]
word_importance = word_importance.sort_values(by = "chi_sq", ascending = False)
words = word_importance["word"][0:500].tolist()

mat = construct_matrix(words, df["reviews.text"].tolist())
mat = mat.astype(np.int)

data = pd.DataFrame(mat, columns = words)
data["rating"] = df["reviews.rating"]
data["rating_binary"] = df["reviews.rating"] >= 3
