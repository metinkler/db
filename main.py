# Main.py
# Main python script to prompt user for input and query the database

import sys
import psycopg2

if __name__ == "__main__":
	

	print("Welcome to our database!")
	
	status = ""		
	
	conn = psycopg.connect("dbname=ncowen_gamesdb user=ncowen password=1023714")
	cur = conn.cursor()
	
	while status != "q":

		gameType = raw_input("What type of game do you want to play? \n [ Board | Dice | Card | Domino | RPG ] \n" )

		numPlayers = int(raw_input("How many players do you have? "))

				

		if gameType == "Board":
			
			age = raw_input("How old are you? ")
			pieces = raw_input("What pieces do you have?\n [ ] \n")

			# query here with the info we've gotten
			cur.execute("SELECT name FROM board WHERE age=%, pieces = %, numPlayers = %;" % (agea
			
			print("Returning %s game with %d people playing, for age %s with the following pieces available: %s" % (gameType, numPlayers, age, pieces))
		
		if gameType == "Dice":
			
			dice = raw_input("What type of dice do you have? ")
			numDice = int(raw_input("How many dice do you have? "))
	
			#query here
		
			print("Returning %s game with %d people playing, with %d %s." % (gameType, numPlayers, numDice, dice))

		if gameType == "Card":
			
			suits = raw_input("What type of cards do you have? ")
			numCards = int(raw_input("How many cards do you have? "))

			# query here

			print("Returning %s game with %d people playing, with %d %s." % (gameType, numPlayers, numCards, suits))

		if gameType == "Domino":

			mats = raw_input("What kind of dominos do you have? \n [ Western Dominoes | Chinese Dominoes ] \n")
			numDom = int(raw_input("How many dominos do you have? "))

			#query here

			print("Returning %s game with %d people playing, and %d %s." % (gameType, numPlayers, numDom, mats))


		if gameType == "RPG":

			mats = raw_input("What lore materials do you have? ")

			# query here

			print("Returning %s game with %d people playing and the following lore materials available: %s" % (gameType, numPlayers, mats))


		status = raw_input("Enter q to quit, or press Enter to search again. \n")
