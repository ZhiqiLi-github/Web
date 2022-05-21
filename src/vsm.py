# from pkg_resources import VersionConflict
from index import *
import numpy as np

class VSM:
    def __init__(self, II, M) -> None:
        '''
            input: II, dict of Index
                    M, doc number 
            output: Vector N * M
            N is the word number
            M is the doc number
        '''
        self.inverted_index = II
        if os.path.exists('../data/index/vector.npy') and os.path.exists('../data/index/vector_std.npy'):
            self.vector = np.load('../data/index/vector.npy')
            self.vector_std = np.load('../data/index/vector_std.npy')
        else:
            n_words = len(list(II.keys()))
            idf = []
            # idf = np.zeros(n_words)
            vector = np.zeros((n_words, M))
            # for index, l in enumerate(II):
            #     idf.append(len(l))
            #     for k, v in l.items():
            #         vector[index][k] = len(v)
            for index, (k, v) in enumerate(II.items()):
                idf.append(v[0])
                keys, values = list(v[1].keys()), list(v[1].values())
                vector[index][keys] = list(map(len, values))
                # for key, value in v[1].items():
                #     vector[index][key] = len(value)
                
            idf = np.array(idf)
            vector[vector == 0] = 0.1
            vector = np.log10(vector) + 1
            # idf = np.array(idf)S
            idf = np.log10(n_words/idf)
            idf = np.expand_dims(idf, axis=1)
            self.vector = vector * idf
            self.vector_std = self.vector / (np.sqrt(np.sum(self.vector**2, axis=0))+1e-8) 
            np.save('../data/index/vector.npy', self.vector)
            np.save('../data/index/vector_std.npy', self.vector_std)

    def Top_k_query(self, command, k):
        '''
            input: vector: vector of doc N*M
                   q_vector: vector of the query word 1*N
                   k: the top k you need
            output idx: the list of result  
        '''
        q_vector = self.str_to_vec(command)
        q_vector = np.expand_dims(q_vector,axis=1)
        cosine = np.sum(self.vector_std * q_vector, axis=0)
        ret = list(np.argpartition(cosine, k)[:k])
        ret.sort()
        return ret, " ".join(command), False

    def str_to_vec(self, list_str):
        vec = np.zeros(len(self.inverted_index))
        keys = list(self.inverted_index.keys())
        for s in list_str:
            vec[keys.index(s)] += 1
        return vec