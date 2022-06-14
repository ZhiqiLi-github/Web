# from pkg_resources import VersionConflict
from cmath import cos
from index import *
import numpy as np
from index import Index
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
            self.idf = np.load('../data/index/idf.npy')
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
                    # vector[index][key] = len(value)
                
            idf = np.array(idf)
            vector[vector == 0] = 0.1
            vector = np.log10(vector) + 1
            # idf = np.array(idf)S
            self.idf = np.log10(M/idf)
            idf = np.expand_dims(idf, axis=1)
            self.vector = vector * idf
            self.vector_std = self.vector / (np.sqrt(np.sum(self.vector**2, axis=0))+1e-8) 
            np.save('../data/index/idf.npy', self.idf)
            np.save('../data/index/vector.npy', self.vector)
            np.save('../data/index/vector_std.npy', self.vector_std)

    def Top_k_query(self, command, k):
        '''
            input: vector: vector of doc N*M
                   q_vector: vector of the query word 1*N
                   k: the top k you need
            output idx: the list of result  
        '''
        q_vector = np.zeros(self.vector_std.shape[1])
        keys = list(self.inverted_index.keys())
        for s in command:
            q_vector += self.vector_std[keys.index(s), :]

        # q_vector = self.str_to_vec(command)
        # q_vector = np.expand_dims(q_vector,axis=1)
        cosine = q_vector
        # cosine = cosine / self.vec_length
        ret = np.argpartition(-cosine, k)[:k]
        ret_cosine = cosine[ret]
        ret_idx = np.argsort(-ret_cosine)
        ret_cosine = ret_cosine[ret_idx]
        ret = ret[ret_idx]
        
        return ret, " ".join(command), ret_cosine

    def Fast_topk_query(self,command,k):
        if len(command) > 1:
            q_vector = self.str_to_vec(command) * self.idf
            q_vector = np.expand_dims(q_vector,axis=1)
            idx = []
            keys = list(self.inverted_index.keys())
            indexs = [keys.index(s) for s in command]
            idfs = [self.idf[index] for index in indexs]
            index = indexs[np.argmax(idfs)]
            idx = self.vector_std[index,:]==0
            idx = [not i for i in idx]
            vector_std = self.vector_std[:,idx]
            print(len(vector_std))
            if len(vector_std) < k:
                vector_std = self.vector_std
            cosine = np.sum(vector_std * q_vector, axis=0) / np.linalg.norm(q_vector)
        else:
            q_vector = np.zeros(self.vector_std.shape[1])
            keys = list(self.inverted_index.keys())
            for s in command:
                q_vector += self.vector_std[keys.index(s), :]
            cosine = q_vector
        ret = np.argpartition(-cosine, k)[:k]
        ret_cosine = cosine[ret]
        ret_idx = np.argsort(-ret_cosine)
        ret_cosine = ret_cosine[ret_idx]
        return ret, " ".join(command), ret_cosine

    def str_to_vec(self, list_str):
        vec = np.zeros(len(self.inverted_index))
        keys = list(self.inverted_index.keys())
        for s in list_str:
            vec[keys.index(s)] += 1
        return vec

if __name__ == "__main__":
    index = Index()
    inverted_index = index.inverted_index
    doc_dict, num_docs = index.get_doc()
    a = VSM(inverted_index,num_docs)
    a1,a2,a3 = a.Fast_topk_query(['government'],5)
    print(a1,a2,a3)