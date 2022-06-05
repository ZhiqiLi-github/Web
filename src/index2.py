import os
import numpy as np
from stem import Stemmer
from gamma import *
import copy

#需要统计每个词出现的位置序列，以及doc序列，以及每个doc内的位置信息，再加上每个doc内的数量
#[[docID],[[positions1],[positions2],...[]],[nums]]
#位置信息是针对为去除标点而定的，单词经过了一定的过滤处理。
#
NUMDOC = 1000

def create_dictionary(src,dic_path,numdoc=NUMDOC):
	filenames = os.listdir(src)
	filenames.sort(key=lambda x:(int(x.split('.')[0])))
	doc_final = []
	doc_map = dict().fromkeys([filename.split('.')[0] for filename in filenames[0:numdoc]])
	idx = 0
	for key in doc_map.keys():
		doc_map[key] = idx+1
		idx+=1
	res = dict()
	for filename in filenames:
		path = src+filename
		with open(path,'r',encoding='ISO-8859-1') as f:
			doc = f.read()
		doc = doc.split(' ')
		doc_afterremove = []
		for o in doc:
			oo=o.strip('\n \t,.<>/\\;\'\"()@!#$%^&*?`+-:')
			if(len(oo)>0) and oo[0] not in ['0','1','2','3','4','5','6','7','8','9']:
				doc_afterremove.append(oo)
		stemmer = Stemmer()
		for word in doc_afterremove:
			word_1 = stemmer.stem(word)
			doc_final.append(word_1)
	doc_final.sort()
	res = res.fromkeys(doc_final)
	dictionary = []
	idx = 0
	for key,_ in res.items():
		dictionary.append([key,idx])
		idx += 1
	
	np.save(dic_path,dictionary)
	return res,doc_map

def create_index(src,Dictionary,docmap,numdoc=NUMDOC):
	filenames = os.listdir(src)
	dic_idx = {}
	keys = Dictionary.keys()
	for key in keys:
		dic_idx[key] = [0,{}]
	filenames.sort(key=lambda x:(int(x.split('.')[0])))
	doc_index = []
	for i in range(numdoc):
		doc_index.append(int(filenames[i].split('.')[0]))
	
	stemmer = Stemmer()
	for i in range(numdoc):
		pos = 0
		f = open(src+filenames[i])
		doc = f.read()
		doc = doc.split(' ')
		# print(len(doc))
		doc_afterremove = []
		for o in doc:
			oo=o.strip('\n \t,.<>/\\;\'\"()@!#$%^&*?`+-:')
			if(len(oo)>0) and oo[0] not in ['0','1','2','3','4','5','6','7','8','9']:
				doc_afterremove.append(oo)
		temp = dict()
		for o in doc_afterremove:
			oo = stemmer.stem(o)
			if oo in dic_idx:
				if oo not in temp:
					temp[oo] = []
				temp[oo].append(pos)
			pos+=1
		for key in temp.keys():
			dic_idx[key][1].update({i+1:temp[key]})
			dic_idx[key][0] += len(temp[key])
	# print(dic_idx)
	return dic_idx

def reduce_index(dest,Dictionary):
	res = []
	for key,value in Dictionary.items():
		temp = []#每个单词的所有编码，包括三个部分：docID，每个文档中的数量，在每个文档中的位置信息，因此一共是N+2个文档
		temp.append( bintohex(gammaencode ([value[0]])) )
		#对于数量，直接进行编码
		keys = []
		values = []
		for key_,value_ in value[1].items():
			keys.append(key_)
			values.append(value_)
			
		temp.append( bintohex(gammaencode ( countdaopaidis(keys) )))
		#计算docID的间距，然后进行编码
		
		for dis in values:
			temp.append( bintohex(gammaencode (countdaopaidis(dis))))
		res.append(temp)
		#对于距离进行编码
	res = np.array(res,dtype=object)
	np.save(dest+"index.npy",res)
	

def load_index(dic_path,index_file):
	res = dict()
	a = np.load(dic_path)

	res = res.fromkeys(a[:,0])
	i=0
	for key,_ in res.items():
		res[key] = a[i,1]
		i+=1
	index = np.load(index_file,allow_pickle=True)
	
	for key,idx in res.items():
		idx = int(idx)
		temp = [0,{}]
		temp[0] = gammadecode(hextobin(index[idx][0]))[0]
		keys = countdaopai (gammadecode(hextobin(index[idx][1])))
		for i,key_ in enumerate(keys):
			temp[1][key_] = countdaopai(gammadecode(hextobin(index[idx][i+2])))
		res[key] = temp
	return res

def vector_space(Dictionary,numdoc=NUMDOC):
	tf_matrix = np.zeros((len(Dictionary),numdoc))
	tf_idf_matrix = np.zeros((len(Dictionary),numdoc))
	df_matrix = np.zeros(len(Dictionary))
	idx = 0
	for key,_ in Dictionary.items():
		i = 0
		for doc in Dictionary[key][0]:
			tf_matrix[idx][doc-1] = int(Dictionary[key][2][i])
			i+=1
		df_matrix[idx] = np.sum(tf_matrix[idx,:]!=0)
		idx+=1
	
	for idx in range(len(Dictionary)):
		idx1 = tf_matrix[idx,:] == 0
		idx2 = tf_matrix[idx,:] !=0
		tf_idf_matrix[idx,idx2] = (1+np.log10(tf_matrix[idx,idx2]))*np.log10(numdoc/df_matrix[idx])
		tf_idf_matrix[idx,idx1] = 0
	return tf_idf_matrix


if __name__ == "__main__":
	src_file = '../data/Reuters/'
	dest_dir = '../data/index_file/'
	pathofdictionary = '../data/index_file/dictionary.npy'
	dictionary,doc_map = create_dictionary(src_file,pathofdictionary)
	# print(dictionary) 
	inverted_index = create_index(src_file,dictionary,doc_map,numdoc=NUMDOC)
	# print(inverted_index)
	#doc_idx是文档名前缀对应其在文档集中的编号
	reduce_index(dest_dir,inverted_index)
	a = np.load(dest_dir+"index.npy",allow_pickle=True)
	inverted_index = load_index(pathofdictionary,dest_dir+'index.npy')
	# space = vector_space(res)