# -*- coding: utf-8 -*-
"""
Created on Tue May 17 21:20:17 2022

@author: v-zhiqili

console

"""
from Index import *
from Inquire import *
# here need to analysis the operator

class Analysis:
    def __init__(self):
        pass
    def simpleBool(wordList):
        nodeList,tree=[],[]
        for i in range(len(wordList)):
            if(wordList[i]=='OR' or wordList[i]=='AND' or wordList[i]=='NOT'):
                nodeList.append(['op',[wordList[i]]])
            else:
                ps = PorterStemmer()
                nodeList.append(['word',[ps.stem(wordList[i])]])
        index=0
        while index<len(nodeList):
            if(nodeList[index][0]=="op" and nodeList[index][1][0]=="NOT"):
                word=tree.pop()
                nodeList[index][1].append(word)
                tree.append(nodeList[index])
            elif(nodeList[index][0]=="op" and (nodeList[index][1][0]=="AND" or nodeList[index][1][0]=="OR")):
                word1=tree.pop()
                word2=tree.pop()
                nodeList[index][1].append(word1)
                nodeList[index][1].append(word2)
                tree.append(nodeList[index])
            else:
                tree.append(nodeList[index])
            index=index+1          
        return tree
    def Execute(tree):
        #print(tree)
        if(tree[0]=='op'):
            if(tree[1][0]=='AND' or tree[1][0]=='OR'):
                result1=Analysis.Execute(tree[1][1])
                result2=Analysis.Execute(tree[1][2])
                #print(result1)
                #print(result2)
                if(tree[1][0]=='AND'):
                    return Bool.And(result1,result2)
                elif(tree[1][0]=='OR'):
                    return Bool.Or(result1,result2)
            elif(tree[1][0]=='NOT'):
                result1=Analysis.Execute(tree[1][1])
                return Bool.Not(result1,ran)
        else:
            ps = PorterStemmer()
            word=ps.stem(tree[1][0])
            return Inquire.InquireByII(word,II)
def displayString(oneStr,key):
   # print(oneStr)
    index=0
    for i in range(len(oneStr)):
        if(oneStr[i:i+len(key)]==key):
            index=i
            break
   # print(index)
    for i in range(20,100):
        if(index-i<=0):
            minIndex=0
            break;
        elif(oneStr[i]==' '):
            minIndex=index-i
            break;
    for i in range(20,100):
        if(index+i>=len(oneStr)):
            maxIndex=len(oneStr)
            break;
        elif(oneStr[i]==' '):
            maxIndex=index+i
            break;
    return "..."+oneStr[minIndex:index],oneStr[index:index+len(key)],oneStr[index+len(key):maxIndex]+"..."
def display(II,key,entry="..\\data\\Reuters"):
    if(key in II):
        print('total:'+str(II[key][0]))
        for i in range(II[key][0]):
            docID=II[key][1][i][0]
            docPos=II[key][1][i][1][0]
            file_object = open(entry+'\\'+str(docID)+'.html')
            file=file_object.read()
            dispStr1,dispStr2,dispStr3=displayString(file,key)
            print("\033[32;1m docID "+str(docID)+": \033[0m",end='')
            print(dispStr1,end='')
            print("\033[32;1m"+dispStr2+'\033[0m',end='')
            print(dispStr3)
            ## first detect if the index exists
if(not (os.path.exists("..\\data\\II.bin") and os.path.exists("..\\data\\II.bit"))): 
    Entry="..\\data\\Reuters"
    fileNameList,indexList=os.listdir(Entry),[]
    for i in range(len(fileNameList)):
        tem=fileNameList[i]
        tem=tem.strip(".html")
        indexList.append(int(tem))
    indexList.sort()
    fileList=[]
    for i in range(max(indexList)):
        filePath=Entry+'\\'+str(i)+'.html'
        if(os.path.exists(filePath)):
            file_object = open(filePath)
            file=file_object.read()
            fileList.append(file)
        else:
            print('\033[33;1m Warning: file %s not exist \033[0m' % (filePath))
            #print('\033[31m file %s not exist \033[0m' % (filePath))
            fileList.append('')
    JJ=Index.SimpleII(fileList)
    Index.WriteII(JJ)
    Index.WriteII(JJ,mode='json')
    Index.MyWriteII(JJ)
    print(max(indexList))
II=Index.MyReadII()
ran=[i for i in range(0,21576)]
while(True):
    sent=input("\ninput your inquire:")
    preList,keyList=sent.split(" "),[]
    for o in preList:
        oo=o.strip(' ')
        if(len(oo)>0):
            keyList.append(oo)
    tree=Analysis.simpleBool(keyList)
    result=Analysis.Execute(tree[0])
    print(result)
    if(len(keyList)==1):
        display(II,keyList[0])

