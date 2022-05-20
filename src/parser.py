from nltk.stem import PorterStemmer
import copy

stemmer = PorterStemmer()
OPRAND = {
    "NOT": 2, 
    "AND": 1,
    "OR": 0,
}

def infix2postfix(sequence):
    ret = []
    op_stack = []
    for token in sequence:
        if token == '(':
            op_stack.append(token)
        elif token == ')':
            top = op_stack.pop()
            while top != '(':
                ret.append(top)
                top = op_stack.pop()
        elif token in OPRAND:
            while len(op_stack) and op_stack[-1] != '(' and OPRAND[op_stack[-1]] >= OPRAND[token]:
                ret.append(op_stack.pop())
            op_stack.append(token)
        else:
            ret.append(stemmer.stem(token))

    while len(op_stack):
        ret.append(op_stack.pop())

    return ret
    
def bool_parser(command_list):
    if isinstance(command_list, str):
        word_list = [copy.deepcopy(command_list)]
    else:
        word_list = [i for i in command_list ]
    after_parser = infix2postfix(word_list)
    return after_parser

def wildcard_parser(word):
    if len(word) != 1:
        raise Exception("Wildcard search only supports single word")
    word = word[0].strip()
    
    if word[0] != '*':
        word = '$'+word
    if word[-1] != '*':
        word = word + '$'

    word_list = word.split('*')
    ret = []
    for word in word_list:
        ret.extend(word[i : i+2] for i in range(len(word)-1))

    return ret

if __name__ == "__main__":
    bool_parser("hello AND B AND ( NOT B )")
    wildcard_parser("app*le*s")