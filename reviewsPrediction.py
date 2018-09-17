import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from wordcloud import WordCloud

pd.options.display.max_rows = 9999
pd.options.display.max_columns = 9999

df = pd.read_csv("hotel_reviews3_english.csv")

num_list1 = df["province"]
province_count=num_list1.value_counts()
province_index = province_count.index[0:10]
province_frequency = province_count.values[0:10]
color_list = ['peru', 'dodgerblue', 'lightsalmon', 'orange', 'chartreuse', 'red', 'gray', 'skyblue', 'fuchsia', 'olive']

plt.rcParams['figure.dpi'] = 300
plt.bar(province_index, province_frequency,color=color_list)
plt.xlabel("province", fontsize=10)
plt.ylabel("reviews amount", fontsize=10)
plt.title("The top ten provinces with most hotel reviews", fontsize=15)
plt.savefig("hotelReviews_province.jpg")

num_list2 = df["city"]
city_count=num_list2.value_counts()[0:10]
city_index = city_count.index
city_frequency = city_count.values

plt.bar(city_index, city_frequency ,color=color_list)
plt.xlabel("city", fontsize=10)
plt.ylabel("reviews amount", fontsize=10)
plt.title("The top ten city with most hotel reviews", fontsize=15)
plt.savefig("hotelReviews_city.jpg")

categories_column = df["categories"].tolist()
categories = { }
for item in categories_column:
    for i in item.split(','):
        if i in categories:
            categories[i] += 1
        else:
            categories[i] = 1
print(categories)

#Hotel_number = categories['Hotels']+categories['Hotel']
#del categories['Hotels']
#categories['Hotel']=Hotel_number
#print(categories)

text=" ".join(categories.keys())
wc=WordCloud(background_color = 'white',width=1000, height=1000).generate(text)
wc.to_file('wordCloud.jpg')
plt.imshow(wc)
plt.axis('off')
plt.show()


