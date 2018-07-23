# Format of of partners' metadata:
	# Each line: Send/recv rank pair is listed; length of line is specified by streak length.

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



main()


