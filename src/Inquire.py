# -*- coding: utf-8 -*-
"""
Created on Tue May 17 21:21:07 2022

@author: v-zhiqili

Inquire
"""

class Inquire:
    def __init__(self):
        pass
    def InquireByII(key,II):
        if key not in II:
            return []
        PaperID=[]
        for i in range(len(II[key][1])):
            PaperID.append(II[key][1][i][0])
        return PaperID
class Bool:
    def __init__(self):
        pass
    def Not(key1,fileIndexList=[]):
        result=[]
        for o in fileIndexList:
            if(o not in key1):
                result.append(o)
        return result
    
    def And(key1,key2):
        #print("AND",key1,key2)
        index1,index2=0,0
        result=[]
        while True:
            if(index1>=len(key1) or index2>=len(key2)):
                break
            if(key1[index1]==key2[index2]):
                result.append(key1[index1])
                index1=index1+1
                index2=index2+1
            elif(key1[index1]<key2[index2]):
                index1=index1+1
            elif(key1[index1]>key2[index2]):
                index2=index2+1
       # print("AND",result)
        return result
    def Or(key1,key2):
        index1,index2=0,0
        result=[]
        while True:
            if(index1>=len(key1) or index1>=len(key2)):
                for i in range(index1,len(key1)):
                    result.append(key1[i])
                for i in range(index2,len(key2)):
                    result.append(key2[i])
                break
            if(key1[index1]==key2[index2]):
                result.append(key1[index1])
                index1=index1+1
                index2=index2+1
            elif(key1[index1]<key2[index2]):
                index1=index1+1
            elif(key1[index1]>key2[index2]):
                index2=index2+1
        result.sort()
        return result