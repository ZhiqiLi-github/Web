# from pkg_resources import VersionConflict
from index import *
import numpy as np

class vsm:
    def __init__(self) -> None:
        pass
    
    def vector_from_dict(II, M):
        '''
            input: II, dict of Index
                    M, doc number 
            output: Vector N * M
            N is the word number
            M is the doc number
        '''
        idf = np.zeros(len(II))
        vector = np.zeros((len(II), M))
        # for index, l in enumerate(II):
        #     idf.append(len(l))
        #     for k, v in l.items():
        #         vector[index][k] = len(v)
        for index, (k, v) in enumerate(II.items()):
            # idf.append(v[0])
            for t in v[1]:
                idf[index] += 1
                vector[index][t[0]] = len(t[1])
        vector[vector == 0] = 0.1
        vector = np.log10(vector) + 1
        # idf = np.array(idf)
        idf = np.log10(10/idf)
        print(vector.shape)
        idf = np.expand_dims(idf, axis=1)
        vector = vector * idf
        print(vector.shape)
        vector_std = vector / (np.sqrt(np.sum(vector**2, axis=0))+1e-8)
        return vector, vector_std
    def Top_k_query(vector_std, q_vector, k):
        '''
            input: vector: vector of doc N*M
                   q_vector: vector of the query word 1*N
                   k: the top k you need
            output idx: the list of result  
        '''
        q_vector = np.expand_dims(q_vector,axis=1)
        cosine = np.sum(vector_std * q_vector, axis=0)
        return np.argsort(cosine)[-k:]
    def str_to_vec(list_str, II):
        vec = np.zeros(len(II))
        keys = list(II.keys())
        for s in list_str:
            vec[keys.index(s)] = 1
        return vec
            
            

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
            print('\033[33;1m Warning: file %s not exist \033[0m' % (filePath))
            #print('\033[31m file %s not exist \033[0m' % (filePath))
            fileList.append('')
    II=Index.SimpleII(fileList)
    print(len(II))
    v, vector_std = vsm.vector_from_dict(II, 100)
    q = np.random.randint(0, len(II), 10)
    q_v = np.zeros(len(II))
    q_v[q] = 1
    print(vsm.Top_k_query(vector_std, q_v, 10))
    # print(v)
