
	# Matching streak lengths with the chain they belong to, and storing streak lengths in streakValues.dat.
	# This is to have a single metadata occurence for streak values.
	# Store total no. of chains -- which specifies the iterative length of the program.

def main():

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

			
main()

