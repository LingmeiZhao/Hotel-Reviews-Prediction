from langdetect import detect
import pandas as pd

pd.options.display.max_rows = 9999
pd.options.display.max_columns = 9999

def detect_language(text_list):
    result = [ ]
    for item in text_list:
        try:
            result.append(detect(item))
        except:
            print(item)
            result.append("Unknown")
    return result

df = pd.read_csv("hotel_reviews.csv")
df = df[["categories", "city", "country",
         "latitude", "longitude", "name",
         "province", "reviews.text", "reviews.title", "reviews.rating"]] 
df = df.dropna(subset = ["latitude", "longitude"])
df = df.dropna(subset = ["reviews.text", "reviews.title", "reviews.rating"])
reviews_title_lang = detect_language(df["reviews.title"].tolist())
reviews_text_lang = detect_language(df["reviews.text"].tolist())

data = df.copy()
data["title_lang"] = reviews_title_lang
data["text_lang"] = reviews_text_lang

data.to_csv("hotel_reviews2.csv", index = False)