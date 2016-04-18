# Main.py
# Main python script to prompt user for input and query the database

import sys
import psycopg2

if __name__ == "__main__":
	

	print("Welcome to our database!")
	
	status = ""		
	
	conn = psycopg2.connect("dbname=ncowen_gamesdb user=ncowen password=1023714")
	cur = conn.cursor()


	while status != "q":

		gameType = raw_input("What type of game do you want to play? \n [ Board |  Card | Domino ] \n" )

		numPlayers = raw_input("How many players do you have? ")

				

		if gameType == "Board":
			
			minAge = int(raw_input("What is the minimum age in your group? "))

			# query here with the info we've gotten
			cur.execute("SELECT name FROM board  WHERE min_age <= %s AND %s BETWEEN min_players AND max_players;" % (minAge, int(numPlayers)))  
			answer = cur.fetchall()
			print(answer)
			print

			desc = raw_input("Select a game for further description , or press q to quit query: ")
			print

			while (desc != "q"):
				cur.execute("SELECT synopsis FROM board WHERE name = '%s' AND min_age <= %s AND %s BETWEEN min_players AND max_players;" % (desc, minAge, int(numPlayers)))
				answer = cur.fetchall()
				print(answer[0][0])

				desc = raw_input("Select a game for further description, or press q to quit query: ")
				print

						
			
		#	print("Returning %s game with %d people playing, for age %s with the following pieces available: %s" % (gameType, numPlayers, age, pieces))
		

		if gameType == "Card":
			
			suits = raw_input("What type of cards do you have? ")
			numCards = raw_input("How many cards do you have? ")

			# query here

			cur.execute("SELECT name FROM card WHERE numCards LIKE %s AND suits = %s AND numPlayers LIKE %s;" % ('%'+numCards+'%', suits, '%'+numPlayers+'%'))		

#			print("Returning %s game with %d people playing, with %d %s." % (gameType, numPlayers, numCards, suits))

		if gameType == "Domino":

			mats = raw_input("What kind of dominos do you have? \n [ Western Dominoes | Chinese Dominoes ] \n")
			numDom = raw_input("How many dominos do you have? ")

			#query here

			cur.execute("SELECT name FROM domino WHERE numDom LIKE %s AND addMaterials = %s AND  num_players LIKE %s;" % ('%'+numDom+'%', mats, '%'+numPlayers+'%'))



		status = raw_input("Enter q to quit, or press Enter to search again. \n")
