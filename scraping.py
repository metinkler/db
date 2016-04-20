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
# [ [Title of game], [Number of Players - can be min, optimal, most], [Type of game], [Number of cards/dominoes/etc. necessary], Link to webpage describing it]

# Gets the HTML from the page
def getPage(url):
	page = urllib2.Request(url)
	tree = lh.parse(urllib2.urlopen(page))
	#tree = html.fromstring(page.info())
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

		for item in design:
			designString += item + " "

		# cleaning strings
		nameString = nameString[:-1]
		reference = reference[:-1]
		playerString = playerString[:-1]
		designString = designString[:-1]
		quantityString = quantityString[:-1]
		link = link[:-1]

		gameInfo = [nameString, reference, playerString, designString, quantityString, link, minPlayers, maxPlayers]	
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
	

#	print(desc)
		
	
	if len(desc) < 1000:
		difficulty = 1

	elif len(desc) < 4000 and len(desc) > 1000 :
		difficulty = 2

	elif len(desc) > 4000 and len(desc) < 9000:
		difficulty = 3

	elif len(desc) > 9000 and len(desc) < 15000:
		difficulty = 4

	elif len(desc) > 1500 and len(desc) < 25000:
		difficulty = 5

	elif len(desc) > 25000:
		difficulty = 6

#	print(desc)
#	print(difficulty)
	descInfo = [desc, difficulty]

	return descInfo


def buildTables(allGames):
	
	
	for item in allGames:
		# determine the type of game the item is (loop b/c it could be multiple types
		for type in item[2]:
			if type in cardTypes:
				# insert into card database
				print(item)
				insertCardGame(item)				

			if type in dominoTypes:
				print(item)
				insertDominoGame(item)

		print

def insertCardGame(game):
	conn = psycopg2.connect("dbname=ncowen_gamesdb user=ncowen password=1023714")
	conn.autocommit = True
	cur = conn.cursor()

	difficulty = getDescription("https://www.pagat.com"+game[5])

#	print ("Name is: %s \n Synopsis is: \n %s \n Complexity is: %s \n, Min_players is: %s \n Max_players is: %s \n, numCards is: %s \n, Suits is: %s \n, Num players is: %s \n" %  (game[0], difficulty[0], difficulty[1], game[6], game[7], game[4], game[3], game[2]))

	try:
		curr.execute("INSERT INTO card (name, synopsis, complexity, min_players, max_players,  numCards, suits, numPlayers) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)" % (game[0], difficulty[0], difficulty[1], game[6], game[7],  game[4], game[3], game[2]))
	except:
		try:
			curr.execute("UPDATE card SET synopsis = %s, complexity = %s, min_players = %s, max_players = %s, numCards = %s, suits = %s, numPlayers = %s;" % (difficulty[0], difficulty[1], game[6], game[7], game[4], game[3], game[2]))
		except:
			pass


def insertDominoGame(game):
	conn = psycopg2.connect("dbname=db.cs.wm.edu user=metink")
	cur = conn.cursor()
	
	difficulty = getDescription(game[4])

#	curr.execute("INSERT INTO domino(Name, NumDom, AddMaterials) VALUES (%s, %s, %s)", (game[0], game[3], game[2]))
#	curr.execute("INSERT INTO game(name, numPlayers, length, price, rules, complexity, descrition) VALUES (%s %s %s %s %s %s)", (game[0], game[1], NULL, NULL, difficulty[0], difficulty[1], NULL))


if __name__ == "__main__":
	print(sys.argv[1])
	page = getPage(sys.argv[1])
	listOfGames = parseHTML(page)
	#getDescription("https://www.pagat.com"+listOfGames[2][5])
	insertCardGame(listOfGames[0])
	#buildTables(listOfGames)
