
	# Use trace files of all ranks to calculate median computation times to be used for sleeping the program.
	# Warmups and ignored instructions have to be removed again.

import os

def main():

	WARMUPS_START = 3
	WARMUPS_END = 3048
	instrCount = 0

	fileList1 = os.listdir('trace/')
	fileList1.sort()
	numRanks = len(fileList1)
	fileList = []
	for item in fileList1:
		tempStr = "trace/" + item
		fileList.append(tempStr)

	#print fileList

	# numComputationTimes = -1
	# with open(fileList[0], 'r') as f:
	# 	for line in f:
	# 		numComputationTimes += 1

	compTimesOut = []

	listOfLists = [[] for x in xrange(numRanks)]

	file_tracker = 0
	#j = 0
	prevEndTime = 0

	numComputationTimes = 0

	# get lines that shall be removed in the future

	ignoreList = []
	with open('ignoreLines.txt', 'r') as f:
		for line in f:
			tempList = line.split()
			ignoreList = tempList

	#print ignoreList

	warmupsCompleteFlag = 0

	for file in fileList:
		#print file
		with open(file,"r") as f:
			for line in f:
				#print line

				instrCount += 1

				ignoreFlag = 0

				if warmupsCompleteFlag == 0:
					if instrCount >= WARMUPS_START or instrCount <= WARMUPS_END:
						ignoreFlag = 1				

				if str(instrCount) in ignoreList:
					ignoreFlag = 1

				words = line.split()
				name = words[0]
				startTime = float(words[3])
				endTime = float(words[4])

				if ignoreFlag == 0:
					if name != "MPI_Init":
						compTime = startTime - prevEndTime * 1000 * 1000 * 1000; # nanoseconds
						listOfLists[file_tracker].append(compTime)
						if file_tracker == 0:
							numComputationTimes += 1

				prevEndTime = endTime

				if warmupsCompleteFlag == 0:
					#other fixing
					if instrCount == WARMUPS_END:
						instrCount = WARMUPS_START - 1
						warmupsCompleteFlag = 1
						
						compTime = startTime - prevEndTime * 1000 * 1000 * 1000; # nanoseconds
						listOfLists[file_tracker].append(compTime)
						if file_tracker == 0:
							numComputationTimes += 1	
			file_tracker +=1


	for i in range(0,numComputationTimes):
		tempList = [item[i] for item in listOfLists]
		compTimesOut.append(median(tempList))

	file = open("comp_times.q", "a")
	for item in compTimesOut:
		file.write(str(item) + " ")
	file.close()
	print "Total no. of computation times = " + str(numComputationTimes)

def median(lst):
    n = len(lst)
    if n < 1:
            return None
    if n % 2 == 1:
            return sorted(lst)[n//2]
    else:
            return sum(sorted(lst)[n//2-1:n//2+1])/2.0


main()