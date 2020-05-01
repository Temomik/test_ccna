import tkinter as tk
from PIL import ImageTk, Image
from random import randint

def nextImage():
    global panel, it
    it += 2
    img2 = ImageTk.PhotoImage(Image.open("imgs/" + str(it) + ".png"))
    panel.configure(image=img2)
    panel.image = img2


def handleString(string,count = 40):
    splitted = string.split(" ")
    buff = 0
    outStr = ""
    for i in splitted:
        if buff <= count:
            outStr += i 
            outStr += " "
            buff += len(i)
        else:
            outStr += "\n"
            buff = 0

    # tmpStr =[]
    # for i in range(0, len(string), count):  
    #     while i + count < len(string) and string[i+count] != " ":
    #         i +=1
    #     tmpStr.append(string[i:i+count] + '\n')

    # outStr = ""
    # for it in tmpStr:
    #     outStr = outStr + str(it)
    return outStr

selectArray = []
rightArray = []
def select(num):
    # print(num)
    if num in selectArray:
        selectArray.remove(num)
        buttons[num].config( fg = "black")
    else:
        selectArray.append(num)
        buttons[num].config( fg = "red")

def next(event):
    global questionsLabel,buttons,root,panel,selectArray,rightArray
    if len(selectArray) != len(rightArray):
        return
    for it in selectArray:
        if it not in rightArray:
            return

    [button.destroy() for button in buttons]
    # panel.destroy()
    buttons.clear()
    selectArray.clear()
    rightArray.clear()
    panel.pack_forget()
    
    answersBuff = []

    while 1:
        line = data.readline()
        if("<next>" in line):
            break
        if("<question>" in line):
            questionsLabel.destroy()
            questionsLabel = tk.Label(root, text=handleString(line.replace("<question>",""),70))
            questionsLabel.pack(side=tk.TOP)
            questionsLabel.config(font=("Consoles", 30))
            continue
        if("<image>" in line):
            panel.pack()
            image = Image.open(line.replace("<image>","").replace("\n",""))
            img2 = ImageTk.PhotoImage(image)
            panel.configure(image=img2)
            panel.image = img2
            continue
        answersBuff.append(line)
    while len(answersBuff) > 0:
        num = randint(0,len(answersBuff) - 1)
        tmpButton = []
        line = answersBuff[num]
        if "<answer>" in line:
            rightArray.append(len(buttons))
        handledLine = handleString(line.replace('\n',''))
        tmpButton = tk.Button(root , text=handledLine.replace("<answer>",""), command= lambda buttonNum = len(buttons): select(buttonNum),fg = "black")
        tmpButton.config(width = 100)
        tmpButton.config(font=("Consoles", 30))
        tmpButton.pack(side=tk.TOP)
        buttons.append(tmpButton)
        answersBuff.remove(answersBuff[num])

buttons = []
data = open("questions.txt", "r")
root = tk.Tk()
root.bind('<Return>', next)
root.bind('<space>', next)
root.attributes("-fullscreen", True)

img = ImageTk.PhotoImage(Image.open("hello.jpg"))
panel = tk.Label(root,image=img)
panel.pack(side="bottom", fill="both", expand="yes")

topSpace = tk.Label(root, text="\n\n\n")
topSpace.pack(side=tk.TOP)

questionsLabel = tk.Label(root, text="Press Enter to start")
questionsLabel.pack(side=tk.TOP)

# startButton= tk.Button(root, text="start")
# startButton.pack(side=tk.TOP)
# buttons.append(startButton)
root.mainloop()


# data = open("questions.txt", "r")
# [print(data.readline()) for i in range(3)]