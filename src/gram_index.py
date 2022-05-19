import numpy as np
from index import *
class Two_gram:
    def __init__():
        pass
    def inverse_to_gram(II):
        '''
            input: II:inverse Index. dtype = dict
            output: IG: 2-gram Index. dtype = dict 
        '''
        IG = {}
        for r in list(II.keys()):
            s = '$' + r
            # print(s)
            for i in range(0, len(s) - 1):
                k = s[i:i+2]
                if not IG.__contains__(k):
                    IG[k] = []
                IG[k].append(r)
        return IG

if __name__ == '__main__':
    print("here test the Index compress...")
    Entry="../data/Reuters"
    fileNameList,indexList=os.listdir(Entry),[]
    for i in range(len(fileNameList)):
        tem=fileNameList[i]
        tem=tem.strip(".html")
        indexList.append(int(tem))
    indexList.sort()
    fileList=[]
    
    for i in range(100):#max(indexList)):
        filePath=Entry+'/'+str(i)+'.html'
        if(os.path.exists(filePath)):
            file_object = open(filePath)
            file=file_object.read()
            fileList.append(file)
        else:
            # print('\033[33;1m Warning: file %s not exist \033[0m' % (filePath))
            #print('\033[31m file %s not exist \033[0m' % (filePath))
            fileList.append('')
    II=Index.SimpleII(fileList)
    IG = Two_gram.inverse_to_gram(II)
    print(IG['sh'])
