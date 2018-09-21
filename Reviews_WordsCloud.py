import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt 

df = pd.read_csv("word_importance.csv").dropna()

words = df["word"].tolist()
frequency = df["freq"].tolist()
words_dic ={ }
for i in range(len(words)):
    words_dic[words[i]]= frequency[i]


text=" ".join(list(words_dic.keys()))
wc=WordCloud(background_color = 'white',width=1000, height=800).generate(text)
wc.to_file('reviewsCloud.jpg')
plt.axis('off')
plt.imshow(wc)



