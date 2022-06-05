from parser import bool_parser, wildcard_parser
# from parser import bool_parser
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
    return stack[-1], postfix_string[-1] if len(postfix_string) == 1 else " ".join(command), len(postfix_string) == 1

def wildcard_search(command, two_gram_index, inverted_index):
    word_list = wildcard_parser(command)
    set1 = set(two_gram_index[word_list[0]])
    for word in word_list[1:]:
        set2 = set(two_gram_index[word])
        set1 = set1.intersection(set2)
        if len(set1) == 0:
            break
    ans = []
    ret = list(set1)
    print(ret)
    for word in ret:
        ids, strs, disp = bool_search([word], inverted_index)
        ans.append((ids, strs, disp))

    # ret = list(zip(*ans))
    ret = ans
    return ret

def phrase_search(command, index):
    '''
        input: command: string of the pharse
               index: the invert index of the doc
        output: the index of the doc
    '''
    ori = command
    invert1 = index[command[0]][1]
    for s in command[1 :]:
        # print(s)
        new_invert = {}
        invert2 = index[s][1]
        key1 = set(invert1.keys())
        key2 = set(invert2.keys())

        key = key1.intersection(key2)

        # print(len(invert1), len(invert2))
        for docID in key:
            # print(d1, d2)
            p1 = invert1[docID]
            p2 = invert2[docID]
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
                new_invert[docID] = tem_pos

        invert1 = new_invert

    doc_ret = list(invert1.keys())
    doc_ret.sort()
    return doc_ret, " ".join(ori), False

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
