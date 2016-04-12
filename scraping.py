#!/usr/bin/python

from lxml import html
import requests
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
	page = requests.get(url)
	tree = html.fromstring(page.content)
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
						if subitem.attrib.get('href'):
							link = subitem.attrib.get('href')
						name.append(subitem.text.strip())
					
			# grab game's number of recommended players
			elif item.attrib.get('class') == "col2":
				for subitem in item.iterdescendants():
					if subitem.text != None:
						# converts ASCII to regular string
						numPlayers = subitem.text.encode('ascii','replace')
						numPlayers = numPlayers.replace('?', '-')
						players.append(numPlayers)
			
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
	
		gameInfo = [name, players, design, quantity, link]	
		allGames.append(gameInfo)

	return allGames

#def getDescription(url):
	# Going to open up the new webpage here, and get the description for the game
	desc = ""
	page = getPage(url)
	return desc


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
	curr.execute("INSERT INTO Card(Name, suits, numCards) VALUES (%s, %s, %s)", (game[0],game[2],game[3]))


def insertDominoGame(game):
	conn = psycopg2.connect("dbname=db.cs.wm.edu user=metink")

	cur = conn.cursor()
	curr.execute("INSERT INTO Domino(Name, NumDom, AddMaterials) VALUES (%s, %s, %s)", (game[0], game[3], game[2]))



if __name__ == "__main__":
	print(sys.argv[1])
	page = getPage(sys.argv[1])
	listOfGames = parseHTML(page)
	#buildTables(listOfGames)
