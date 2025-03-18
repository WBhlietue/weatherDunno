import math
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

import server
K = 3

db = server.db
cur = db.cursor()
cur.execute("select * from movie")
data = cur.fetchall()

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

def ReadData():
     global data
     cur.execute("select * from movie")
     data = cur.fetchall()

def Start(findDatas):
    distances = []
    datas = [findDatas[0], findDatas[2]]
    cur.execute(f'select * from movie')
    for i in cur.fetchall():
        distances.append(GetDistance(datas,[float(i[1]), i[2]], i[0], i[3]))
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

def OpenNewWindow1(result,data):
    new_window = tk.Toplevel(root)  
    new_window.title("Dunno")
    new_window.geometry("300x200")
    res = [f"Manhattan: {result[0]}", f"Euclidean: {result[1]}"]

    label = tk.Label(new_window, text="\n".join(res))
    label.pack(pady=20)
    def SaveE():
        cur.execute(f"insert into movie (rating, name, duration, genre) values ({data[0]}, '{data[1]}', {data[2]}, '{result[1]}')")
        db.commit()
        messagebox.showinfo("Save", "Saved")
        ReadData()
        Close()
    def SaveM():
        cur.execute(f"insert into movie (rating, name, duration, genre) values ({data[0]}, '{data[1]}', {data[2]}, '{result[0]}')")
        db.commit()
       
        messagebox.showinfo("Save", "Saved")
        ReadData()
        Close()
    def Close():
        new_window.destroy()
    btn1 = tk.Button(new_window, text="Save with Euclidean", command=SaveE)
    btn1.pack(pady=10)
    btn3 = tk.Button(new_window, text="Save with Manhattan", command=SaveM)
    btn3.pack(pady=10)
    btn2 = tk.Button(new_window, text="Close", command=Close)
    btn2.pack(pady=10)

def Click():
    if(len(textInput.get()) == 0 or len(textInput2.get()) == 0 or len(textInput3.get()) == 0 or len(textInput4.get()) == 0):
        messagebox.showwarning("Input", "Please fill all fields")
        return
    cur.execute(f"select genre from movie where name = {textInput2.get()}")
    genre = cur.fetchall()
    if(len(genre) != 0):
        messagebox.showinfo("Result", f"Movie already exists, {genre[0][0]}")
        return
    print(genre)
    global K
    print(len(data))
    K = int(textInput4.get())
    if(K > len(data)):
        messagebox.showwarning("Input", "K too big")
        return 
    result = Start([float(textInput.get()), textInput2.get(), float(textInput3.get())])
    OpenNewWindow1(result,[float(textInput.get()), textInput2.get(), float(textInput3.get())])

def Show():
    root2 = tk.Tk()
    root2.title("Table Display")

    def display_table(root, data, headers):
        tree = ttk.Treeview(root, columns=headers, show="headings")
        for header in headers:
            tree.heading(header, text=header)
        for row in data:
            tree.insert("", "end", values=row)
        tree.pack(fill="both", expand=True)  
    headers = ["Name", "Rating", "Duration", "Genre"]
    display_table(root2, data, headers)



root = tk.Tk()
root.title("Dunno")
root.geometry("250x400")
def validate_input(new_value):
    try:
        float(new_value)  
        return True
    except ValueError:
        return new_value == ""

validate_cmd = root.register(validate_input)

def validate_input2(new_value):
    try:
        int(new_value)  
        return True
    except ValueError:
        return new_value == ""

validate_cmd2 = root.register(validate_input2)

label = tk.Label(root, text="Rating")
label.place(x=50, y=50)
textInput = tk.Entry(
    root,
    width=15,
    validate="key",  
    validatecommand=(validate_cmd, "%P"), 
)
textInput.place(x=130, y=50)

label2 = tk.Label(root, text="Name")
label2.place(x=50, y=100)
textInput2 = tk.Entry(
    root,
    width=15,
)
textInput2.place(x=130, y=100)

label3 = tk.Label(root, text="Duration")
label3.place(x=50, y=150)
textInput3 = tk.Entry(
    root,
    width=15,
    validate="key",  
    validatecommand=(validate_cmd, "%P"), 
)
textInput3.place(x=130, y=150)

label4 = tk.Label(root, text="K")
label4.place(x=50, y=200)
textInput4 = tk.Entry(
    root,
    width=15,
    validate="key",  
    validatecommand=(validate_cmd2, "%P"), 
)
textInput4.place(x=130, y=200)

root.option_add("*Font", ("Arial", 14))
button3 = tk.Button(root, text="Check", command=Click,width=10)
button3.place(x = 75,y = 300)
button4 = tk.Button(root, text="ShowData", command=Show,width=10)
button4.place(x = 75,y = 350)


root.mainloop()