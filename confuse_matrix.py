import pandas as pd
import numpy as np
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt


data = pd.read_csv("prediction.csv")
y_pre = data["x"]

df = pd.read_csv("test.csv")
y = df["rating"]

cm = confusion_matrix(y, y_pre)
print(cm)

labels = [0,1]

def plot_confusion_matrix(cm, title="Confusion Matrix", cmap = plt.cm.binary):
    plt.imshow(cm, interpolation= "nearest", cmap= cmap)
    plt.title(title)
    plt.colorbar()
    xlocations = np.array(range(len(labels)))
    plt.xticks(xlocations,labels)
    plt.yticks(xlocations,labels)
    plt.ylabel("True label")
    plt.xlabel("Predicted label")

np.set_printoptions(precision = 2)
cm_normalized = cm.astype("float")/cm.sum(axis=1)[:, np.newaxis]
print(cm_normalized)
plt.figure(figsize=(12,8),dpi = 120)

ind_array = np.arange(len(labels))
x,y = np.meshgrid(ind_array,ind_array)

for x_val, y_val in zip(x.flatten(),y.flatten()):
    c = cm_normalized[y_val][x_val]
    if(c > 0.01):
        plt.text(x_val,y_val, "%0.2f" %(c,), color="red", fontsize=7, va="center",ha="center")

tick_marks = np.array(range(len(labels))) + 0.5       
plt.gca().set_xticks(tick_marks,minor = True)
plt.gca().set_yticks(tick_marks,minor = True)
plt.gca().xaxis.set_ticks_position("none")
plt.gca().yaxis.set_ticks_position("none")
plt.grid(True, which ="minor",linestyle="-")
plt.gcf().subplots_adjust(bottom=0.15)

plot_confusion_matrix(cm_normalized,title= "Normalized Confusion Matrix")
plt.savefig("Normal Confusion Matrix.jpg")


plot_confusion_matrix(cm,title="Confusion Matrix") 
plt.show()