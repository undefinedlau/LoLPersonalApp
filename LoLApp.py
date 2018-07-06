from riotwatcher import RiotWatcher 
from requests import HTTPError
from urllib.request import urlopen
import datetime
import json

# This is to turn off certificate verification to solve urlopen problem
import os, ssl

# Global variables
APIKEY = "RGAPI-1951f5fb-d915-4b9a-80cf-a6d71310d75b"
watcher = RiotWatcher(APIKEY)

# A python dictionary is implemented as a hash table
champ_dict = {} # each champion will be associated with a champion key



'''
getCurrentPatch - helper function for makeChampionList. Updates the current patch in url

Return: the latest patch 
'''
def getCurrentPatch():
	url = json.loads(urlopen("https://ddragon.leagueoflegends.com/api/versions.json").read())
	return url[0]


'''
makeChampionList - populates a champion array for conversion from id to actual champion
	Adapted from https://stackoverflow.com/questions/21670239/extract-data-from-json-api-using-python
'''
def makeChampionList():
	url = urlopen("http://ddragon.leagueoflegends.com/cdn/" + getCurrentPatch() + "/data/en_US/champion.json").read()
	result = json.loads(url)

	# champ_dict is a global variable declared at the very top
	for champ in result["data"]:
		champ_dict[int(result["data"][champ]["key"])] = champ


'''
getChampion - gets a champion from the champion dictionary

@champID - the id of the champion

Return: the name of the champion associated with the id 
'''
def getChampion(champID):
	# There is no need to return -1 on wrong input because we are reading off of Riot's JSON file
	# which we assume to have no errors
	return champ_dict[int(champID)]


'''
reformatDate - turns epoch milliseconds into a more readable time 

@region - region of the summoner 
@summoner_name - name of the player

Return: a nicely formatted and readable time
'''
def reformatDate(startingValue):
	# Adapted from https://developer.riotgames.com/api-methods/#summoner-v3/GET_getBySummonerName
	# Revision date, according to the League of Legends API description, is the following:
	# Date summoner was last modified specified as epoch milliseconds
	# The following events will update this timestamp: 
	# profile icon change, playing the tutorial or advanced tutorial, finishing a game, summoner name change

	formattedTime = datetime.datetime.fromtimestamp(startingValue).strftime('%Y-%m-%d %H:%M:%S')
	return formattedTime


'''
 displaySummonerStatistics - prints out basic information of each summoner

 @region - region of the summoner

 @summoner_name - name of the summoner
'''
def displaySummonerStatistics():
	summoner_name = input("Please enter summoner name: ")
	region = input("Please enter region: ")

	try:
		print("\n")
		print("----------")
		print("Displaying Information for Summoner", summoner_name)

		summoner = watcher.summoner.by_name(region, summoner_name)

		print("Summoner Name:", summoner['name'])
		print("Summoner ID:", summoner['id'])
		print("Account ID:", summoner['accountId'])
		print("Summoner Level:", summoner['summonerLevel'])
		print("Last Activity:", reformatDate(summoner['revisionDate']/1000))
	except HTTPError as err:
		print("\n")
		print("Error when displaying summoner statistics")
		print("Summoner or region was not found")
	print("----------")


''' 
getChampionID - gets the champ_id for a champion

@champion - the champion we want id for 

Return: the id of the champion, else -1 
'''	
def getChampionID(champion):
	for champ_id,champ in champ_dict.items():
		if (champion == champ):
			return champ_id
	return -1


'''
displayKDA - displays kills, deaths, and assists for the player

@region - region to search for the player
@match_id - id of the game Played
@account_id - id of the player's account
'''
def displayKDA(region, match_id, account_id):
	participantId = -1

	try:
		participantIdentities = watcher.match.by_id(region, match_id)["participantIdentities"]
		participants = watcher.match.by_id(region, match_id)["participants"]

		# search through participantIdentities to find the one corresponding to the provided account_id (user)
		for i in range(0,len(participantIdentities)):
			if (account_id == participantIdentities[i]["player"]["accountId"]):
				participantId = participantIdentities[i]["participantId"]	

		# search through participants to find the one corresponding to participantId, and print
		for i in range(0,len(participants)):
			if (participants[i]["stats"]["participantId"] == participantId):
				stats = participants[i]["stats"]
				print("Kills:", stats["kills"], "Deaths:", stats["deaths"], "Assists:", stats["assists"])
	except HTTPError as err:
		pass


