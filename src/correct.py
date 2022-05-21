import numpy as np

def wrong_word(Dictionary,input_word):
	outputword = None
	if input_word in Dictionary:
		outputword = input_word
	else:
		listofword = []
		for word in Dictionary:
			if word[0] == input_word[0] and np.abs(len(word)-len(input_word))<=2:
				listofword.append(word)
		min_dis,min_idx = 10000,0
		idx = 0
		for word in listofword:
			dist = count_dist(word,input_word)
			if dist < min_dis:
				min_dis = dist
				min_idx = idx
			idx += 1


		outputword = listofword[min_idx]
		print("\033[31;1m{}\033[0m".format(input_word+' ---> ' + outputword))

	return outputword

def count_dist(word1,word2):
	dist = 0
	word3,word4 = word1.lower(),word2.lower()
	len1,len2 = len(word3),len(word4)
	matrix = np.zeros((len1,len2))
	for i in range(len1):
		matrix[i,0] = i
	for j in range(len2):
		matrix[0,j] = j
	for i in range(1,len1):
		for j in range(1,len2):
			if word3[i] == word4[j]:
				matrix[i,j] = min(matrix[i-1,j]+1,matrix[i,j-1]+1,matrix[i-1,j-1])
			else:
				matrix[i,j] = min(matrix[i-1,j]+1,matrix[i,j-1]+1,matrix[i-1,j-1]+1)
	dist = matrix[len1-1,len2-1]
	return dist

if __name__ == "__main__":
	print(count_dist("osio","snow"))