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
    def convertToVB(n):
        numList=[]
        while True:
            numList.append(n%128)
            n=n//128
            if(n==0):
                break
        byteList=[]
        for i in range(len(numList)):
            if(i!=len(numList)-1):
                byteList.append(int(numList[i]).to_bytes(length=1,signed=False,byteorder='big'))
            else:
                byteList.append(int(numList[i]+128).to_bytes(length=1,signed=False,byteorder='big'))
        return byteList
        #print(byteList)
#        data_byte1 = int(1324).to_bytes(length=2, byteorder='big', signed=True)
    def convertFromVB(bytesList,index=0):
        numList=[]
        while True:
            tem=int.from_bytes(bytesList[index], byteorder='big', signed=False)
            if tem>=128:
                numList.append(tem-128)
                break;
            else:
                numList.append(tem)
            index=index+1
        n=0
        pos=1
        for i in range(len(numList)):
            n=pos*numList[i]+n
            pos=pos*128
        return n,index+1
    def MyWriteII(II,path="..\\data",fileName='II'):
        """
        The format:
            word1length,word1pos,.....
            word1:docID1,posNum,pos1,pos2,...,docID2,posNum,pos1,....
            ...
        """
        totalList=[]
        keyList=[]
        numList=[]
        for key in II:
            num=II[key][0]
            wordList=[]
            for j in range(num):
                docID=II[key][1][j][0]
                if(j==0):
                    wordList.append(docID)
                else:
                    wordList.append(docID-II[key][1][j-1][0])
                posNumber=[]
                
                for k in range(len(II[key][1][j][1])):
                    if(k==0):
                        posNumber.append(II[key][1][j][1][k])
                    else:
                        posNumber.append(II[key][1][j][1][k]-II[key][1][j][1][k-1])
                #print(("*",docID,len(posNumber),posNumber),end=" ")
                wordList.append(len(posNumber))
                wordList.extend(posNumber)
            keyList.append(key)
            totalList.append(wordList)
            numList.append(num)
        ansList=[]
        #print(len(keyList))
        ansList.append(len(keyList))
        for i in range(len(keyList)):
            #print(keyList[i],end=" ")
            ansList.append(len(keyList[i]))
            for j in range(len(keyList[i])):
                ansList.append(ord(keyList[i][j]))
        for i in range(len(totalList)):
            #print(numList[i],end=" ")
            ansList.append(numList[i])
            ansList.extend(totalList[i])
        byteList=[]
        for i in range(len(ansList)):
            tem=Index.convertToVB(ansList[i])
            byteList.extend(tem)
        ans=''
        for i in range(len(byteList)):
            if(i==0):
                ans=bytes(byteList[i])
            else:
                ans+=bytes(byteList[i])            
        with open(path+'\\'+fileName+'.bin', "wb") as f:
            f.write(ans)        
        return ans
    def MyReadII(path="..\\data",fileName='II',mode='bits'):
        ## here need to read the fileand convert it to bytes
        buffer,II='',[]
        with open(path+'\\'+fileName+'.bin', "rb") as f:
            buffer=f.read()           
        for i in range(len(buffer)):
            tem=buffer[i]
            tem=tem.to_bytes(length=1,signed=False,byteorder='big')
            II.append(tem)
        index=0
        num,index=Index.convertFromVB(II,index)
        keyList=[]
        #print(num)
        for i in range(num):
            wordLength,index=Index.convertFromVB(II,index)
            key=""
            for j in range(wordLength):
                char,index=Index.convertFromVB(II,index)
                char=chr(char)
                key=key+char
            #print(key,end=" ")
            keyList.append(key)
        newII={}
        for i in range(num):
            sublistLen,index=Index.convertFromVB(II,index)
            posWordList=[sublistLen,[]]
            #print(sublistLen,end=" ")
            for j in range(sublistLen):
                
                docID,index=Index.convertFromVB(II,index)
                if(j!=0):
                    docID+=posWordList[1][j-1][0]    
                PosNumPerDoc,index=Index.convertFromVB(II,index)
                
                posOneDoc=[]
                for k in range(PosNumPerDoc):
                    pos,index=Index.convertFromVB(II,index)
                    if(k==0):
                        posOneDoc.append(pos)
                    else:
                        posOneDoc.append(pos+posOneDoc[k-1])
                #print(("*",docID,PosNumPerDoc,posOneDoc))
                posWordList[1].append([docID,posOneDoc])
            newII[keyList[i]]=posWordList
        #print(newII)
        return newII 
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
    def compare(II1,II2):
        keyList1=[key for key in II1]
        keyList2=[key for key in II2]
        for i in range(len(keyList1)):
            if(keyList1[i]!=keyList2[i]):
                raise Exception("\033[31m key mismatch:"+str(keyList1[i])+","+str(keyList2[i])+" \033[1m")
        for key in II1:
            if(II1[key][0]!=II2[key][0]):
                raise Exception("\033[31m freq mismatch,"+str(keyList1[i])+":"+str(II1[key][0])+","+str(II2[key][0])+" \033[1m")
            for j in range(len(II1[key][1])):
                if(II1[key][1][j][0]!=II2[key][1][j][0]):
                    raise Exception("\033[31m docID mismatch,"+str(keyList1[i])+":"+str(II1[key][1][j][0])+","+str(II2[key][1][j][0])+" \033[1m")
                    if(len(II1[key][1][j][1])!=len(II2[key][1][j][1])):
                        raise Exception("\033[31m doc pos freq mismatch,"+str(keyList1[i])+","+str(II1[key][1][j][0])+":"+str(len(II1[key][1][j][1]))+","+str(len(II2[key][1][j][1]))+" \033[1m")
                    for k in range(II1[key][1][j][1]):
                        if(II1[key][1][j][1][k]!=II2[key][1][j][1][k]):
                            raise Exception("\033[31m doc pos mismatch,"+str(keyList1[i])+","+str(II1[key][1][j][0])+":"+str(II1[key][1][j][1][k])+","+str(II2[key][1][j][1][k])+" \033[1m")
        print("\033[32;1m # compare II1 and II2, passed \033[0m")
if __name__ == "__main__":
    print("here test the Index compress...")
    Entry="..\\data\\Reuters"
    fileNameList,indexList=os.listdir(Entry),[]
    for i in range(len(fileNameList)):
        tem=fileNameList[i]
        tem=tem.strip(".html")
        indexList.append(int(tem))
    indexList.sort()
    fileList=[]
    for i in range(100):#max(indexList)):
        filePath=Entry+'\\'+str(i)+'.html'
        if(os.path.exists(filePath)):
            file_object = open(filePath)
            file=file_object.read()
            fileList.append(file)
        else:
            print('\033[33;1m Warning: file %s not exist \033[0m' % (filePath))
            #print('\033[31m file %s not exist \033[0m' % (filePath))
            fileList.append('')
    II=Index.SimpleII(fileList)

    Index.MyWriteII(II,fileName='test_compress')
    JJ=Index.MyReadII(fileName='test_compress')
    Index.compare(II,JJ)
   # Index.WriteII(II)
    #II=Index.ReadII()
   # Index.WriteII(II,mode='json')
