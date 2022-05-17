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
        print(tree)
        if(tree[0]=='op'):
            if(tree[1][0]=='AND' or tree[1][0]=='OR'):
                result1=Analysis.Execute(tree[1][1])
                result2=Analysis.Execute(tree[1][2])
                print(result1)
                print(result2)
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
II=Index.ReadII()
ran=[i for i in range(0,40)]
while(True):
    sent=input("input your inquire:")
    preList,keyList=sent.split(" "),[]
    for o in preList:
        oo=o.strip(' ')
        if(len(oo)>0):
            keyList.append(oo)
    tree=Analysis.simpleBool(keyList)
    result=Analysis.Execute(tree[0])
    print(result)
    
