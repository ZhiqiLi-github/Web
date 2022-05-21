from itertools import product
import os

from vsm import VSM
from search import bool_search, wildcard_search, phrase_search
from parser import synonym
from correct import wrong_word
from index import Index, PorterStemmer

class SearchEngine:
    def __init__(self) -> None:
        self.state = 0 # 0 for bool, 1 for wildcard search, 2 for phrase search
        self.mode = {
            "bool" : 0,
            "wildcard": 1,
            "phrase": 2,
        }
        self.command = {
            "switch": self.switch,
            "open": self.open,
            "close": self.close,
        }


        self.index = Index()
        self.inverted_index = self.index.inverted_index
        self.doc_dict, self.num_docs = self.index.get_doc()
        self.two_gram_index = self.index.two_gram
        self.vsm = VSM(self.inverted_index, self.num_docs)
        self.top_k = 5
        # print(self.inverted_index['search'])
        self.search_method = [
            lambda command: bool_search(command, self.inverted_index),
            lambda command: wildcard_search(command, self.two_gram_index, self.inverted_index),
            lambda command: phrase_search(command, self.inverted_index),
            lambda command: self.vsm.Top_k_query(command, self.top_k)
        ]
        self.stemmer = PorterStemmer()

        self.correct = False
        self.extend = False
        pass
    
    def open(self, command):
        old_value_correct = self.correct
        old_value_extend = self.extend
        flag = True
        for i in range(len(command)):
            if command[i] == 'correct':
                self.correct = True
            elif command[i] == 'extend':
                self.extend = True
            else: 
                print("Error: Only support featrue in [\"correct\", \"extend\"]")
                self.correct = old_value_correct
                self.extend = old_value_extend
                flag = False
                break
                
        if flag: 
            print("Open " + ", ".join(command)+" successfully!")
    def close(self, command):
        old_value_correct = self.correct
        old_value_extend = self.extend
        flag = True
        for i in range(len(command)):
            if command[i] == 'correct':
                self.correct = False
            elif command[i] == 'extend':
                self.extend = False
            else: 
                print("Error: Only support featrue in [\"correct\", \"extend\"]")
                self.correct = old_value_correct
                self.extend = old_value_extend
                flag = False
                break
        if flag: 
            print("Close " + ", ".join(command)+" successfully!")
    
    def search(self, command):
        command_list = self.preprocess(command)
        res = list(self.search_method[self.state](com) for com in command_list)

        if self.state == 1:
            res = res[-1]
        return res
    
    def stem(self, word: str):
        return self.stemmer.stem(word)
    
    def preprocess(self, command):
        command_list = command.strip().split()
        word_list = [i for i in command_list]
        if self.state != 1:
            word_idx = [i for i in range(len(command_list)) if command_list[i] not in ["NOT", "AND", "OR"]]
            for i in word_idx:
                command_list[i] = self.stem(command_list[i])
                if self.correct:
                    command_list[i] = self.stem(wrong_word(self.inverted_index, command_list[i]))

            if self.extend:
                all_words = list(synonym(word_list[i]) for i in word_idx)
                tmp = list(product(*all_words))
                tmp = list(zip(*tmp))
                length = len(tmp[0])
                res = [[i]*length for i in command_list]
                for i in range(len(word_idx)):
                    res[word_idx[i]] = tmp[i] 
                command_list = list(zip(*res))
                pass
            else:
                command_list = [command_list]
        else: 
            command_list = [command_list]
        return command_list
                    
    def switch(self, mode):
        if len(mode) > 1:
            print("Error: Only one parameter is needed!")
            return 
        mode = mode[0]
        
        if mode not in self.mode:
            print("Error: No such mode, please select from ['bool', 'wildcard', 'phrase']")
            return 

        self.state = self.mode[mode]
        print("Switch search mode to "+mode)

    def interpreter(self, command: str):
        if len(command) == 0:
            return None
        command = command.strip()
        if command[0] == ':':
            command = command[1:]
            command_list = command.strip().split()
            try: 
                print(command_list)
                self.command[command_list[0]](command_list[1:])
            except:
                print("No such command ... ")
            return None
        else:
            return self.search(command)

    def display_string(self, oneStr, key, pos):
        # print(oneStr)
        index = pos
        for i in range(index, len(oneStr)):
            if( self.stem(oneStr[i:i+len(key)]) == key ):
                index=i
                break
        # print(index)
        for i in range(20,100):
            if(index-i<=0):
                minIndex=0
                break
            elif(oneStr[i]==' '):
                minIndex=index-i
                break
        for i in range(20,100):
            if(index+i>=len(oneStr)):
                maxIndex=len(oneStr)
                break
            elif(oneStr[i]==' '):
                maxIndex=index+i
                break
        return "..."+oneStr[minIndex:index],oneStr[index:index+len(key)],oneStr[index+len(key):maxIndex]+"..."

    def display(self, result):
        if result is not None:
            for docIDs, key, disp in result:
                self.display_res(docIDs, key, disp)

    def display_res(self, docIDs, key, disp, entry="../data/Reuters"):
        print("Search for", "\033[33;1m{}\033[0m".format(key), "total:", "\033[33;1m{}\033[0m".format(len(docIDs)))
        if len(docIDs) == 0:
            return 
        print("docIDs: "+" ".join(str(i) for i in docIDs[:5]) + "...")
        if disp:
            for docID in docIDs[:5]:
                file_object = open(os.path.join(entry, self.doc_dict[docID]))
                file=file_object.read()
                pos = self.inverted_index[key][1][docID][-1]
                dispStr1,dispStr2,dispStr3 = self.display_string(file, key, pos)
                print("\033[32;1m docID "+str(docID)+": \033[0m",end='')
                print(dispStr1,end='')
                print("\033[32;1m"+dispStr2+'\033[0m',end='')
                print(dispStr3)
                ## first detect if the index exists