from lxml import html
import requests

from PIL import Image
import requests
from io import BytesIO

def saveImageByUrl(url, filename):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    img.save(filename)

page = requests.get('https://www.ccna7.com/ccna1-v6-0/ccna1-v6-0-final-exam-answer-2017-100/')
tree = html.fromstring(page.content)
# print(tree.xpath('//li/text()'))
questions = tree.xpath('//li//h3/text()');
# [print(answers[i]) for i in range(len(answers))]
# answers = tree.xpath('//li/text()');

allText = tree.xpath('//img/@src|//li/text()|//li//h3/text()|//li//em/*/text()|//li//span[@style="color: #ff0000;"]/text()| //li//span[@style="color: #ff0000;"]//em/text()');
questions = tree.xpath('//li//h3/text()');
rightAnswers = tree.xpath('//li//span[@style="color: #ff0000;"]/text()| //li//span[@style="color: #ff0000;"]//em/text()');
# [print(answers[i]) for i in range(len(answers))]
f = open("questions.txt", "w+")
# print(len(answers))
firstQuestion = True
questionsNum = 1
for elem in allText:
    elem = elem.encode("ascii", errors="ignore").decode()
    if elem in questions:
        if not firstQuestion:
            f.write("<next>\n")
        else:
            firstQuestion = False
        f.write("<question>" + str(questionsNum) + ". " + elem + '\n')
        questionsNum += 1
    else :
        if elem in rightAnswers:
            f.write("<answer>" + elem + '\n')
        else:
            if "data:image/" not in elem:
                if "http" in elem:
                    fileName = "imgs/" + str(allText.index(elem)) + ".png"
                    saveImageByUrl(elem, fileName)
                    f.write("<image>" + fileName + '\n')
                else:
                    if len(elem) > 1:
                        f.write(elem + '\n')
            