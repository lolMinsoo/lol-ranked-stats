import requests
import json
import csv
from datetime import datetime

API_KEY = ''
current_date = datetime.today().strftime('%Y-%m-%d')


def get_ranked_data(apikey, region):
	# Open File
	filename = current_date + "_{}_DATA.csv".format(region)
	file = open(filename, "w+", encoding='utf-8')
	file.close()
	
	diamond_data(apikey, region)
	master_data(apikey, region)
	grandmaster_data(apikey, region)
	challenger_data(apikey, region)
	
def master_data(apikey, region):
	URL = 'https://{region}.api.riotgames.com/lol/league/v4/masterleagues/by-queue/RANKED_SOLO_5x5?api_key={key}'
	
	get_data = requests.get(URL.format(region=region, key=apikey))
	json_data = get_data.json()
	
	filename = current_date + "_{}_DATA.csv".format(region)
	file = open(filename, "a+", encoding='utf-8')
	
	for i in range(len(json_data['entries'])):
		file.write(json_data['entries'][i]['summonerName'] + ', ' + json_data['entries'][i]['summonerId']
		+ ', MASTER I, ' + str(json_data['entries'][i]['leaguePoints']) + '\n')
	file.close()
		
def challenger_data(apikey, region):
	URL = 'https://{region}.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5?api_key={key}'
	
	get_data = requests.get(URL.format(region=region, key=apikey))
	json_data = get_data.json()
	
	filename = current_date + "_{}_DATA.csv".format(region)
	file = open(filename, "a+", encoding='utf-8')
	
	for i in range(len(json_data['entries'])):
		file.write(json_data['entries'][i]['summonerName'] + ', ' + json_data['entries'][i]['summonerId']
		+ ', CHALLENGER I, ' + str(json_data['entries'][i]['leaguePoints']) + '\n')
	file.close()
		
def grandmaster_data(apikey, region):
	URL = 'https://{region}.api.riotgames.com/lol/league/v4/grandmasterleagues/by-queue/RANKED_SOLO_5x5?api_key={key}'
	
	get_data = requests.get(URL.format(region=region, key=apikey))
	json_data = get_data.json()

	filename = current_date + "_{}_DATA.csv".format(region)
	file = open(filename, "a+", encoding='utf-8')
	
	for i in range(len(json_data['entries'])):
		file.write(json_data['entries'][i]['summonerName'] + ', ' + json_data['entries'][i]['summonerId']
		+ ', GRANDMASTER I, ' + str(json_data['entries'][i]['leaguePoints']) + '\n')
	file.close()

def diamond_data(apikey, region):
	URL = 'https://{region}.api.riotgames.com/lol/league/v4/entries/RANKED_SOLO_5x5/DIAMOND/I?api_key={key}'
	
	get_data = requests.get(URL.format(region=region, key=apikey))
	json_data = get_data.json()

	filename = current_date + "_{}_DATA.csv".format(region)
	file = open(filename, "a+", encoding='utf-8')
	
	for i in range(len(json_data)):
		file.write(json_data[i]['summonerName'] + ', ' + json_data[i]['summonerId']
		+ ', DIAMOND I, ' + str(json_data[i]['leaguePoints']) + '\n')
	file.close()
		
get_ranked_data(API_KEY, "NA1")