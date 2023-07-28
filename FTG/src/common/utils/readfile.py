import time

def readFile_ParseLine(path, numThread = 1):
	def __parseLine(string):
		# string = string.strip()
		lines = string.split("\n")
		if not lines:
			return None
		for i in range(len(lines)):
			lines[i] = lines[i].strip()
			lines[i] = lines[i].split(" ")	## regex?
		return lines
	start = time.perf_counter()
	print(f"Reading file: {path}")
	try:
		## type of file: "r","rb"
		with open(path,"r") as file:
			## multithread (?)
			data = file.read()
			print(f"Read file in: {time.perf_counter() - start}")
		file.close()
	except IOError: 
		print("Error: File does not appear to exist.")
		return False
	else:
		lines = __parseLine(data)
		if not lines:
			print(f"Error: File does not contain any readable data.")
			return None
		print(f"Success reading file.")
		return lines
	return None