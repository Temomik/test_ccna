import tkinter as tk
from PIL import ImageTk, Image

def nextImage():
    global panel, it
    it += 2
    img2 = ImageTk.PhotoImage(Image.open("imgs/" + str(it) + ".png"))
    panel.configure(image=img2)
    panel.image = img2


def handleString(string):
    tmpStr =[]
    count = 40
    [tmpStr.append(string[i:i+count] + '\n') for i in range(0, len(string), count)]
    outStr = ""
    for it in tmpStr:
        outStr = outStr + str(it)
    return outStr

def next():
    global questionsLabel,buttons,root
    [button.destroy() for button in buttons]
    while(1):
        line = data.readline()
        if("<next>" in line):
            return
        if("<question>" in line):
            questionsLabel.text = line
        
        tmpButton = []
        newLine = handleString(line)
        if "<answer>" in line :
            tmpButton = tk.Button(root,width=40,height=10 , text=newLine, command=next)
        else:
            tmpButton = tk.Button(root,width=40,height=10, text=newLine)
        tmpButton.pack(side=tk.TOP)
        buttons.append(tmpButton)
buttons = []
data = open("questions.txt", "r")
root = tk.Tk()

root.attributes("-fullscreen", True)
# img = ImageTk.PhotoImage(Image.open("imgs/75.png"))
# panel = tk.Label(root, image=img)
# panel.pack(side="bottom", fill="both", expand="yes")
it = 3
questionsLabel = tk.Label(root, text="Hello, world!")
questionsLabel.pack(side=tk.TOP)

startButton= tk.Button(root, text="start", command=next)
startButton.config( height = 100)
startButton.config( width = 100)
startButton.pack(side=tk.TOP)
buttons.append(startButton)
root.mainloop()


# data = open("questions.txt", "r")
# [print(data.readline()) for i in range(3)]