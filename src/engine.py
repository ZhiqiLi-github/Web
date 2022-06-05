from itertools import product
import os
from pydoc import doc

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
            "topk": 3,
        }
        self.command = {
            "switch": self.switch,
            "open": self.open,
            "close": self.close,
            "top": self.change_k, 
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
    
    def change_k(self, k):
        k = int(k[0])
        if k > 0:
            self.top_k = k

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
                else:
                    if command_list[i] not in self.inverted_index:
                        raise Exception("No such word ...")

            if self.extend and self.state != 3:
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
        elif self.state == 1: 
            command_list = [command_list]
            
        return command_list
                    
    def switch(self, mode):
        if len(mode) > 1:
            print("Error: Only one parameter is needed!")
            return 
        mode = mode[0]
        
        if mode not in self.mode:
            print("Error: No such mode, please select from ['bool', 'wildcard', 'phrase', 'topk']")
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
            except Exception as exp:
                print("No such command ... ")
            return None
        else:
            ret = None
            try:
                ret = self.search(command)
            except Exception as exp:
                
                print(exp.args[0])
            return ret



    def display_topk_table(self, docIds, scores):
        
        print("-"*20+"top %3d"%(self.top_k)+'-'*2+'-'*20)
        print("|"+"-"*48+"|")
        print("|"+"Doc name".center(24, ' ')+"|"+"score".center(23, ' ')+"|")
        print("|"+"-"*48+"|")
        for i in range(self.top_k):
            name = self.doc_dict[docIds[i]]
            score_str = "%.4f"%(scores[i])
            print("|"+ name.center(24, ' ')+"|" +score_str.center(23, ' ')+"|")
            print("|"+"-"*48+"|")
        return        
    def display(self, result):
        if result is not None:
            if self.state != 3:
                for docIDs, key, disp in result:
                    self.display_res(docIDs, key, disp)
            else:
                docIDs, _ , scores = result[0]
                self.display_topk_table(docIDs, scores)

    def display_res(self, docIDs, key, disp, entry="../data/Reuters"):
        print("Search for", "\033[33;1m{}\033[0m".format(key), "total:", "\033[33;1m{}\033[0m".format(len(docIDs)))
        if len(docIDs) == 0:
            return 

        choice = 'n'
        if len(docIDs) > 20:
            while 1:
                choice = input("The answers may be too long to show all of them,\n do u wanna show them all?[y/n]")
                if choice not in ['y', 'n']:
                    choice = input("Please choose from [y, n]")
                else:
                    break
                
        if choice == 'n':
            print("Doc names: "+" ".join(self.doc_dict[idx] for idx in docIDs[:5]) + ' ...')

        else:
            print("Doc names: "+" ".join(self.doc_dict[idx]+'\n' if (cnt+1) % 5 == 0 else self.doc_dict[idx] for cnt, idx in enumerate(docIDs)) )
        if disp:
            if choice == 'y':
                docIDs_to_show = docIDs
            else:
                docIDs_to_show = docIDs[:5]
            for docID in docIDs_to_show:
                file_object = open(os.path.join(entry, self.doc_dict[docID]))
                file=file_object.read()
                # pos = self.inverted_index[key][1][docID][-1]
                print(self.doc_dict[docID])
                dispStr1,dispStr2,dispStr3 = self.display_string(file, key)
                print("\033[32;1m {}".format(self.doc_dict[docID])+": \033[0m",end='')
                print(dispStr1,end='')
                print("\033[32;1m"+dispStr2+'\033[0m',end='')
                print(dispStr3)
                ## first detect if the index exists
    def display_string(self, oneStr, key):
        list1 = oneStr.split(' ')
        m = {}
        list2 = []
        k = 0
        for i in range(len(list1)):
            oo = list1[i].strip('\n \t,.<>/\\;\'\"()@!#$%^&*?`+-')
            if len(oo) > 0:
                list2.append(oo)
                m[k] = i
                k +=1
        list2 = list(map(self.stem, list2))
        listkey = key.split(' ')
        idx = -1
        for i in range(len(list2)-len(listkey)+1):
            flag = True
            for j in range(len(listkey)):
                if list2[i + j] != listkey[j]:
                    flag = False
                    break
            if flag:
                idx = i
                break
        if idx != -1:
            length = 0
            r = ''
            b = m[idx]
            e = m[idx + len(listkey)-1]
            for i in range(b, e+1):
                r += list1[i] + ' '
                length += len(list1[i])+1
            begin = oneStr.find(r)
            minIndex = 0
            for i in range(20, 100):
                if begin - i <= 0:
                    minIndex = 0
                    break
                elif oneStr[begin - i] == ' ':
                    minIndex = begin - i
                    break
            maxIndex = 0
            for i in range(20, 100):
                if begin + i + length >= len(oneStr):
                    maxIndex = begin + i + length
                    break
                elif oneStr[begin+i+length] == ' ':
                    maxIndex = begin+length + i
                    break
            return "..."+oneStr[minIndex:begin],oneStr[begin:begin+length],oneStr[begin+length:maxIndex]+"..."
