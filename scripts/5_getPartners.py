def main():

	firstLineFlag = 1

	with open('finalMeta0.m', 'r') as f:
		#streakRunningFlag = 0
		streakCount = 0
		previousName = ""
		for line in f:
			words = line.split()
			name = words[0]

			if name == "MPI_Irecv" or name == "MPI_Isend":
				if name == "MPI_Isend":
					partnerRank = words[6]
				else:
					partnerRank = -2
				file = open("partner.q","a")

				if previousName == "MPI_Isend" or previousName == "MPI_Irecv":					
					
					file.write(str(partnerRank) + " ")
					#file.close()
				else:
					if firstLineFlag == 1:
						firstLineFlag = 0
						file.write(str(partnerRank) + " ")
					else:
						file.write("\n")
						file.write(str(partnerRank) + " ")
						#file.close()
				file.close()

			previousName = name

			# if name == "MPI_Isend" or name == "MPI_Irecv":
			# 	streakCount += 1
			# 	previousName = name

			# elif name == "MPI_Wait" and (previousName == "MPI_Isend" or previousName == "MPI_Irecv"):
			# 	previousName = name

			# 	sender = words[5]
			# 	recver = words[6]

			# 	endingOpCount = int(words[2]) - 1
			# 	file = open('streak.out', 'a')
			# 	outputStr = str(streakCount) + " " + str(endingOpCount) + " " + sender + " " + recver + "\n"
			# 	file.write(outputStr)
			# 	file.close()
			# 	file2 = open('chain.out', 'a')
			# 	outputStr2 = str(streakCount) + " "
			# 	file2.write(outputStr2)
			# 	file2.close()
			# 	streakCount = 0

main()


