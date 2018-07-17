def main():

	# blockLength = []
	# blockLength.append(150)
	# blockLength.append(435)
	# blockLength.append(151)
	#blockLength.append(436)


	# blockLength1 = 150
	# blockLength2 = 467
	# blockLength3 = 150
	# blockLength4 = 436

	total_len = 0
	chainLenList = []

	with open('block.dat', 'r') as f:
		for line in f:
			for w in line.split():
				total_len += 1

	file = open('length_meta.q', 'r')
	data = file.readline()
	file.close()
	data += " " + str(total_len)
	file = open('length_meta.q', 'w')
	file.write(data)
	file.close()






				# 	if pos == 2 and counter == length:
				# 		filename = "block" + str(pos) + ".o2"							
				# 		file = open(filename, "a")
				# 		for i in range(0, length):
				# 			file.write(currList[i] + " ")
				# 		file.close()
				# 		pos += 1
				# else:
				# 	print "gonna print to file"
				# 	filename = "block" + str(pos) + ".o2"
					
				# 	file = open(filename, "a")
				# 	for i in range(0, length):
				# 		file.write(currList[i] + " ")
				# 	file.close()
				# 	pos += 1
				# 	if pos < 3:
				# 		length = blockLength[pos]
				# 		print "length is now " + str(length)
				# 	counter = 0
				# 	currList = []

				# 	currList.append(w)
				# 	counter += 1


	file = open("chain.dat", "r")
	streakLenList = file.read().split()
	file.close()

	i = 0
	with open('block.dat','r') as f:
		for line in f:
			for w in line.split():
				currChainLength = int(w)
				value = streakLenList[i]
				f2 = open('streakValues.dat','a')
				f2.write(value + " ")
				f2.close()
				i += currChainLength



		# 	filename = "block" + str(i) + ".o2"
		# strValFilename = "streakValues" + str(i) + ".o2"
		# with open(filename, 'r') as f:
		# 	for line in f:
		# 		for w in line.split():
		# 			currChainLength = int(w)				
		# 			value = streakLenList[pos]
		# 			f2 = open(strValFilename,"a")
		# 			f2.write(value + " ")
		# 			f2.close()
		# 			pos += currChainLength

		#f2 = open("streakValues.o2", "a")
		#f2.write("\n\n")
		#f2.close()





			
main()

