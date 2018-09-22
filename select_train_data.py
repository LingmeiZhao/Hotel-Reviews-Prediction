import pandas as pd


df = pd.read_csv("train.csv")

df["rating"].value_counts()

df1 = df[df["rating"]==1]
df0 = df[df["rating"]==0]

df2 = df1.sample(frac = 0.2)

df_new = pd.concat([df0,df2])

df_new["rating"].value_counts()

df_new.to_csv("train_new.csv",index=False)