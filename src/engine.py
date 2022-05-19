import os
from index import Index
from search import bool_search, wildcard_search, phrase_search
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

        self.inverted_index = Index.MyReadII()

        self.term_dict = None
        self.doc_dict  = None
        self.search_method = [
            bool_search,
            wildcard_search,
            phrase_search
        ]
        pass

    def search(self, command):
        docID = self.search_method[self.state](command, self.inverted_index)
        return docID
        
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
        command_list = command.strip().split()
        if command_list[0] in self.command:
            self.command[command_list[0]](command_list[1:])
        else:
            return self.search(command_list), command_list[0] if len(command_list) == 1 else None

    def display_string(self, oneStr,key):
    # print(oneStr)
        index=0
        for i in range(len(oneStr)):
            if(oneStr[i:i+len(key)]==key):
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
        print('total:{}'.format(len(docIDs)))
        print(" ".join(str(i) for i in docIDs[:5]) + "...")
        for docID in docIDs[:5]:
            file_object = open(os.path.join(entry, str(docID)+'.html'))
            file=file_object.read()
            dispStr1,dispStr2,dispStr3 = self.display_string(file,key)
            print("\033[32;1m docID "+str(docID)+": \033[0m",end='')
            print(dispStr1,end='')
            print("\033[32;1m"+dispStr2+'\033[0m',end='')
            print(dispStr3)
            ## first detect if the index exists