
from pyspark import SparkConf, SparkContext
from string import atoi
import time,sys
from itertools import chain, combinations

global t3
global tot_cnt
tot_cnt=0
def addStrings(x,y,nRows):
	output = str(bin(int(x,2) | int(y,2)))[2:]
	output = "0"*(nRows.value-len(output)) + output
	return output


def formatdata(x,nRows):
	'''
		for conversion of row in database to bitstring 
		for example if row is 2 a b c where 2 is the transaction id and total transactions is 5
		then output is ( (a,"01000"), (b,"01000"), (c,"01000"))
	'''
	output = []
	temp = '0' * nRows.value
	# print x[0].value
	temp = str(temp[:int(x[0])-1]) + '1' + str(temp[int(x[0]):])
	for i in range(1,len(x)):
		output.append((x[i],temp))
	return output


def find_freqItems(data,nRows,minRF):


	mapping = data.flatMap(lambda x: [(y,1) for y in x])

	

	reduced = mapping.reduceByKey(lambda x,y:x+y)
	freqItems = reduced.filter(lambda x:x[1]>=minRF.value*nRows.value)
	return freqItems

	
def generateCandidateSetOfLength2(data):
	output = []
	for i in range(0,len(data)):
		for j in range(i+1,len(data)):
			output.append(data[i]+data[j])
	return output



def generateCandidateSet(data):
	return data.map(lambda x:(tuple(x[:-1]),[x[-1]])).reduceByKey(lambda x,y:x+y).flatMap(lambda x:[list(x[0])+[x[1][i],x[1][j]] for i in range(0,len(x[1])) for j in range(i+1,len(x[1]))])

def update(x,GlobalfreqItemsWithOutBitmap):
	x = list(x)
	least = GlobalfreqItemsWithOutBitmap.value[x[0]]
	least_v = x[0]
	for i in x:
		y = GlobalfreqItemsWithOutBitmap.value[i]
		if y<least:
			least = y
			least_v = i
		elif y==least and least_v < i:
			least_v = i
	x.remove(least_v)
	return list(x) + [least_v]

def mapper(x,candidateset):
	# x = x.strip().split(",")
	output = []
	pos = 0
	for i in candidateset:
		a = 0
		b = 0
		c = 0
		for item in i[:-1]:
			if item in x:
				a=1
				b=1
				break
		if i[-1] in x:
			a = 1
			c = 1
		if(a==1 or b&c==1):
			output.append((pos,[a,b&c]))
		pos += 1
	return tuple(output)

def mapper1(x,y):
	a = 0
	b = 0
	c = 0
	for item in y[:-1]:
		if item in x:
			a=1
			b=1
	if y[-1] in x:
		a = 1
		c = 1
	return (str(y),[a,b&c])

def addvalues(x,y):
	return [x[0]+y[0],x[1]+y[1]]


def check(x,GlobalfreqItemsWithOutBitmap,nRows,minCS,maxOR,candidateset):
	pattern = candidateset[x[0]]
	#global tot_cnt
	CS = x[1][0]
	OR = x[1][1]
	OR_deno = GlobalfreqItemsWithOutBitmap.value[pattern[-1]]
	value = int(str(len(str(CS)))+ str(CS) + str(len(str(OR)))+ str(OR))
	if float(CS)/nRows.value>=minCS.value and float(OR)/OR_deno<=maxOR.value:
		#tot_pat=tot_pat+1
		return (pattern, value)
	elif float(OR)/OR_deno<=maxOR.value:
		#tot_pat=tot_pat+1
		return (pattern, 0)
	else:
		return (pattern, -1)

def ParallelCmine(sc,inputFile,numPartitions):
	global t3
	global tot_cnt
	
	# load the given data in RDD
	data = sc.textFile(inputFile,numPartitions)


	#find no of rows i.e no of transactions and broadcast it 
	nRows = sc.broadcast(data.count())
	
	# convertion of each transaction from string to list of itemss
	data2 = data.map(lambda x:x.strip().encode("ascii", "ignore").split(' '))
	output = sc.emptyRDD()
	t3 = time.time()
	t4 = time.time()

	#bitmap of each frequent item
	freqItemsWithOutBitmap = find_freqItems(data2,nRows,minRF)
	# freqItems = freqItemsWithOutBitmap
	#only the frequent Itmes removing the bitmap of each frequent item
	coveragePatterns = freqItemsWithOutBitmap.filter(lambda x:x[1]>=minCS.value*nRows.value).map(lambda x:[x[0], x[1]])
	freqItems = freqItemsWithOutBitmap.map(lambda x:[x[0]])

	# output freqItems
	output = output.union(coveragePatterns)
	
	#Convert the TIDs of freq element to dict to access it easy
	freqItemsWithOutBitmap = freqItemsWithOutBitmap.collectAsMap()
	
	
	#broadcasting the TIDs of frequent Itmes
	GlobalfreqItemsWithOutBitmap = sc.broadcast(freqItemsWithOutBitmap)
		
	#get the candidateset from the freq itmes
	candidateset = generateCandidateSetOfLength2(freqItems.collect())

	#tot_cnt=tot_cnt+len(candidatese)

	candidateset = sc.parallelize(candidateset,numPartitions)
	
	size = 2
	while True:
		if candidateset.isEmpty():
			break
		# temp = []
		candidateset = candidateset.map(lambda x:update(x,GlobalfreqItemsWithOutBitmap))

		candidateset = candidateset.collect()
		tot_cnt=tot_cnt+len(candidateset)
		
		temp = data2.flatMap(lambda x:mapper(x,candidateset))
		
		temp = temp.reduceByKey(lambda x,y:addvalues(x,y))

		
		temp = temp.map(lambda x:check(x,GlobalfreqItemsWithOutBitmap,nRows,minCS,maxOR,candidateset))
		
		coveragePatterns = temp.filter(lambda x:x[1]>=1).map(lambda x:[x[0], x[1]])
		
		NO = temp.filter(lambda x:x[1]!=-1).map(lambda x:x[0])

		output = output.union(coveragePatterns)
		candidateset = generateCandidateSet(NO)

		
		t5 = time.time()
		
		t4 = t5
		size += 1

		
	return output.collect()



if __name__ == "__main__":
	global t3
	global tot_cnt
	
	APP_NAME = "Parallel-Cmine"

	conf = SparkConf().setAppName(APP_NAME)
	
	sc = SparkContext(conf=conf)
	
	inputFile = sys.argv[5]
	minrf = float(sys.argv[1])
	mincs = float(sys.argv[2])
	maxor = float(sys.argv[3])
	numPartitions = int(sys.argv[4])
	data = sys.argv[6]


	minRF = sc.broadcast(minrf)
	minCS = sc.broadcast(mincs)
	maxOR = sc.broadcast(maxor)
	GlobalfreqItemsWithTIDS = sc.broadcast([])
	nRows = sc.broadcast(0)
	t1 = time.time()
	output = ParallelCmine(sc,inputFile,numPartitions)
	t2 = time.time()
	

	count = len(output)
	fout = open(sys.argv[7], 'a')
	
	fout.write("cmine_mapreduce"+","+str(minrf)+","+str(mincs)+","+str(maxor)+","+str(numPartitions)+","+str(len(output))+","+inputFile+","+str(t3-t1)+","+str(t2-t1)+",total_patterns: "+str(tot_cnt)+"\n")
	fout.close()
	
