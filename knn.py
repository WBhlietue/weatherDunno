import pandas
import math
import tkinter as tk
from tkinter import ttk
import mysql.connector

K = 3

db = mysql.connector.connect(
  host="",
  user="",
  password="",
  database = "dataTan"
)
cursor = db.cursor()
cursor.execute("select * from movie;")
d = cursor.fetchall()
print(d)
data = pandas.read_csv("knn.csv")

def ManhattanDis(list1, list2):
    n = 0
    for i in range(len(list1)):
        n += abs(list1[i] - list2[i])
    return n

def Euclidean(list1, list2):
    n = 0
    for i in range(len(list1)):
        n += math.pow(list1[i] - list2[i], 2)
    return math.sqrt(n)

def GetDistance(list1, list2, name, genre):
    return [ManhattanDis(list1, list2), Euclidean(list1, list2), name, genre]


def Start(findDatas):
    distances = []
    datas = [findDatas[0], findDatas[2]]
    for _, i in data.iterrows():
        distances.append(GetDistance(datas, [i["rating"], i["duration"]], i["name"], i["genre"]))
    sortedDataMantattan = sorted(distances, key=lambda x: x[0], reverse=False)
    sortedDataEuclidean = sorted(distances, key=lambda x: x[1], reverse=False)
    manhattonResult = {}
    euclideanResult = {}
    for i in range(K):
        manha = sortedDataMantattan[i]
        if(manha[3] in manhattonResult.keys()):
            manhattonResult[manha[3]] += 1
        else:
            manhattonResult[manha[3]] = 1

        euc = sortedDataEuclidean[i]
        if(euc[3] in euclideanResult.keys()):
            euclideanResult[euc[3]] += 1
        else:
            euclideanResult[euc[3]] = 1
    resultManhatton = sorted(manhattonResult, key=lambda x: x[1], reverse=True)[0]
    resultEuclidean = sorted(euclideanResult, key=lambda x: x[1], reverse=True)[0]

    return (resultManhatton, resultEuclidean)
    

# findDatas = [7.4, "Barbie", 114]

def Click():
    result = Start([float(textInput.get(1.0, "end-1c")), textInput2.get(1.0, "end-1c"), float(textInput3.get(1.0, "end-1c"))])
    print(result)

root = tk.Tk()
root.title("Dunno")
root.geometry("250x400")

label = tk.Label(root, text="Rating")
label.place(x=50, y=50)
textInput = tk.Text(root, width=10,height=2)
textInput.place(x=130, y=50)

label2 = tk.Label(root, text="Name")
label2.place(x=50, y=100)
textInput2 = tk.Text(root, width=10,height=2)
textInput2.place(x=130, y=100)

label3 = tk.Label(root, text="Duration")
label3.place(x=50, y=150)
textInput3 = tk.Text(root, width=10,height=2)
textInput3.place(x=130, y=150)

root.option_add("*Font", ("Arial", 14))
button3 = tk.Button(root, text="Check", command=Click)
button3.place(x = 75,y = 300)


root.mainloop()