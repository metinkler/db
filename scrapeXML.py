import xmltodict as xmltd


gameDict = {}

def parseXML(xml):
	
	# actual path to file
	fd = open(xml)
	gameDict = xmltodict.parse(fd.read())

	return gameDict


def fillDB(gameDict):
	
	for key in gameDict:
		return


def insertBoardGame(gameDict):
	return

def insertDiceGame(gameDict):
	return

def insertRPGGame(gameDict):
	return


if __name__ == "__main__":

	parseXML(sys.argv[1])

	print(gameDict)
