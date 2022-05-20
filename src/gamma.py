from operator import mod

from numpy import zeros



def gamma_encode_number(a):
	temp = bin(a)
	res = temp.replace('0b','')
	le = len(res)
	res = res[1:len(res)]
	for i in range(le):
		if i ==0:
			res = '0'+res
		else:
			res = '1'+res
	return res
	#返回的是字符串

def gammaencode(numbers):
    bytestream = ""
    for n in numbers:
        byte = gamma_encode_number(n)
        bytestream += (byte)
    # if numbers[0] == 1:
    #     bytestream = "g"+bytestream
	#标识序列的开头为1
    return bytestream

def bintohex(bytestream):
	res = ""
	# have_one = 0
	# if bytestream[0] == 'g':
	# 	have_one = 1
	# 	bytestream = bytestream[1:]
	for i in range(len(bytestream)//4):
		num = hex(int(bytestream[len(bytestream)-i*4-1])*1+int(bytestream[len(bytestream)-i*4-2])*2
		+int(bytestream[len(bytestream)-i*4-3])*4+int(bytestream[len(bytestream)-i*4-4])*8)
		res = str(num).replace('0x','') + res
	num = 0
	for i in range(len(bytestream) % 4):
		num += int(bytestream[i])*(2**(len(bytestream)%4-i-1))
	res = str(hex(num)).replace('0x','') + res
	res = str(4-len(bytestream)%4)+res
	return res
def bintoint(bytestream):
	num=0
	for i in range(len(bytestream)):
		num += int(bytestream[i])*(2**(len(bytestream)-i-1))
	res = str(num)
	return res

def hextobin(number):
	res = ""
	for i in range(len(number)):
		temp = "0x"+number[i]
		temp1 = str(bin(int(temp,base=16)))[2:]
		for i in range(4-len(temp1)):
			temp1 = '0'+temp1
		res += temp1
	return res

def gammadecode(bytestream):
	numof1 = 0
	res = []
	i=0
	numof0 = int(bintoint(bytestream[0:4]))
	bytestream = bytestream[4+numof0:]
	while i < len(bytestream):
		if bytestream[i] == '0':
			temp = "1"+bytestream[i+1:i+1+numof1]
			res.append(int(bintoint(temp)))
			i+=numof1
			numof1 = 0
		else:
			numof1+=1
		i+=1
	return res

def countdaopaidis(daopai):
    daopaidis = daopai.copy()
    for i in range(len(daopai)):
        if i == 0:
            daopaidis[i] = daopai[i]
        else:
            daopaidis[i] = daopai[i] - daopai[i - 1]
    return daopaidis

def countdaopai(daopaidis):
    daopai = daopaidis.copy()
    for i in range(len(daopaidis)):
        daopai[i] = sum(daopaidis[0: i + 1])
    return daopai

if __name__ == "__main__":
	# print(gamma_encode_number(511))
	temp = gammaencode([1,341,1024,34342])
	print(temp)
	print(len(temp))
	temp1 = bintohex(temp)
	print(temp1)
	temp2 = (hextobin(temp1))
	print(temp2)
	print(gammadecode(temp2))