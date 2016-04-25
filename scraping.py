#!/usr/bin/python

from lxml import html as lh
import urllib2
import sys
import psycopg2


# massive lists containing each game's info (which is another list)
allGames = []

cardTypes = ["French suited cards", "Latin suited cards", "Quartet cards", "German suited cards", "Old Maid cards", "Number cards", "Cuckoo cards", "French suited Tarot", "Italian suited Tarot", "Flower cards", "Shogi cards", "Quartet cards", "Joffre cards", "Swiss suited cards", "Quitli cards", "Lost Heir cards", "Money cards", "Chinese chess cards", "Top Trumps cards", "Whot cards"]
dominoTypes = ["Western dominoes", "Chinese dominoes", "Number tiles", "Money tiles", "Cuckoo pieces"]


# Each game is listed in format:
# [ Title of game, Refers to, Number of Players (string), Type of game, Number of cards/dominoes/etc. necessary (string), Link to webpage describing it, min players, max players]

# Gets the HTML from the page
def getPage(url):
	page = urllib2.Request(url)
	tree = lh.parse(urllib2.urlopen(page))
	return tree


def parseHTML(tree):
	# extract necessary game data from HTML
	
	tags  = tree.xpath('//tr')
	#for each tr element
	for element in tags:
		#for each td within that (i.e., for col1, col2, col3 or col4

		name = []
		players = []
		design = []
		quantity = []
		link = ""

		for item in element.iterchildren():
			#for each item within that column -- so name/numPlayers/typeGame/numCards
			
			# grab game's name
			if item.attrib.get('class') == "col1":
				for subitem in item.iterdescendants():
					if subitem.text != None:
						nameList = subitem.text.encode('ascii', 'replace')
						if subitem.attrib.get('href'):
							link = subitem.attrib.get('href')
							link = link[2:]
						name.append(nameList.strip())
						
					
			# grab game's number of recommended players
			elif item.attrib.get('class') == "col2":
				for subitem in item.iterdescendants():
					if subitem.text != None:
						# converts ASCII to regular string
						numPlayers = subitem.text.encode('ascii','replace')
						numPlayers = numPlayers.replace('?', '-')
						numPlayers = numPlayers.split(',')

						for item in numPlayers:
							# append every number of players within range specified (if specified)
							if "-" in item:
								item = item.strip(', ')
								rangePlayers = item.split('-')
								for x in range(int(rangePlayers[0]),int(rangePlayers[1])+1):
									players.append(x)

							else:
								item = item.strip(' ')
								if item != "":
									item = item.strip('+')
									# currently just ignoring x+ players???
									players.append(int(item))							
			
			# grab type of game
			elif item.attrib.get('class') == "col3":
				for subitem in item.iterdescendants():
					if subitem.text != None:
						design.append(subitem.attrib.get('title'))
			
			# grab number of cards
			elif item.attrib.get('class') == "col4":
				for subitem in item.iterdescendants():
					if subitem.text != None:
						quantity.append(subitem.text.strip())
		
	
		# building strings from given lists`
		playerString = ""
		nameString = ""
		reference = ""
		quantityString = ""
		designString = ""
		foundSee = False


		if len(players) > 0:
			minPlayers = int(players[0])
			maxPlayers = int(players[-1])
		else:
			minPlayers = 0
			maxPlayers = 0


		for item in players:
			playerString += str(item) + " "
			
		for item in name:
			if foundSee == False:
				if item == "see":
					foundSee = True
				else:
					nameString += str(item) + " "
			else:
				reference += item + " " 

		for item in quantity:
			quantityString += str(item) + " "

#		for item in design:
#			designString += item + " "

		# cleaning strings
		nameString = nameString[:-1]
		reference = reference[:-1]
		playerString = playerString[:-1]
		#designString = designString[:-1]
		quantityString = quantityString[:-1]

		gameInfo = [nameString, reference, playerString, design, quantityString, link, minPlayers, maxPlayers]	
		allGames.append(gameInfo)
	#	print(gameInfo)

	allGames.pop(0)
	allGames.pop(0)

	return allGames

