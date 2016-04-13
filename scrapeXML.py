import xmltodict as xmltd


gameDict = {}

def parseXML(xml):
	
	# actual path to file
	fd = open(xml)
	gameDict = xmltodict.parse(fd.read())

	return gameDict

if __name__ == "__main__":

	parseXML(sys.argv[1])

	print(gameDict)
