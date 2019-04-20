from nltk.translate.bleu_score import sentence_bleu
from nltk.translate.bleu_score import corpus_bleu
import matplotlib.pyplot as plt
import numpy as np
import os
import xlwt

def insert(original, new, pos):
    '''Inserts new inside original at pos.'''
    return original[:pos] + new + original[pos:]

def replacePun(fileName,newFileName):
    # Read standard file to stanList
    # dir = "Xiaoyi.txt"
    dir = fileName
    filePath = os.path.join('OrigData', dir)
    file = open(filePath)
    contentList = []

    line = file.readline()
    while line:

        punctuation = [',','.',':',';','?']
        print(line[-2])
        if(line[-2] not in punctuation):
            line = line + "."
        for pun in punctuation:
            line = line.replace(pun," "+pun)
            # try:
            #     idx = line.index(pun)
            # except ValueError:
            #     pass
            # else:
            #     line = insert(line," ",idx)

        contentList.append(line)
        line = file.readline()
    file.close()

    newTxt = open(newFileName,'w')
    for content in contentList:
        content = content.split()
        # print (content[0])
        # print (content[1])
        # print ("\n")
        for idx in np.arange(1,len(content),1):
            newTxt.write(content[idx])
            newTxt.write(" ")
        newTxt.write("\n")
    newTxt.close()

def readStandardData():
    standardFile = "Standard.txt"
    filePath = os.path.join('data',standardFile)
    standardData = []
    file = open(filePath)
    content = file.readline()
    while content:
        standardData.append(content)
        content = file.readline()
    file.close()
    return standardData

def computeBLEU(fileList,writeTxt,writeExcel):
    a = []
    b = []
    c = []
    d = []

    standard = readStandardData()
    # otherFiles = ["Baidu.txt","Google.txt","Jinshan.txt","Xiaoyi.txt","Youdao.txt"]
    otherFiles = fileList
    for fileName in otherFiles:
        filePath = os.path.join('data',fileName)
        contentList = []
        file = open(filePath)
        content = file.readline()
        while content:
            contentList.append(content)
            content = file.readline()
        file.close()

        resFileName = insert(fileName, "_res", -4)
        if(writeTxt):
            resFile = open(os.path.join("result",resFileName),'w')
        if(writeExcel):
            excelFile = xlwt.Workbook(encoding='utf-8')
            booksheet = excelFile.add_sheet(fileName, cell_overwrite_ok=True)
            booksheet.write(0, 0, "1-gram_Cumulative")
            booksheet.write(0, 1, "2-gram_Cumulative")
            booksheet.write(0, 2, "3-gram_Cumulative")
            booksheet.write(0, 3, "4-gram_Cumulative")
            booksheet.write(0, 4, "1-gram_Individual")
            booksheet.write(0, 5, "2-gram_Individual")
            booksheet.write(0, 6, "3-gram_Individual")
            booksheet.write(0, 7, "4-gram_Individual")
            excelFileIdx = 1

        for reference, candidate in zip(standard,contentList):
            score1g = sentence_bleu([reference.split()], candidate.split(), weights=(1, 0, 0, 0))
            score2g = sentence_bleu([reference.split()], candidate.split(), weights=(0.5, 0.5, 0, 0))
            score3g = sentence_bleu([reference.split()], candidate.split(), weights=(0.33, 0.33, 0.33, 0))
            score4g = sentence_bleu([reference.split()], candidate.split(), weights=(0.25, 0.25, 0.25, 0.25))

            ind_score1g = sentence_bleu([reference.split()], candidate.split(), weights=(1, 0, 0, 0))
            ind_score2g = sentence_bleu([reference.split()], candidate.split(), weights=(0, 1, 0, 0))
            ind_score3g = sentence_bleu([reference.split()], candidate.split(), weights=(0, 0, 1, 0))
            ind_score4g = sentence_bleu([reference.split()], candidate.split(), weights=(0, 0, 0, 1))

            a.append(score1g)
            b.append(score2g)
            c.append(score3g)
            d.append(score4g)
            if(writeTxt):
                resFile.write(reference + candidate)
                resFile.write("Cumulative 1-gram: %f\n" % score1g)
                resFile.write("Cumulative 2-gram: %f\n" % score2g)
                resFile.write("Cumulative 3-gram: %f\n" % score3g)
                resFile.write("Cumulative 4-gram: %f\n" % score4g)

                resFile.write("Individual 1-gram: %f\n" % ind_score1g)
                resFile.write("Individual 2-gram: %f\n" % ind_score2g)
                resFile.write("Individual 3-gram: %f\n" % ind_score3g)
                resFile.write("Individual 4-gram: %f\n\n" % ind_score4g)
            if(writeExcel):
                booksheet.write(excelFileIdx, 0, score1g)
                booksheet.write(excelFileIdx, 1, score2g)
                booksheet.write(excelFileIdx, 2, score3g)
                booksheet.write(excelFileIdx, 3, score4g)

                booksheet.write(excelFileIdx, 4, ind_score1g)
                booksheet.write(excelFileIdx, 5, ind_score2g)
                booksheet.write(excelFileIdx, 6, ind_score3g)
                booksheet.write(excelFileIdx, 7, ind_score4g)
                excelFileIdx+=1
        if(writeExcel):
            excelResFileName = os.path.join("result",resFileName).replace('txt','xls')
            excelFile.save(excelResFileName)
        if(writeTxt):
            resFile.close()
    return a,b,c,d
def plotTheFigre():
    a, b, c, d = computeBLEU(fileList)
    Baidu1g = sorted(a[60 * 0:60 * 1])
    Baidu2g = b[60 * 0:60 * 1]
    Baidu3g = c[60 * 0:60 * 1]
    Baidu4g = d[60 * 0:60 * 1]

    Google1g = sorted(a[60 * 1:60 * 2])
    Google2g = b[60 * 1:60 * 2]
    Google3g = c[60 * 1:60 * 2]
    Google4g = d[60 * 1:60 * 2]

    Jinshan1g = sorted(a[60 * 2:60 * 3])
    Jinshan2g = b[60 * 2:60 * 3]
    Jinshan3g = c[60 * 2:60 * 3]
    Jinshan4g = d[60 * 2:60 * 3]

    Xiaoyi1g = sorted(a[60 * 3:60 * 4])
    Xiaoyi2g = b[60 * 3:60 * 4]
    Xiaoyi3g = c[60 * 3:60 * 4]
    Xiaoyi4g = d[60 * 3:60 * 4]

    Youdao1g = sorted(a[60 * 4:60 * 5])
    Youdao2g = b[60 * 4:60 * 5]
    Youdao3g = c[60 * 4:60 * 5]
    Youdao4g = d[60 * 4:60 * 5]

    plt.plot(Baidu1g, label="Baidu")
    plt.plot(Google1g, label="Google")
    plt.plot(Jinshan1g, label="Jinshan")
    plt.plot(Xiaoyi1g, label="Xiaoyi")
    plt.plot(Youdao1g, label="Youdao")
    plt.legend(loc='upper left')
    plt.show()


if __name__ == '__main__':


    fileList = ["Baidu.txt", "Google.txt", "Jinshan.txt", "Xiaoyi.txt", "Youdao.txt"]
    for file in fileList:
        replacePun(file,file)

    # computeBLEU(fileList,True,False)

    # str1 = "Empty talk harms the country"
    # str2 = "Empty talk spoils the country"


