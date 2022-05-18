from nltk.stem import PorterStemmer

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
    if len(ret) > 2 and ret[1] == 'NOT':
        tmp = ret[2]
        ret[2] = ret[1]
        ret[1] = ret[0]
        ret[0] = tmp
    return ret
    
def bool_parser(word_list):
    if isinstance(word_list, str):
        word_list = [word_list]
    word_list = infix2postfix(word_list)
    print(word_list)
    return word_list

def wildcard_parser(word):
    word = word.strip()
    
    if word[0] != '*':
        word = '$'+word
    if word[-1] != '*':
        word = word + '$'

    word_list = word.split('*')
    ret = []
    for word in word_list:
        ret.extend(word[i : i+2] for i in range(len(word)-1))
    print(ret)

if __name__ == "__main__":
    bool_parser("hello AND B AND ( NOT B )")
    wildcard_parser("app*le*s")