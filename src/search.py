from parser import bool_parser

def inquire(key, index):
    ret = []
    if key in index:
        ret = list(index[key][1][i][0] for i in range(len(index[key][1])))
    return ret

def bool_op_and(stack, *other):
    l1 = stack.pop()
    l2 = stack.pop()
    i, j = 0, 0
    ret = []
    while i < len(l1) and j < len(l2):
        if l1[i] == l2[j]:
            ret.append(l1[i])
            i += 1
            j += 1
        elif l1[i] < l2[j]:
            i += 1
        else:
            j += 1
    stack.append(ret)
    
def bool_op_or(stack, *other):
    l1 = stack.pop()
    l2 = stack.pop()
    i, j = 0, 0
    ret = []
    while i < len(l1) and j < len(l2):
        if l1[i] == l2[j]:
            ret.append(l1[i])
            i += 1
            j += 1
        elif l1[i] < l2[j]:
            ret.append(l1[i])
            i += 1
        else:
            ret.append(l2[j])
            j += 1
    
    ret.extend(l1[i:]+l2[j:])
    stack.append(ret)
 
    
def bool_op_not(stack, num_doc):

    l = [0] + stack.pop() + [num_doc+1]
    ret = sum(list(list(range(l[i]+1, l[i+1])) for i in range(len(l)-1)), start=[])
        
    stack.append(ret)
    
def bool_search(command, index, num_doc = 10788):
    OPRAND = ["NOT", "AND", "OR"]
    postfix_string = bool_parser(command)
    stack = []
    for token in postfix_string:
        if token in OPRAND:
            eval('bool_op_'+token.lower())(stack, num_doc)
        else:
            stack.append(inquire(token, index))

    return stack[-1]

def wildcard_search(command, index):
    pass

def phrase_search(command, index):
    pass

if __name__ == "__main__":
    a = list(range(0,100,2))
    b = list(range(1,100))
    stack = [a]
    print(stack)

    # bool_op_and(stack)
    bool_op_not(stack, 100)
    # bool_op_or(stack)
    print(stack)