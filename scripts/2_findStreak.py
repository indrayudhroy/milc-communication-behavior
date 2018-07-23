def main():

	INSTR_TYPE_WORD_POS = 0

	SENDER_WORD_POS = 5
	RECVER_WORD_POS = 6

	with open('finalMeta0.m', 'r') as f:
		#streakRunningFlag = 0
		streakCount = 0
		previousName = ""

		# name: name of MPI operation

		# locate the first wait afer a streak of recvs/sends

		for line in f:
			words = line.split()
			name = words[INSTR_TYPE_WORD_POS]

			if name == "MPI_Isend" or name == "MPI_Irecv":
				streakCount += 1
				previousName = name

			elif name == "MPI_Wait" and (previousName == "MPI_Isend" or previousName == "MPI_Irecv"): 	
				previousName = name


				sender = words[SENDER_WORD_POS]
				recver = words[RECVER_WORD_POS]

				endingOpCount = int(words[2]) - 1

				# endingOpCount: instruction no. that ended the previous group of send/recv operations

				# Pattern of program: fixed no. of sends and receives followed by equal no. of  waits. This is a streak (chain.dat).
				# Collectives occur at predefined positions. The send/recv pattern repeats in a specific way. This is a chain.
				# Accumulating the send/recv streaks separated by collectives into block.dat. 
				# Collectives occurrences are stored as metadata since they're not part of the pattern.

				file2 = open('chain.dat', 'a')
				outputStr2 = str(streakCount) + " "
				file2.write(outputStr2)
				file2.close()
				streakCount = 0

main()


