def main():

	sendrecvCount = 0
	with open('finalMeta0.m', 'r') as f:
		for line in f:
			words = line.split()
			name = words[0]

			if name == "MPI_Isend" or name == "MPI_Irecv":
				sendrecvCount += 1	

	MAX_SENDRECVS = sendrecvCount
	
	sigma = 0
	count = 0

	with open('chain.dat', 'r') as f:
		#count = 0
		streakChainLen = 1
		oldWord = ""		

		for line in f:
			for w in line.split():

				sigma += int(w)
				count += 1

				if count > 1:
					if w == oldWord:
						streakChainLen += 1
						if sigma == MAX_SENDRECVS:
							file = open("block.dat","a")
							file.write(str(streakChainLen) + " ")
							file.close()
					else:
						file = open("block.dat","a")
						file.write(str(streakChainLen) + " ")
						file.close()
						#print "logged. value = "+str(streakChainLen)+", sigma = "+str(sigma)
						streakChainLen = 1

				oldWord = w

	#print "sum of streaks = " + str(sigma)


main()
