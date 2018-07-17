def main():

	WARMUPS_START = 3
	WARMUPS_END = 3048

	instrCount = 0

	with open('meta0.m', 'r') as f:
		for line in f:
			instrCount += 1
			if instrCount < WARMUPS_START or instrCount > WARMUPS_END:
				file = open('newMeta0.m', 'a')
				file.write(line)
				file.close()

main()
