from tkinter import *
import tkinter as tk
from PIL import ImageTk, Image
from random import randint
from datetime import datetime
import os
from tkinter import filedialog as fd 

basewidth = 500   #image scale
lineBreak = 70
fontSize = 25

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
    if num in selectArray:
        selectArray.remove(num)
        buttons[num].config( fg = "black")
    else:
        selectArray.append(num)
        buttons[num].config( fg = "red")

def skip(event):
    onRightAnwer()

currentQuestions = 0
def returnPrev(event):
    global data,currentQuestions
    data.seek(0)
    startFrom(currentQuestions-1)
    onRightAnwer()

def onRightAnwer():
    global questionsLabel,buttons,root,selectArray,rightArray,explainLabel
    global imagesTest,imageCount,isExplain,saveLine
    global isCurrentSaved,data,isFirstStart,startQuestionsNum
    global currentQuestions,basewidth
    if isFirstStart:
        isFirstStart = False
        tmpBuff = startQuestionsNum.get()
        firstNum = 0
        try:
            firstNum = int(tmpBuff.strip())
        except:
            pass    
        startFrom(firstNum)
    [button.destroy() for button in buttons]
    [imagesTest[it].pack_forget() for it in range(imageCount)]
    # panel.destroy()
    imageCount = 0
    buttons.clear()
    selectArray.clear()
    rightArray.clear()

    answersBuff = []
    isCurrentSaved = False
    isExplain = False
    explainText = ""
    answersText = ""
    saveLine = ""
    while 1:
        line = data.readline()
        if not line:
            data.seek(0)
            continue
        saveLine += str(line)
        if "<next>" in line:
            break
        if isExplain or "<explain>" in line:
            isExplain = True
            explainText += line.replace("<explain>","")
            continue
        if "<question>" in line:
            questionsLabel.destroy()
            try:
                currentQuestions = int(line.replace("<question>","").split(".")[0])
            except:
                pass
            questionsLabel = tk.Label(root, text=handleString(line.replace("<question>",""),lineBreak))
            questionsLabel.pack(side=tk.TOP)
            questionsLabel.config(font=("Consoles", fontSize))
            continue
        if "<image>" in line:
            imgResized = Image.open(line.replace("<image>","").replace("\n",""))
            wpercent = (basewidth/float(imgResized.size[0]))
            hsize = int((float(imgResized.size[1])*float(wpercent)))
            imgResized = imgResized.resize((basewidth,hsize), Image.ANTIALIAS)
            imagesTest[imageCount].pack()
            img2 = ImageTk.PhotoImage(imgResized)
            imagesTest[imageCount].configure(image=img2)
            imagesTest[imageCount].image = img2
            imageCount += 1
            continue
        answersBuff.append(line)
    while len(answersBuff) > 0:
        num = randint(0,len(answersBuff) - 1)
        tmpButton = []
        line = answersBuff[num]
        if "<answer>" in line:
            rightArray.append(len(buttons))
            answersText += line + "\n"
        handledLine = handleString(line.replace('\n','').replace("<answer>",""),lineBreak)
        tmpButton = tk.Button(root , text=handledLine, command= lambda buttonNum = len(buttons): select(buttonNum),fg = "black")
        tmpButton.config(width = 100)
        tmpButton.config(font=("Consoles", fontSize))
        tmpButton.pack(side=tk.TOP)
        buttons.append(tmpButton)
        answersBuff.remove(answersBuff[num])

    explainLabel.destroy()
    explainLabel = tk.Label(root, text= "Explain\n " + handleString(explainText.replace("\n","") + "\n\n\n" + answersText,lineBreak))
    explainLabel.pack(side=tk.TOP)
    explainLabel.config(font=("Consoles", fontSize))
    explainLabel.pack_forget()

saveFile = []
isCreatedSaveFile = False
isCurrentSaved = False
savedFilename = ""
saveLine = ""
def saveCurrentQuestions(event):
    global saveLine,isCreatedSaveFile,isCurrentSaved,savedFilename
    if not isCreatedSaveFile:
        savedFilename = "saves/" + str(datetime.now()).replace(" ", "_") + ".txt"
        open(savedFilename, "w+",encoding="utf-8")
        isCreatedSaveFile = True
    if not isCurrentSaved and isCreatedSaveFile:
        saveFile = open(savedFilename, "a",encoding="utf-8")
        isCurrentSaved = True
        saveFile.write(str(saveLine))

def next(event):
    global selectArray,rightArray
    if len(selectArray) != len(rightArray):
        return
    for it in selectArray:
        if it not in rightArray:
            return
    onRightAnwer()

def startFrom(num):
    global data
    if num <= 1:
        return
    num -= 1
    tmpStr = str(num) + ". "
    # print(tmpStr)
    needToStop = False
    while 1:
        line = data.readline()
        if not line:
            data.seek(0)
            return
        if needToStop  and "<next>" in line:
            return
        if tmpStr in line :
            needToStop = True

def openFile():
    global data,root
    try:
        data = open(fd.askopenfilename() , "r",encoding="utf-8")
    except:
        pass

isFirstStart = True
root = tk.Tk()
buttons = []
imagesTest = []

data = []
root.bind('<Return>', next)
root.bind('<space>', next)
root.bind('e',showExplain)
root.bind('s',skip)
root.bind('a',returnPrev)
root.bind('w',saveCurrentQuestions)
root.attributes("-fullscreen", True)
data = open("questions.txt" , "r",encoding="utf-8")

os.system("mkdir -p saves")
img = ImageTk.PhotoImage(Image.open("hello.jpg"))
for i in range(5):
    imagesTest.append(tk.Label(root,image=img))
imagesTest[0].pack(side="bottom",fill="both", expand="yes")
imageCount = 1;
topSpace = tk.Label(root, text="\n")
topSpace.pack(side=tk.TOP)

questionsLabel = tk.Label(root, text=handleString("Open file and Press sapce or Enter to start",lineBreak))
questionsLabel.pack(side=tk.TOP)

startQuestionsNum = Entry(root)
startQuestionsNum.pack(side="top")
buttons.append(startQuestionsNum)
openButtom  = tk.Button(root, text='Open File', command=openFile)
openButtom.pack(side=tk.TOP)
buttons.append(openButtom)

explainLabel = tk.Label(root,text="")
explainLabel.pack(side=tk.TOP)
root.mainloop()