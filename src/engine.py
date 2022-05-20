import os

from vsm import VSM
from search import bool_search, wildcard_search, phrase_search
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
            "switch": self.switch
        }


        self.index = Index()
        self.inverted_index = self.index.inverted_index
        self.doc_dict, self.num_docs = self.index.get_doc()
        self.two_gram_index = self.index.inverse_to_gram()
        self.vsm = VSM(self.inverted_index, self.num_docs)
        self.top_k = 5
        # print(self.inverted_index['search'])
        self.search_method = [
            lambda command: bool_search(command, self.inverted_index),
            lambda command: wildcard_search(command, self.two_gram_index, self.inverted_index),
            lambda command: phrase_search(command, self.inverted_index),
            lambda command: self.vsm.Top_k_query(command, self.top_k)
        ]
        pass

    def search(self, command):
        return self.search_method[self.state](command)
        
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
            return None, None
        command = command.strip()
        if command[0] == ':':
            command = command[1:]
            command_list = command.strip().split()
            try: 
                self.command[command_list[0]](command_list[1:])
            except:
                print("No such command ... ")
            return None, None
        else:
            return self.search(command.split())

    def display_string(self, oneStr, key, pos):
        # print(oneStr)
        stemmer = PorterStemmer()
        index = pos
        for i in range(index, len(oneStr)):
            if( stemmer.stem(oneStr[i:i+len(key)]) == key):
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

    def display(self, docIDs, key, entry="../data/Reuters"):
        print("Search for", "\033[33;1m{}\033[0m".format(key), "total:", "\033[33;1m{}\033[0m".format(len(docIDs)))
        if len(docIDs) == 0:
            return 
        print(" ".join(str(i) for i in docIDs[:5]) + "...")
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