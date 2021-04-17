from random import choice
from PySide6.QtWidgets import QApplication,QMainWindow
from bs4 import BeautifulSoup
import requests
import re
import numpy as np
import random
import sys
from mainwindow import Ui_MainWindow


immortalpage = 'https://kisslightnovels.info/novel/immortal-and-martial-dual-cultivation/immortal-and-martial-dual-cultivation-chapter-566/'
baseLink = 'https://kisslightnovels.info/novel/immortal-and-martial-dual-cultivation/immortal-and-martial-dual-cultivation-chapter-{0}/'

ADDTEXT = "adsbygoogle"
pattern = r"[^\w\s]"

def stripPunctuation(text):
    return re.sub(pattern,"",text)


def scour(Pagenumber):
    response = requests.get(baseLink.format(Pagenumber))
    soup = BeautifulSoup(response.text, 'html.parser')

    #gets me all the text
    all_paragraphs = soup.find_all('p')

    text = ""

    #scours the webpage for text
    #gets rid of the end of page login there are 21 divs
    for paragraph in all_paragraphs[4:len(all_paragraphs) - 21]:
        #removes excess class
        if paragraph.get("class") == None  and not (ADDTEXT in paragraph.text):
            text += paragraph.text + " "

    #gets rid of the extra space
    return text[:len(text) - 1]

def scourFrom(startpage,endpage):
    #end page inclusive
    text = ""
    for x in range(startpage,endpage+1) :
        text += scour(x) + " "
    #removes the ending space
    return text[:len(text) - 1]



class markov(object):
    def __init__(self):
        self.data = {}

    #example
    # {a_word : [next word,....., n-next word]}
    #there are no percentages, but the frequency will decide if it gets chosen more often
    def addText(self,text):
        #get all new words
        words = np.array([text for text in text.split(' ')])
        #get the already known words
        dataKeys = np.array(self.data.keys())
        #get the new word list
        old_words = words[np.in1d(words,dataKeys)]
        new_words = words[np.in1d(words,old_words) == False]

        #add words to the data
        for word in old_words:

            # grabs the next words
            NextWordIdx = np.where(words == word)[0] + 1

            # make sure index is lower than the length of the wordlist
            NextWordIdx = NextWordIdx[NextWordIdx < len(words)]

            NextWord = words[NextWordIdx]

            #add this word to the word list
            for morewords in NextWord :

                #morewords is a single word
                self.data[word].append(morewords)

        for word in new_words :
            #pretty much identical, possibly simplify later

            # grabs the next words
            NextWordIdx = np.where(words == word)[0] + 1

            #make sure index is lower than the length of the wordlist
            NextWordIdx = NextWordIdx[NextWordIdx < len(words)]

            NextWord = words[NextWordIdx]

            self.data[word] = []
            # add this word to the word list
            for morewords in NextWord:
                # morewords is a single word
                self.data[word].append(morewords)
        return self.data

    #random word if the current list is empty
    def nextWord(self,aWord):
        if len(self.data[aWord]) == 0 :
            return self.randomWord()
        return random.choice(self.data[aWord])

    #too be implemented
    def nextMostLikely(self,aWord):
        pass

    def randomWord(self):
        keys = list(self.data.keys())
        key = random.choice(keys)
        while len(self.data[key]) == 0 :
            key = random.choice(keys)

        return random.choice(self.data[key])

    def clear(self):
        self.data = {}

    def wordInside(self,AWord):
        keys = list(self.data.keys())
        return AWord in keys


class MainWindow(QMainWindow) :
    def __init__(self,parent = None):
        QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.updateText)
        self.setStyleSheet(open('Obit.qss').read())

    def updateText(self):
        #should really be using default values...
        start = self.ui.StartNumberEdit.text()
        end = self.ui.EndNumberEdit.text()
        length = self.ui.WordCountEdit.text()

        word = self.ui.ChosenWordEdit.text()

        #makes sure input is valid
        if(not(start == "" or end == "")):
            immortaltext = scourFrom(int(start), int(end))
        else:
            immortaltext = scour(10)

        immortaltext = immortaltext.lower()
        immortaltext = stripPunctuation(immortaltext)

        mark = markov()

        dist = mark.addText(immortaltext)
        if(not mark.wordInside(word)) :
            word = mark.randomWord()


        #makes sure length is valid
        if(length == "") :
            length = 100
        else:
            length = int(length)

        sentence = ""

        # builds me a sentence with 100 words in it
        for x in range(length):
            sentence += word + " "
            word = mark.nextWord(word)

        print(sentence)
        self.ui.textBrowser.setText(sentence)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #opens window
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    # window.show()

    sys.exit(app.exec_())



