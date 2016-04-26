# Models the Bayesian Spam Filter
#	We are taking each word in training data and adding it to 
#	a dictionary with respect to each complexity. Test data
#	text is compared to give the probability that it belongs to
#	a given class.

import glob
import string
import sys
import psycopg2
import csv


def main():

	conn = psycopg2.connect("dbname=ncowen_gamesdb user=ncowen password=1023714")
	conn.autocommit = True
	cur = conn.cursor()

	easyDict = {}
	interDict = {}
	hardDict = {}	# yes, I know

	easyGamesNum = 0
	interGamesNum = 0
	hardGamesNum = 0

	# Create training set

	easyGames = ["Bullshit", "Crazy Eights", "Go Fish", "I Doubt It!", "Old Maid", "Pig", "Slapjack", "War", "52 pick-up"]
	interGames = ["Blackjack 21", "Baccarat", "Canasta", "President", "Spades", "Speed"]
	hardGames = ["Bridge", "Euchre", "Gin Rummy", "Gleek", "Hearts", "Pinochle Double Deck", "Texas Hold''em Poker"]

	for game in easyGames:
		easyDict = createDictionary(easyDict, game, cur)
		easyGamesNum += 1
	for game in interGames:
		interDict = createDictionary(interDict, game, cur)
		interGamesNum += 1
	for game in hardGames:
		hardDict = createDictionary(hardDict, game, cur)
		hardGamesNum += 1
	totalNumGames = easyGamesNum + interGamesNum + hardGamesNum

	priorProbEasy = float(easyGamesNum)/float(totalNumGames)
	priorProbInter = float(interGamesNum)/float(totalNumGames)
	priorProbHard = float(hardGamesNum)/float(totalNumGames)

	# build dictionary of all words
	master = easyDict.copy()
	master.update(interDict)
	master.update(hardDict)
	M = len(master)

	produceRates(easyGames, interGames, hardGames, easyDict, interDict, hardDict, M, priorProbEasy, priorProbInter, priorProbHard, cur)

	cur.close()
	conn.close()


def produceRates(easyGames, interGames, hardGames, easyDict, interDict, hardDict, M, priorProbEasy, priorProbInter, priorProbHard, cur):
	cur.execute("SELECT name FROM card ORDER BY name;")
	allGames = cur.fetchall()

	for game in allGames:
		game = game[0]
		game = game.replace("'", "''") # SQL recognizes '' as '

		sumEasy, sumInter, sumHard = classifyGame(game, easyDict, interDict, hardDict, M, priorProbEasy, priorProbInter, priorProbHard, cur)
		maxSum = max([sumEasy, sumInter, sumHard])
		game = "'" + game + "'"
		if maxSum == sumEasy:
			cur.execute("UPDATE card SET complexity = 'easy' WHERE name = %s;" % (game))
			print("%s: easy" % (game))
		elif maxSum == sumInter:
			cur.execute("UPDATE card SET complexity = 'intermediate' WHERE name = %s;" % (game))
			print("%s: intermediate" % (game))
		else:
			cur.execute("UPDATE card SET complexity = 'hard' WHERE name = %s;" % (game))
			print("%s: hard" % (game))
		

def classifyGame(game, easyDict, interDict, hardDict, M, priorProbEasy, priorProbInter, priorProbHard, cur):
	sumEasy = priorProbEasy * 100
	sumInter = priorProbInter * 100
	sumHard = priorProbHard * 100

	cur.execute("SELECT synopsis FROM card WHERE name = '%s';" % (game))
	synopsis = cur.fetchall()
	synopsis = synopsis[0][0]
	synopsis = synopsis.split('\n')

	for line in synopsis:
		line = line.strip()
		if line != '':
				# strip punctuation
			line = line.translate(str.maketrans({key: None for key in string.punctuation}))
			line = line.split()
			for word in line:
				word = word.lower()
				if word in easyDict:
					probEasy = computeProbability(word, easyDict, M) * 100
					sumEasy *= probEasy
				else:
					probEasy = float(1)/float(M + len(easyDict)) * 100
					sumEasy *= probEasy
				if word in interDict:
					probInter = computeProbability(word, interDict, M) * 100
					sumInter *= probInter
				else:
					probInter = float(1)/float(M + len(interDict)) * 100
					sumInter *= probInter
				if word in hardDict:
					probHard = computeProbability(word, hardDict, M) * 100
					sumHard *= probHard
				else:
					probHard = float(1)/float(M + len(hardDict)) * 100
					sumHard *= probHard

	return (sumEasy, sumInter, sumHard)


''' M is length of master dictionary (easy, intermediate, hard combined) '''
def computeProbability(word, dictionary, M):
	N = len(dictionary)
	numerator = dictionary[word] + 1
	denominator = N + M
	return float(numerator)/float(denominator)


def createDictionary(dictionary, game, cur):
	cur.execute("SELECT synopsis FROM card WHERE name = '%s';" % (game))
	synopsis = cur.fetchall()
	synopsis = synopsis[0][0]
	synopsis = synopsis.split('\n')

	for line in synopsis:
			# strip punctuation
		line = line.strip()
		if line != '':
			line = line.translate(str.maketrans({key: None for key in string.punctuation}))
			line = line.split()
			for word in line:
				word = word.lower()
				if word in dictionary:
					dictionary[word] += 1
				else:
					dictionary[word] = 1
	return dictionary



main()