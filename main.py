import tkinter as tk
from tkinter import ttk
import lab1
import lab2 

root = tk.Tk()
root.title("Dunno")
root.geometry("700x400")

root.option_add("*Font", ("Arial", 14))
texts =lab1.texts
headers = lab1.headers[0:-1]
selected_option = []
for i in range(len(headers)):
    selected_option.append(tk.StringVar(value=sorted(texts[i])[0]))
    dropdown = ttk.Combobox(root, values=sorted(texts[i]), textvariable=selected_option[-1], state="readonly")
    dropdown.place(x=400, y=50*(i+1))
    label = tk.Label(root, text=headers[i])
    label.place(x=50, y=50*(i+1))


def OpenNewWindow1(result):
    new_window = tk.Toplevel(root)  
    new_window.title("Dunno")
    new_window.geometry("800x600")
    
    label = tk.Label(new_window, text=result[0].upper())
    label.pack(pady=20)
    text_widget = tk.Text(new_window, wrap=tk.WORD, height=45, width=50,font=("Courier", 14))
    text_widget.insert(tk.END, result[1])
    scrollbar = tk.Scrollbar(new_window)

    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.config(command=text_widget.yview)
    text_widget.config(yscrollcommand=scrollbar.set)

def Click1():
    l = []
    for i in selected_option:
        l.append(i.get())
    res = lab1.Start(l)
    OpenNewWindow1(res)
def Click2():
    l = []
    for i in selected_option:
        l.append(i.get())
    res = lab2.Start(l)
    OpenNewWindow1(res)
def Click3():
    for i in selected_option:
        print(i.get())

button1 = tk.Button(root, text="Lab 1", command=Click1)
button1.place(x = 50,y = 300)
button2 = tk.Button(root, text="Lab 2", command=Click2)
button2.place(x = 150,y = 300)
button3 = tk.Button(root, text="Lab 3", command=Click3)
button3.place(x = 250,y = 300)


root.mainloop()