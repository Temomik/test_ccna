from tkinter import *
import tkinter as tk
from PIL import ImageTk, Image
from random import randint

def hideAll():
    global questionsLabel,buttons,imageCount,imagesTest
    for i in buttons:
        i.pack_forget()
    for i in range(imageCount):
        imagesTest[i].pack_forget()
    questionsLabel.pack_forget()

def showAll():
    global questionsLabel,buttons,imageCount,imagesTest
    questionsLabel.pack()
    for i in range(imageCount):
        imagesTest[i].pack()
    for i in buttons:
        i.pack()

explainState = 0
def showExplain(event):
    global explainState
    if explainState == 1:
        explainLabel.pack_forget()
        showAll()
        explainState = 0
    else:
        hideAll()
        explainState = 1
        explainLabel.pack()

def handleString(string,count = 40):
    splitted = string.split(" ")
    buff = 0
    outStr = ""
    for i in splitted:
        if buff + len(i) <= count:
            outStr += i 
            outStr += " "
            buff += len(i)
        else:
            outStr += "\n" + i + " "
            buff = 0
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

def skip(ecent):
    onRightAnwer()
def onRightAnwer():
    global questionsLabel,buttons,root,selectArray,rightArray,explainLabel,imagesTest,imageCount
    [button.destroy() for button in buttons]
    [imagesTest[it].pack_forget() for it in range(imageCount)]
    # panel.destroy()
    imageCount = 0
    buttons.clear()
    selectArray.clear()
    rightArray.clear()

    answersBuff = []
    isExplain = False
    explainText = ""
    answersText = ""
    while 1:
        line = data.readline()
        if "<next>" in line:
            break
        if isExplain or "<explain>" in line:
            isExplain = True
            explainText += line.replace("<explain>","")
            continue
        if "<question>" in line:
            questionsLabel.destroy()
            questionsLabel = tk.Label(root, text=handleString(line.replace("<question>",""),70))
            questionsLabel.pack(side=tk.TOP)
            questionsLabel.config(font=("Consoles", 30))
            continue
        if "<image>" in line:
            imgResized = Image.open(line.replace("<image>","").replace("\n",""))
            # tmpImg = tk.Label(root,image=ImageTk.PhotoImage(imgResized))
            # tmpImg.pack(side="bottom", fill="both", expand="yes")
            imagesTest[imageCount].pack()
            image = Image.open(line.replace("<image>","").replace("\n",""))
            img2 = ImageTk.PhotoImage(image)
            imagesTest[imageCount].configure(image=img2)
            imagesTest[imageCount].image = img2
            imageCount += 1
            # img = ImageTk.PhotoImage(Image.open("hello.jpg"))
            # panel = tk.Label(root,image=img)
            # panel.pack(side="bottom", fill="both", expand="yes")
            # imagesTest.append(tmpImg)
            continue
        answersBuff.append(line)
    while len(answersBuff) > 0:
        num = randint(0,len(answersBuff) - 1)
        tmpButton = []
        line = answersBuff[num]
        if "<answer>" in line:
            rightArray.append(len(buttons))
            answersText += line + "\n"
        handledLine = handleString(line.replace('\n','').replace("<answer>",""))
        tmpButton = tk.Button(root , text=handledLine, command= lambda buttonNum = len(buttons): select(buttonNum),fg = "black")
        tmpButton.config(width = 100)
        tmpButton.config(font=("Consoles", 30))
        tmpButton.pack(side=tk.TOP)
        buttons.append(tmpButton)
        answersBuff.remove(answersBuff[num])

    explainLabel.destroy()
    explainLabel = tk.Label(root, text= "Explain\n " + handleString(explainText.replace("\n","") + "\n\n\n" + answersText,70))
    explainLabel.pack(side=tk.TOP)
    explainLabel.config(font=("Consoles", 30))
    explainLabel.pack_forget()

def next(event):
    global selectArray,rightArray
    if len(selectArray) != len(rightArray):
        return
    for it in selectArray:
        if it not in rightArray:
            return
    onRightAnwer()

root = tk.Tk()
buttons = []
imagesTest = []
data = open("questions.txt", "r")
root.bind('<Return>', next)
root.bind('<space>', next)
root.bind('e',showExplain)
root.bind('s',skip)
root.attributes("-fullscreen", True)

img = ImageTk.PhotoImage(Image.open("hello.jpg"))
for i in range(5):
    imagesTest.append(tk.Label(root,image=img))
imagesTest[0].pack(side="bottom",fill="both", expand="yes")
imageCount = 1;
topSpace = tk.Label(root, text="\n")
topSpace.pack(side=tk.TOP)

questionsLabel = tk.Label(root, text="Press Enter to start")
questionsLabel.pack(side=tk.TOP)
explainLabel = tk.Label(root,text="")
explainLabel.pack(side=tk.TOP)
# startButton= tk.Button(root, text="start")
# startButton.pack(side=tk.TOP)
# buttons.append(startButton)
root.mainloop()


# data = open("questions.txt", "r")
# [print(data.readline()) for i in range(3)]