def main():

	instrCount = 0
	allreduceCount = 0
	prevName = ""
	compTimesOut = []
	msgSizeOut = []
	tagOut = []
	prevEndTime = 0
	messageSize = 0
	tag = 0

	oldMsgSize = 0

	with open('finalMeta0.m', 'r') as f:
		for line in f:

			instrCount += 1

			words = line.split()
			name = words[0]
			startTime = float(words[3])
			endTime = float(words[4])

			# if name != "MPI_Init":
			# 	compTime = startTime - prevEndTime * 1000 * 1000 * 1000; # nanoseconds
			# 	compTimesOut.append(compTime)			

			if name == "MPI_Allreduce":
				file = open("allreduce.q","a")
				file.write(str(instrCount - 1) + " ")
				file.close()
				allreduceCount += 1

			if name == "MPI_Isend" or name == "MPI_Irecv":
				if len(words) > 8:
					messageSize = int(words[8])
					oldMsgSize = messageSize
				else:
					messageSize = oldMsgSize
				tag = words[7]
				msgSizeOut.append(messageSize)
				tagOut.append(tag)

			prevName = name
			prevEndTime = endTime


	# with open('computation_times.q','a') as compFile:
	# 	for item in compTimesOut:
	# 		compFile.write(str(item) + " ")

	with open('msg_sizes.q','a') as msgFile:
		for item in msgSizeOut:
			msgFile.write(str(item) + " ")			

	with open('taglist.q','a') as f:
		for item in tagOut:
			f.write(item + " ")	

	with open('length_meta.q','a') as f:
		f.write(str(instrCount) + " " + str(len(msgSizeOut)) + " " + str(allreduceCount))

	





			
main()

