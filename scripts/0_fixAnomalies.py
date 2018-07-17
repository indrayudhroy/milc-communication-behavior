def main():

	# partners = [1, 2, 4, 8, 12, 48]		# 60 ranks
	# partners = [1, 5, 6, 42, 48, 336, 384, 3456]	# 3840 ranks
	partners = [1, 5, 6, 30, 36, 324, 360, 5760]	# 6120 ranks
	deleteByTag = []

	instrCount = 0

	with open('newMeta0.m','r') as f:
		for line in f:
			instrCount += 1
			words = line.split()
			name = words[0]

			if name == "MPI_Isend":
				partner = int(words[6])
				tag = int(words[7])
				if partner not in partners:
					deleteByTag.append(tag)

	file = open('finalMeta0.m', 'a')

	instrPointer = 0
	with open('newMeta0.m', 'r') as f:
		for line in f:
			words = line.split()
			name = words[0]

			instrPointer += 1

			if name == "MPI_Isend" or name == "MPI_Irecv":
				tag = int(words[7])
				if tag not in deleteByTag:
					file.write(line)
				else:
					err = open('ignoreLines.txt', 'a')
					err.write(str(instrPointer) + " ")
					err.close()
			elif name == "MPI_Wait":
				partner = int(words[6])
				tag = int(words[7])
				deleteFlag = 0
				if tag in deleteByTag:
					deleteFlag = 1
				if partner == 0 and tag == 0:	#hard-coded condition ("0 0")
					deleteFlag = 1
				if deleteFlag == 0:
					file.write(line)
				else:
					err = open('ignoreLines.txt', 'a')
					err.write(str(instrPointer) + " ")
					err.close()
			else:
				file.write(line)
	file.close()

main()


