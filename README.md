# Description
This is a personal application created by Brian Lau for the game League of 
Legends. Most of us are accustomed to looking up our summoner name on the more
well known LoL statistics websites, like op.gg, but there are times when those 
websites are under maintenance, laggy, over-complicate things by displaying more 
information than necessary, or (simply put) don't display correct information. 
Thus, I wrote this program in order to grab essential information about 
summoners.  

This application has 5 options: show summoner statistics, display match 
information, get champion id, display server status, and exit. 

Note that this application is written in Python 3.   


# High Level Overview of the Options

## Show summoner statistics
Displays summoner name, summoner id, summoner level, account id, and last
activity on the account.   

## Display match information
Displays platform id, game id, champion played, time, and kills/deaths/assists
(kda) for the past 10 games. Optionally, you may provide a champion as a means
of filtering.   

## Get champion id
Returns the champion id as an integer.  

## Display server status
Displays the status of the game, store, website, and client of a given region.
If something is down, then the incident message will also be printed alongside.   

## Exit
Leaves the program with a thank you!

# Function Descriptions

## getCurrentPatch
Loads in the url for the list of patches, converted into json. Returns the 
current patch.  

## makeChampionList  
Populates the global variable champ_dict with champions from the current patch.
Makes use of the getCurrentPatch function.  

## getChampion
Given champion id, returns the champion in the dictionary associated with the
id.  

## reformatDate
Turns epoch milliseconds into a more readable date and time.  

## displaySummonerStatistics
Main function for part1. Displays summoner name, summoner id, account id, 
summoner level, and last activity (also known as revisionDate). All of the main
code is surrounded in a try-except in order to catch HTTPErrors. All of the main
functions are protected by try-except.

## getChampionID
Main function for part2. Given champion as a parameter, iterate through the 
champion dictionary to find the champion and return its id. If not found then 
return -1.  

## displayKDA
Helper function for displayMatchInfo. Prints out the kills, deaths, and assists
for a game of the user. We first locate the user's participantId and then use
the participantId to find the KDA.  

## displayMatchInfo
Main function for part3. This function is divided into two parts: without the
champion filter and with the filter. With the champion filter, the function will
print platform id, game id, champion played, time, and KDA for the past 10 games
with provided champion, else it will only print the past 10 games. Make sure to
follow the given guidelines (in the program) on typing what champion to look for
when choosing the filter option.  

## displayRegionStatus
Main function for part4. Given a region (ex: na1), output the status of the 
store, website, game, and client. If one of the four is down then we also print
out the incident message. The list of all region codes can be found on
this link: https://developer.riotgames.com/regional-endpoints.html"    

## displayPrompt
Prints out the user's prompt.  

## checkUserInput
Verifies if the user input is within the bounds of the prompt. Returns 0 if yes
otherwise -1.  

## controller
The main driver of the program. It has a series of if statements inside a while
loop. When the user exits, we break out of the loop.  

## main
First we disable certificate verification. Then we make the championList. 
Finally we call the controller to handle everything else.  



