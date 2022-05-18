from numpy import isin
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
        self.inverted_index = Index.ReadII()
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
            return self.search(command_list)

    def display(self, docID):
        print(docID)