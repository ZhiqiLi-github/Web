from parser import bool_parser, wildcard_parser
# from parser import bool_parser
from ast import Pass
from tkinter.tix import Tree
from index import *
def inquire(key, index):
    ret = []
    if key in index:
        ret = list(index[key][1].keys())
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

    return [stack[-1]], [postfix_string[-1] if len(postfix_string) == 1 else None]

def wildcard_search(command, two_gram_index, inverted_index):
    word_list = wildcard_parser(command)
    ret = [two_gram_index[word_list[0]]]
    for word in word_list[1:]:
        ret.append(two_gram_index[word])
        bool_op_and(ret)
        if len(ret[-1]) == 0:
            break
    
    ans = []
    for word in ret[-1]:
        ids, strs = bool_search(word, inverted_index)
        ans.append((ids[-1], strs[-1]))

    ret = list(zip(*ans))
    return ret

def phrase_search(command, index):
    '''
        input: command: string of the pharse
               index: the invert index of the doc
        output: the index of the doc
    '''
    ori = command
    command = Parser.parse(ori)
    command = Parser.stem(command)
    invert1 = index[command[0]][1]
    for s in command[1 :]:
        # print(s)
        new_invert = []
        invert2 = index[s][1]
        d1 = 0
        d2 = 0
        # print(len(invert1), len(invert2))
        while True:
            # print(d1, d2)
            if d1 >= len(invert1) or d2 >= len(invert2) :
                break
            if invert1[d1][0] == invert2[d2][0]:
                p1 = invert1[d1][1]
                p2 = invert2[d2][1]
                i1 = 0
                i2 = 0
                tem_pos = []
                while True:
                    if  i1 >= len(p1) or i2 >= len(p2):
                        break
                    if p1[i1] + 1 == p2[i2]:
                        tem_pos.append(p2[i2])
                        i1 += 1
                        i2 += 1
                    elif p1[i1] + 1 > p2[i2]:
                        i2 += 1
                    elif p1[i1] + 1 < p2[i2]:
                        i1 += 1
                if len(tem_pos) != 0:
                    new_invert.append([invert1[d1][0], tem_pos])
                if d1 < len(invert1):
                    d1 += 1
                if d2 < len(invert2):
                    d2 += 1

            elif invert1[d1][0] > invert2[d2][0] :
                d2 += 1
            elif invert1[d1][0] < invert2[d2][0] :
                d1 += 1
        invert1 = new_invert

    doc_ret = []
    for i in range(len(invert1)):
        doc_ret.append(invert1[i][0])
    return [doc_ret], [ori]

if __name__ == "__main__":
    # a = list(range(0,100,2))
    # b = list(range(1,100))
    # stack = [a]
    # print(stack)

    # # bool_op_and(stack)
    # bool_op_not(stack, 100)
    # # bool_op_or(stack)
    # print(stack)
    print("here test the Index compress...")
    Entry="../data/Reuters"
    fileNameList,indexList=os.listdir(Entry),[]
    for i in range(len(fileNameList)):
        tem=fileNameList[i]
        tem=tem.strip(".html")
        indexList.append(int(tem))
    indexList.sort()
    fileList=[]
    for i in range(100):#max(indexList)):
        filePath=Entry+'/'+str(i)+'.html'
        if(os.path.exists(filePath)):
            file_object = open(filePath)
            file=file_object.read()
            fileList.append(file)
        else:
            # print('\033[33;1m Warning: file %s not exist \033[0m' % (filePath))
            #print('\033[31m file %s not exist \033[0m' % (filePath))
            fileList.append('')
    II=Index.SimpleII(fileList)
    a = " is likely"
    a = Parser.parse(a)
    a = Parser.stem(a)
    # print(II.keys())
    # a = ['to', 'be']
    print(phrase_search(a, II))
