# Web
- language: python
- required module: os, nltk, json, pickle
- (pip install directly) 

### 0. Simple Retrieval

A simple retrieval sample is shown in ``src\console.py``, to run it by input ``python console.py``  to ``cmd`` or ``powershell`` in the folder of ``src`` easily.  ``Powershell`` is recommended, for  color is not supported by ``cmd``.

In this sample, a simple bool retrieval is  supported, by the bool expression must be written in postfix. For example ``NOT consign AND continue`` must be written as ``consign NOT continue AND``  

If the inquire have no bool operator, the result will include a string with the key word in it.

### 1.Index

The format of the inverse index is as follow:

```
key1:{
	freq1,
	[
	[docID1,[pos1,pos2,....]],
	[docID2,[pos1,pos2,....]],
	]
}
key2:{
	freq2,
	[
	[docID1,[pos1,pos2,....]],
	[docID2,[pos1,pos2,....]],
	]
}
...
```

For compress, the format is as follow:

```
key_num,key1_len,key1,key2_len,key2,...
freq1,docID1,pos_num,pos1,pos2-pos1,...docID2-docID1,pos_num,pos1,pos2-pos1,...
freq2,docID2,pos_num,pos1,pos2-pos1,...docID2-docID1,pos_num,pos1,pos2-pos1,...
```

All bytes will number and bytes will convert to VB.

Inverse index is stored in ``II.json II.bit`` in ``.\data``(``II.json`` is stored in the format of json and ``II.bit`` is written to file by pickle), and the compressed inversed index is stored in ``II.bin``

**``II.json`` is to large which cannot be upload to github, if you want to use it, ``Index.WriteII(II,mode='json')`` can generate it。**

To construct and use Index, refer to ``src\Index.py``.

