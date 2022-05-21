# -*- coding: utf-8 -*-
"""
Created on Tue May 17 19:48:30 2022

@author: v-zhiqili

parser:
    
"""
import os
from tkinter.tix import Tree
import numpy as np
import pandas as pd
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from tqdm import trange, tqdm
from multiprocessing.dummy import Pool

class Parser:
    def __init__(self):
        pass
    def parse(str):
        list1=str.split(' ')
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
    def __init__(self, datadir='../data', index_name='II.npy'):
        if not os.path.exists(os.path.join(datadir, 'index', index_name)):
            path = os.path.join(datadir, 'Reuters')
            file_list = os.listdir(path)
            file_list.sort(key=lambda x: int(x.split('.')[0]))
            file_objs = []
            for file_name in file_list:    
                file_path = os.path.join(path, file_name)
                file_objs.append(open(file_path, encoding='ISO-8859-1').read())
            self.inverted_index = self.create_inverted_index(file_objs)
            doc_dict = file_list
            num_dict = len(file_list)
            # self.two_gram = self.__build_2_gram()
            self.__write()
            self.__write_2_gram()
            self.__write_dict(doc_dict, num_dict)
        else: 
            self.inverted_index = self.__read()
            # self.two_gram = self.__load_2_gram()

        self.two_gram = self.__build_2_gram()
        
    def get_doc(self):
        return self.__read_dict()

    def __write_2_gram(self, path='../data/index/two_gram.txt'):
        all = []
        for key, value in self.two_gram.items():
            all.append(key+","+",".join(value))

        with open(path, "w") as f:
            f.write("|".join(all))

        f.close()
    def __load_2_gram(self, path='../data/index/two_gram.txt'):
        pool = Pool(8)
        with open(path) as f:
            all = f.read()

        all = all.split('|')
        all = list(pool.map(lambda x: x.split(','), all))
        all = dict(pool.map(lambda x: (x[0], x[1:]), all))

        f.close()
        return all

    def __build_2_gram(self):
        '''
            input: II:inverse index dtype = dict
            output: IG: 2-gram index dtype = dict 
        '''
        IG = {}
        II = self.inverted_index
        for r in list(II.keys()):
            s = '$' + r + '$'
            # print(s)
            for i in range(0, len(s) - 1):
                k = s[i:i+2]
                if not IG.__contains__(k):
                    IG[k] = []
                IG[k].append(r)

        for i in IG:
            IG[i].sort()
        return IG

    def __write_dict(self, doc_dict, num_dict, datadir = '../data/index'):
        np.savez_compressed(os.path.join(datadir, 'doc_dict'), np.array(doc_dict, dtype=object))
        pass

    def __read_dict(self, datadir='../data/index'):
        doc_dict = np.load(os.path.join(datadir, 'doc_dict.npz'), allow_pickle=True)['arr_0']
        doc_dict = list(doc_dict)
        return doc_dict, len(doc_dict)

    def get_index_by_key(self, key):
        return self.inverted_index[key]

    def create_inverted_index(self, fileList):
        II={}
        for i in trange(len(fileList)):
            file = fileList[i]
            wordList1=Parser.parse(file)
            wordList2=Parser.stem(wordList1)
            temDict={}
            for j in range(len(wordList2)):
                if(wordList2[j] not in II):
                    II[wordList2[j]]=[0,{}]
                if(wordList2[j] not in temDict):
                    temDict[wordList2[j]]=[]
                temDict[wordList2[j]].append(j)
            for key in temDict:
                II[key][1].update({i:temDict[key]})
                II[key][0]=II[key][0]+1
        return II

    def __convertToVB(self, n):
        numList=[]
        while True:
            numList.append(n%128)
            n=n//128
            if(n==0):
                break
        byteList=[]
        for i in range(len(numList)):
            if(i!=len(numList)-1):
                byteList.append(numList[i])
            else:
                byteList.append(numList[i]+128)
        return byteList

    def __convertFromVB(self, bytesList,index=0):

        numList=[]
        while True:
            tem=bytesList[index]
            if tem>=128:
                numList.append(tem-128)
                break
            else:
                numList.append(tem)
            index=index+1
        n=0
        pos=1
        for i in range(len(numList)):
            n=pos*numList[i]+n
            pos=pos*128
        return n,index+1

    def __write(self, path="../data/index",fileName='II'):
        """
        The format:
            word1length,word1pos,.....
            word1:docID1,posNum,pos1,pos2,...,docID2,posNum,pos1,....
            ...
        """
        totalList=[]
        keyList=[]
        numList=[]
        II = self.inverted_index
        last_docID = 0
        for key in tqdm(II):
            num=II[key][0]
            wordList=[]
            for j, (docID, record) in enumerate(II[key][1].items()):
                if(j==0):
                    wordList.append(docID)
                else:
                    wordList.append(docID-last_docID)
                
                last_docID = docID

                posNumber = np.array(record)
                posNumber = [record[0]] + list(posNumber[1:] - posNumber[:-1])

                wordList.append(len(posNumber))
                wordList.extend(posNumber)
                
            keyList.append(key)
            totalList.append(wordList)
            numList.append(num)
        ansList=[]
        #print(len(keyList))
        ansList.append(len(keyList))
        for i in trange(len(keyList)):
            #print(keyList[i],end=" ")
            ansList.append(len(keyList[i]))
            for j in range(len(keyList[i])):
                ansList.append(ord(keyList[i][j]))
        for i in trange(len(totalList)):
            #print(numList[i],end=" ")
            ansList.append(numList[i])
            ansList.extend(totalList[i])
        byteList=[]
        for i in trange(len(ansList)):
            tem = self.__convertToVB(ansList[i])
            byteList.extend(tem)

        byteList = np.array(byteList, dtype=np.uint8)
        # for i in trange(len(byteList)):
        #     if(i==0):
        #         ans=bytes(byteList[i])
        #     else:
        #         ans+=bytes(byteList[i])            
        
        if not os.path.exists(path):
            os.mkdir(path)
        
        np.save(os.path.join(path, fileName+'.npy'), byteList)

    def __read(self, path="../data/index",fileName='II'):
        ## here need to read the fileand convert it to bytes
        print('reading index file ... ')
        byteList = np.load(os.path.join(path,fileName+'.npy'))
        II = list(byteList)

        index=0
        num,index = self.__convertFromVB(II,index)
        keyList=[]
        #print(num)
        for i in range(num):
            wordLength, index = self.__convertFromVB(II,index)
            key=""
            for j in range(wordLength):
                char , index= self.__convertFromVB(II,index)
                char=chr(char)
                key=key+char
            #print(key,end=" ")
            keyList.append(key)

        newII={}
        last_docID = 0

        for i in range(num):
            sublistLen,index=self.__convertFromVB(II,index)
            posWordList=[sublistLen,{}]
            #print(sublistLen,end=" ")
            for j in range(sublistLen):
                
                docID, index = self.__convertFromVB(II,index)
                if j != 0:
                    docID += last_docID
                    last_docID = docID
                else:
                    last_docID = docID
                PosNumPerDoc,index=self.__convertFromVB(II,index)
                
                posOneDoc=[]
                for k in range(PosNumPerDoc):
                    pos,index=self.__convertFromVB(II,index)
                    if(k==0):
                        posOneDoc.append(pos)
                    else:
                        posOneDoc.append(pos+posOneDoc[-1])
                #print(("*",docID,PosNumPerDoc,posOneDoc))
                posWordList[1][docID] = posOneDoc
            newII[keyList[i]]=posWordList

        print('Done!')
        return newII 

    # def WriteII(II,path="../data",fileName='II',mode='bits'): #mode:bits and json
    #     if(mode=='bits'):    
    #         pick_file = open(path+'/'+fileName+'.bit','wb')
    #         pickle.dump(II,pick_file)
    #         pick_file.close()
    #     elif(mode=='json'):
    #         jsObj = json.dumps(II,sort_keys=True, indent=4)  
    #         fileObject = open(path+'/'+fileName+'.json', 'w')  
    #         fileObject.write(jsObj)  
    #         fileObject.close() 
    # def ReadII(path="../data",fileName='II',mode='bits'): #mode:bits and json
    #     if(mode=='bits'):    
    #         pick_file = open(path+'/'+fileName+'.bit','rb')
    #         II= pickle.load(pick_file)
    #         pick_file.close()
    #         return II
    #     elif(mode=='json'):
    #         fileObject = open(path+'/'+fileName+'.json', 'w')  
    #         II=json.load(fileObject)  
    #         fileObject.close()
    #         return II
    def compare(self):

        II1 = self.inverted_index
        II2 = self.__read()
        keyList1=[key for key in II1]
        keyList2=[key for key in II2]
        for i in range(len(keyList1)):
            if(keyList1[i]!=keyList2[i]):
                raise Exception("\033[31m key mismatch:"+str(keyList1[i])+","+str(keyList2[i])+" \033[1m")
        for key in II1:
            if(II1[key][0]!=II2[key][0]):
                raise Exception("\033[31m freq mismatch,"+str(keyList1[i])+":"+str(II1[key][0])+","+str(II2[key][0])+" \033[1m")
            docID1 = len(II1[key][1].keys())
            docID2 = len(II2[key][1].keys())
            if docID1 != docID2:
                raise Exception("\033[31m docID mismatch,"+str(keyList1[i])+":"+str(II1[key][1][j][0])+","+str(II2[key][1][j][0])+" \033[1m")
            for j in II1[key][1]:
                if II1[key][1][j] != II2[key][1][j]:
                    raise Exception("\033[31m doc pos mismatch \033[1m")
        print("\033[32;1m # compare II1 and II2, passed \033[0m")

    

if __name__ == "__main__":
    index = Index()
    index.compare()