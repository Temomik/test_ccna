from lxml import html
import requests

from PIL import Image
import requests
from io import BytesIO

def saveImageByUrl(url, filename):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    img.save(filename)

page = requests.get('https://itexamanswers.net/ccna-1-final-exam-answers-v5-1-v6-0-introduction-to-networks.html#ftoc-version-6-0')
tree = html.fromstring(page.content)
allText = tree.xpath('//article//img[@alt=""]/@src|//article//strong//text()|//article//div[@class="message_box success"]//text()|//article//li//text()')
f = open("questions.txt", "w+", encoding="utf-8")
firstQuestion = True
questionsNum = 1
for elem in allText:
    asciiElem = elem.encode("ascii", errors="ignore").decode()
    if str(questionsNum) + ". " in elem:
        if not firstQuestion:
            f.write("<next>\n")
        else:
            firstQuestion = False
        questionsNum += 1
        f.write("<question>" + asciiElem.replace("*","") + '\n')
    else :
        if not firstQuestion:
            if "*" in elem and elem.find('*') == len(elem) - 1 and len(elem) > 1 :
                f.write("<answer>" + asciiElem.replace("*","") + '\n')
            else:
                isImage = True
                imgTagStart = "http"
                imageEceptionsTags = {".com"}
                for exceptionsTag in imageEceptionsTags:
                    if exceptionsTag in elem[(len(elem)-len(exceptionsTag)):]:
                        isImage = False
                if imgTagStart in elem[0:len(imgTagStart)] and isImage:
                    print("_"+elem+"_")
                    fileName = "imgs/" + str(allText.index(elem)) + ".png"
                    saveImageByUrl(elem, fileName)
                    f.write("<image>" + fileName + '\n')
                    continue
                if "Explain:" in elem:
                    f.write("<explain>")
                else:
                    if len(elem) > 1:
                        f.write(elem.replace("\n","") + '\n')
            