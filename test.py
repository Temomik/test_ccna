import tkinter as tk
from PIL import ImageTk, Image

def nextImage():
    global panel, it
    it += 2
    img2 = ImageTk.PhotoImage(Image.open("imgs/" + str(it) + ".png"))
    panel.configure(image=img2)
    panel.image = img2


def handleString(string,count = 40):
    tmpStr =[]
    [tmpStr.append(string[i:i+count] + '\n') for i in range(0, len(string), count)]
    outStr = ""
    for it in tmpStr:
        outStr = outStr + str(it)
    return outStr

def next():
    global questionsLabel,buttons,root,panel
    [button.destroy() for button in buttons]
    # panel.destroy()
    panel.pack_forget()
    while(1):
        line = data.readline()
        if("<next>" in line):
            return
        if("<question>" in line):
            questionsLabel.destroy()
            questionsLabel = tk.Label(root, text=handleString(line,100))
            questionsLabel.pack(side=tk.TOP)
            continue
        if("<image>" in line):
            panel.pack()
            image = Image.open(line.replace("<image>","").replace("\n",""))
            img2 = ImageTk.PhotoImage(image)
            panel.configure(image=img2)
            panel.image = img2
            continue
        
        tmpButton = []
        newLine = handleString(line.replace('\n',''))
        if "<answer>" in line :
            tmpButton = tk.Button(root , text=newLine, command=next)
        else:
            tmpButton = tk.Button(root, text=newLine)
        tmpButton.config( width = 100)
        tmpButton.pack(side=tk.TOP)
        buttons.append(tmpButton)
buttons = []
data = open("questions.txt", "r")
root = tk.Tk()

root.attributes("-fullscreen", True)

img = ImageTk.PhotoImage(Image.open("imgs/75.png"))
panel = tk.Label(root,image=img)
panel.pack(side="bottom", fill="both", expand="yes")

topSpace = tk.Label(root, text="\n\n\n")
topSpace.pack(side=tk.TOP)

questionsLabel = tk.Label(root, text="Hello, world!")
questionsLabel.pack(side=tk.TOP)

startButton= tk.Button(root, text="start", command=next)
startButton.pack(side=tk.TOP)
buttons.append(startButton)
root.mainloop()


# data = open("questions.txt", "r")
# [print(data.readline()) for i in range(3)]