# displayMatchInfo - displays past 10 games (optional: for a specific champion)
def displayMatchInfo():

	region = input("Please enter region: ")
	acc_id = input("Please enter account id\n (You may find account id by using the first option in the prompt): ")
	specific_champion = input("Would you like to search for a specific champion? (y/n): ")
	

	if (specific_champion == 'n'):

		print("\n")
		print("----------")
		print("Displaying information for last 10 matches: ")
		print("\n")

		try:
			# For neater code and also speeding code up by a few seconds!
			matches_n = watcher.match.matchlist_by_account(region, acc_id)["matches"]

			for i in range(0,10): # handle 10 requests
				print("Platform ID:", matches_n[i]["platformId"])
				print("Game ID:", matches_n[i]["gameId"])
				print("Champion Played:", getChampion(matches_n[i]["champion"]))
				print("Time:", reformatDate(matches_n[i]["timestamp"]/1000))
				displayKDA(region, int(matches_n[i]["gameId"]), int(acc_id))
				print("\n")
		except HTTPError as err:
			print("\n")
			print("Error when displaying match information")
			print("Please recheck to see if you typed in correct region and/or account id")
		print("----------")

	elif (specific_champion == 'y'):
		# Strip all white space to account for how the champion is stored in the dictionary
		champ = input("Please type the champion's name with uppercase for each new word (omitting punctuation): ").replace(" ","")
		champ_id = getChampionID(champ)
		while (champ_id == -1):
			champ = input("Cannot find champion. Please re-enter: ").replace(" ","")
			champ_id = getChampionID(champ)

		try:
			print("\n")
			print("----------")
			print("Displaying information for last 10 matches for", champ)
			print("\n")
			# For neater code and also speeding code up by a few seconds!
			matches_y = watcher.match.matchlist_by_account(region,acc_id, None, None, None, None, None, None, [champ_id])["matches"]
			
			for i in range(0,10):
				print("Platform ID:", matches_y[i]["platformId"])
				print("Game ID:", matches_y[i]["gameId"] )
				print("Champion Played:", getChampion(matches_y[i]["champion"]))
				print("Time:", reformatDate(matches_y[i]["timestamp"]/1000))
				displayKDA(region, int(matches_y[i]["gameId"]), int(acc_id))
				print("\n")
		except HTTPError as err:
			print("\n")
			print("Error when displaying match information")
			print("Please recheck to see if you typed in correct region and/or account id")
		print("----------")

	else:
		print("\nError with response. Please type 'y' or 'n' when asking for specific champion")


'''
displayRegionStatus - displays status for a region
'''
def displayRegionStatus():
	try:
		region = input("Please enter region: ")
		print("----------")
		print("Status for region", region)
		i = 0

		# There are only 4 services: game, store, web, client
		for i in range(0,4):
			services = watcher.lol_status.shard_data(region)["services"]
			print(services[i]["name"], "-", service[i]["status"])
			
			# There could be messages describing the incident if a service is down
			# But we do not want to print them unless they exist
			if (watcher.lol_status.shard_data(region)["services"][i]["incidents"] != []):
				print("Incidents: ", watcher.lol_status.shard_data(region)["services"][i]["incidents"])
			i = i + 1

		print("----------")
	except HTTPError as err:
		print("\n")
		print("Error when displaying region information")
		print("Please recheck to see if you typed in correct region")

'''
displayPrompt - displays the prompt for the user

Return: the user input, else -1
'''
def displayPrompt():
	print("\n")
	print("**********Prompt**********")
	print("1. Show Summoner Statistics")
	print("2. Display Match Information")
	print("3. Get champion id")
	print("4. Display server status")
	print("5. Exit")
	print("**************************\n")

	try:
		user_input = int(input("What would you like to do? "))
	except (TypeError, ValueError):
		print("Invalid input type (please enter an integer)")
		return -1

	return user_input;

'''
checkUserInput - make sure the user_input is within the bounds of the Prompt

@user_input - an integer of the user's choice

Return: -1 if not within bounds, 0 otherwise
'''
def checkUserInput(user_input):
	lower_bound = 1
	upper_bound = 5

	if (user_input < lower_bound or user_input > upper_bound):
		return -1;
	return 0;

'''
controller - a driver function that keeps the entire application running
@user_input - an integer of the user's choice
'''
def controller():

	while 1:
		user_input = -5 # some indicator integer
		user_input = displayPrompt()

		if (user_input == -1):
			continue
		while (checkUserInput(user_input) == -1):
			print("Your choice is out of bounds. Please try again")
			user_input = displayPrompt()
		if (user_input == 1):
			displaySummonerStatistics()
		elif (user_input == 2):
			displayMatchInfo()
		elif (user_input == 3):
			print("\n")
			print("----------")
			champ = input("Please enter a champion with uppercases for each new word: ").replace(" ","")
			
			champ_id = getChampionID(champ)
			while (champ_id == -1):
				print("Cannot find champion. Please try again")
				champ = input("Please enter a champion with uppercases for each new word: ").replace(" ","")
				champ_id = getChampionID(champ)
			print("Champion ID for", champ, "is", champ_id)
			
		elif (user_input == 4):
			displayRegionStatus()
		elif (user_input == 5):
			print("Thank you for using this simple application! Good bye!")
			break


def main():
	# This is to turn off certificate verification to solve urlopen problem
	# http://blog.pengyifan.com/how-to-fix-python-ssl-certificate_verify_failed/
	if (not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None)): 
		ssl._create_default_https_context = ssl._create_unverified_context

	makeChampionList()
	
	print("\n\n\n\n\n")
	print("Welcome! This application will grab useful information for you from Riot's API")
	print("To start, please find your region here: https://developer.riotgames.com/regional-endpoints.html")
	
	controller()


if __name__ == "__main__":
	main()