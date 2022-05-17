# -*- coding: utf-8 -*-
"""
Created on Tue May 17 19:48:30 2022

@author: v-zhiqili

parser:
    
"""
import os
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import json
import pickle

class Parser:
    def __init__(self):
        pass
    def parse(str):
        list1=str.split(' ');
        list2=[]
        for o in list1:
            oo=o.strip('\n \t,.<>/\\;\'\"()@!#$%^&*?`+-')
            if(len(oo)>0):
                list2.append(oo)    
        return list2
    def stem(wordList):
        resultlist=[]
        ps = PorterStemmer()
        for o in wordList:
            resultlist.append(ps.stem(o))
        return resultlist
class Index:
    def __int__(self):
        pass
    def SimpleII(fileList):
        II={}
        for i in range(len(fileList)):
            wordList1=Parser.parse(fileList[i])
            wordList2=Parser.stem(wordList1)
            temDict={}
            for j in range(len(wordList2)):
                if(wordList2[j] not in II):
                    II[wordList2[j]]=[0,[]]
                if(wordList2[j] not in temDict):
                    temDict[wordList2[j]]=[]
                temDict[wordList2[j]].append(j)
            for key in temDict:
                II[key][1].append([i,temDict[key]])
                II[key][0]=II[key][0]+1
        return II
    def WriteII(II,path="..\\data",fileName='II',mode='bits'): #mode:bits and json
        if(mode=='bits'):    
            pick_file = open(path+'\\'+fileName+'.bit','wb')
            pickle.dump(II,pick_file)
            pick_file.close()
        elif(mode=='json'):
            jsObj = json.dumps(II,sort_keys=True, indent=4)  
            fileObject = open(path+'\\'+fileName+'.json', 'w')  
            fileObject.write(jsObj)  
            fileObject.close() 
    def ReadII(path="..\\data",fileName='II',mode='bits'): #mode:bits and json
        if(mode=='bits'):    
            pick_file = open(path+'\\'+fileName+'.bit','rb')
            II= pickle.load(pick_file)
            pick_file.close()
            return II
        elif(mode=='json'):
            fileObject = open(path+'\\'+fileName+'.json', 'w')  
            II=json.load(fileObject)  
            fileObject.close()
            return II

if __name__ == "__main__":
    Entry="..\\data\\Reuters"
    fileNameList,indexList=os.listdir(Entry),[]
    for i in range(len(fileNameList)):
        tem=fileNameList[i]
        tem=tem.strip(".html")
        indexList.append(int(tem))
    indexList.sort()
    fileList=[]
    for i in range(40):#max(indexList)):
        filePath=Entry+'\\'+str(i)+'.html'
        if(os.path.exists(filePath)):
            file_object = open(filePath)
            file=file_object.read()
            fileList.append(file)
        else:
            print('\033[31m file %s not exist \033[0m' % (filePath))
            fileList.append('')
    II=Index.SimpleII(fileList)
    Index.WriteII(II)
    II=Index.ReadII()
    Index.WriteII(II,mode='json')
