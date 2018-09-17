import pandas as pd
pd.options.display.max_rows = 9999
pd.options.display.max_columns = 9999
df = pd.read_csv("hotel_reviews2.csv")
data = df[(df["title_lang"] == "en") & (df["text_lang"] == "en")]
data = data[["categories", "city", "latitude", "longitude", "province", "reviews.text", "reviews.title"]]

states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY", "AS", "DC", "FM", "GU", "MH", "MP", "PW", "PR", "VI", "AE", "AA", "AE", "AE", "AE", "AP"]

states_set = set(states)

filter_column = []
province = data["province"].tolist()
filter_column = [ (i in states_set) for i in province]
data = data[filter_column]
data.to_csv("hotel_reviews3_english.csv", index = False)

categories_column = data["categories"].tolist()
categories = { }
for item in categories_column:
    for i in item.split(','):
        if i in categories:
            categories[i] += 1
        else:
            categories[i] = 1
print(categories)