def getDescription(url):
	# Going to open up the new webpage here, and get the description for the game
	difficulty = 0
	desc = ""
	print url
	page = getPage(url)
	badClass = False

	tags = page.xpath('//div[@class="mainContent clearfix"]')
	# tags now inclue basically everything in the main content
	for element in tags:
		#desc += element.text
		
		for text in element.iterdescendants():
		
			if text.tag == "h1":
				badClass = True

			elif text.tag == "h2":	
				badClass = False

			else:
				if (badClass == False):
					if (text.text != None and text.text != " InstanceBeginEditable name=\"MainContent\" " and text.text != " InstanceEndEditable " and text.text != " end #mainContent "):
						desc += text.text

					if (text.tail != None):
						desc += text.tail

					if text.tag != "strong" and text.tag != "a":
						desc += "\n"


	return desc


def buildTables(allGames, curr):
	
	
	for item in allGames:
		# determine the type of game the item is (loop b/c it could be multiple types
		
		# check through list for if it should be inserted into card or domino database, then convert it to string b/c right now it's a list

		cardInsert = 0
		dominoInsert = 0
		gameTypeStr = ""
 
		for gameType in item[3]:
			if gameType in cardTypes:
				cardInsert += 1
			elif gameType in dominoTypes:
				dominoInsert += 1

			gameTypeStr += gameType + " "

		# replace list with string so it can match database attribute
		gameTypeStr = gameTypeStr[:-1]
		item[3] = gameTypeStr
		
		# fix empty references to have null value
		if item[1] == "":
		  item[1] = None
		  		
		if cardInsert > 0:
			# insert into card database
			insertCardGame(item, curr)				

		if dominoInsert > 0:
			# insert into domino
			insertDominoGame(item, curr)
			


def insertCardGame(game, curr):
  
	url = "https://www.pagat.com"+game[5]

	desc = getDescription(url)

	cardTuple = (game[0], desc, 0, game[6], game[7], game[4], game[3], game[1], game[2], url)
	updateTuple = (desc, 0, game[6], game[7], game[4], game[3], game[1], game[2], url, game[0])

	try:
		curr.execute("UPDATE card SET url = %s WHERE name =%s;", (url, game[0]))
#(name, synopsis, complexity, min_players, max_players, numCards, suits, refers, num_players, url) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);", cardTuple)
	except:
		pass
		#try: 
	#	    curr.execute("UPDATE card SET synopsis = %s, complexity = %s, min_players = %s, max_players = %s, numCards = %s, suits = %s, refers=%s, num_players = %s, url = %s WHERE name = %s;", updateTuple)
	#	except:
	#		pass


def insertDominoGame(game, curr):

	url = "https://www.pagat.com"+game[5]	

	desc = getDescription(url)
	
	dominoTuple = (game[0], desc, 0, game[6], game[7], game[4], game[3], game[1], game[2], url)
	updateTuple = (desc, 0, game[6], game[7], game[4], game[3], game[1], game[2], url, game[0])

	try:
		curr.execute("UPDATE domino SET url = %s WHERE name=%s;", (url, game[0]))

#(name, synopsis, complexity, min_players, max_players,  numDom, domino_type, refers, num_players, url) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);", dominoTuple)
	except:
		pass
#		try:
#			curr.execute("UPDATE domino SET synopsis = %s, complexity = %s, min_players = %s, max_players = %s, numDom = %s, domino_type = %s, refers = %s, num_players = %s, url = %s WHERE name = %s;", updateTuple)
#		except:
#			pass


if __name__ == "__main__":
	print(sys.argv[1])
	page = getPage(sys.argv[1])
	listOfGames = parseHTML(page)

	conn = psycopg2.connect("dbname=ncowen_gamesdb user=metink password=Marroy22")
	conn.autocommit = True
	curr = conn.cursor()
	
	buildTables(listOfGames, curr)
	
	curr.close()
	conn.close()
