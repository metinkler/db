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


		playerString = ""
		for item in players:
			playerString += str(item) + " "
			
		nameString = ""
		for item in name:
			nameString += str(item) + " "

		quantityString = ""
		for item in quantity:
			quantityString += str(item) + " "

		designString = ""
		for item in design:
			designString += item + " "


		gameInfo = [nameString, playerString, designString, quantityString, link]	
		allGames.append(gameInfo)
		#print(gameInfo)

	return allGames

def getDescription(url):
	# Going to open up the new webpage here, and get the description for the game
	difficulty = 0
	desc = ""
	print url
	page = getPage(url)

	tags = page.xpath('//div[@class="mainContent clearfix"]')
	# tags now inclue basically everything in the main content
	for element in tags:
		#desc += element.text

		if (element.attrib.get('class') != "tlcontents top3"):
			for text in element.iterdescendants():
				if (text.attrib.get('class') == "tlcontents top3"):
					print "AGHHHHHH"
			
				else:
					if (text.text != None):
						print text.text
					if (text.tail != None):
						print text.tail
	
		desc += "\n"
		
	
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

	print(desc)
	print(difficulty)
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
	conn = psycopg2.connect("dbname=db.cs.wm.edu user=metink")
	cur = conn.cursor()

	difficulty = getDifficulty(game[4])

	# do we need a loop here? An entirely new entry if you're changing like jst the numCards value? 
	curr.execute("INSERT INTO card(name, numCards, suits) VALUES (%s, %s, %s)", (game[0],game[3],game[2]))
	curr.execute("INSERT INTO game(name, numPlayers, length, price, rules, complexity, description) VALUES (%s \
%s %s %s %s %s)", (game[0], game[1], NULL, NULL, difficulty[0], difficulty[1], NULL))

def insertDominoGame(game):
	conn = psycopg2.connect("dbname=db.cs.wm.edu user=metink")
	cur = conn.cursor()
	
	difficulty = getDifficulty(game[4])

	curr.execute("INSERT INTO domino(Name, NumDom, AddMaterials) VALUES (%s, %s, %s)", (game[0], game[3], game[2]))
	curr.execute("INSERT INTO game(name, numPlayers, length, price, rules, complexity, descrition) VALUES (%s \
%s %s %s %s %s)", (game[0], game[1], NULL, NULL, difficulty[0], difficulty[1], NULL))


if __name__ == "__main__":
	print(sys.argv[1])
	page = getPage(sys.argv[1])
	listOfGames = parseHTML(page)
	getDescription("https://www.pagat.com"+listOfGames[2][4])
	#buildTables(listOfGames)
