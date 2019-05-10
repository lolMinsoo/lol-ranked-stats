import requests
import json
import csv
from datetime import datetime

API_KEY = ''
current_date = datetime.today().strftime('%Y-%m-%d')




def main():
	print('------------------------------')
	print('1. Get ranked data')
	
	# TODO: Need to implement checks
	if input() == '1':
		region = input('Region: ')
		print(region)
		get_ranked_data(API_KEY, region)

def get_ranked_data(apikey, region):
	
	TOTAL_PLAYERS = 0
	filename = current_date + "_{}_DATA.csv".format(region)
	file = open(filename, "w+", encoding='utf-8')
	file.close()
	
	TOTAL_PLAYERS = diamond_data(apikey, region, TOTAL_PLAYERS)
	TOTAL_PLAYERS = master_data(apikey, region, TOTAL_PLAYERS)
	TOTAL_PLAYERS = grandmaster_data(apikey, region, TOTAL_PLAYERS)
	TOTAL_PLAYERS = challenger_data(apikey, region, TOTAL_PLAYERS)
	
	print('{} players analyzed'.format(TOTAL_PLAYERS))
	
def master_data(apikey, region, TOTAL_PLAYERS):
	URL = 'https://{region}.api.riotgames.com/lol/league/v4/masterleagues/by-queue/RANKED_SOLO_5x5?api_key={key}'
	
	get_data = requests.get(URL.format(region=region, key=apikey))
	json_data = get_data.json()
	
	print('Gathering {} Master players data.'.format(str(len(json_data['entries']))))

	
	filename = current_date + "_{}_DATA.csv".format(region)
	file = open(filename, "a+", encoding='utf-8')
	
	for i in range(len(json_data['entries'])):
		file.write(json_data['entries'][i]['summonerName'] + ', ' + json_data['entries'][i]['summonerId']
		+ ', MASTER I, ' + str(json_data['entries'][i]['leaguePoints']) + '\n')
	file.close()
	
	return TOTAL_PLAYERS
		
def challenger_data(apikey, region, TOTAL_PLAYERS):
	URL = 'https://{region}.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5?api_key={key}'
	
	get_data = requests.get(URL.format(region=region, key=apikey))
	json_data = get_data.json()
	
	print('Gathering {} Challenger players data.'.format(str(len(json_data['entries']))))
	TOTAL_PLAYERS += len(json_data['entries'])
	
	filename = current_date + "_{}_DATA.csv".format(region)
	file = open(filename, "a+", encoding='utf-8')
	
	for i in range(len(json_data['entries'])):
		file.write(json_data['entries'][i]['summonerName'] + ', ' + json_data['entries'][i]['summonerId']
		+ ', CHALLENGER I, ' + str(json_data['entries'][i]['leaguePoints']) + '\n')
	file.close()
	return TOTAL_PLAYERS
		
def grandmaster_data(apikey, region, TOTAL_PLAYERS):
	URL = 'https://{region}.api.riotgames.com/lol/league/v4/grandmasterleagues/by-queue/RANKED_SOLO_5x5?api_key={key}'
	
	get_data = requests.get(URL.format(region=region, key=apikey))
	json_data = get_data.json()

	print('Gathering {} Grandmaster players data.'.format(str(len(json_data['entries']))))
	TOTAL_PLAYERS += len(json_data['entries'])
	
	filename = current_date + "_{}_DATA.csv".format(region)
	file = open(filename, "a+", encoding='utf-8')
	
	for i in range(len(json_data['entries'])):
		file.write(json_data['entries'][i]['summonerName'] + ', ' + json_data['entries'][i]['summonerId']
		+ ', GRANDMASTER I, ' + str(json_data['entries'][i]['leaguePoints']) + '\n')
	file.close()
	return TOTAL_PLAYERS

def diamond_data(apikey, region, TOTAL_PLAYERS):
	URL = 'https://{region}.api.riotgames.com/lol/league/v4/entries/RANKED_SOLO_5x5/DIAMOND/I?page={page}&api_key={key}'
	
	filename = current_date + "_{}_DATA.csv".format(region)
	file = open(filename, "a+", encoding='utf-8')
	
	for page in range(1, 50):
	
		json_data = requests.get(URL.format(region=region, page=page, key=apikey)).json()
		TOTAL_PLAYERS += len(json_data)
		
		if page == 1:
			print('Gathering first {} Diamond I players data.'.format(str(len(json_data))))
		elif len(json_data) > 1:
			print('Gathering next {} Diamond I players data.'.format(str(len(json_data))))
		
		if len(json_data) < 1:
			break
		for i in range(len(json_data)):
			file.write(json_data[i]['summonerName'] + ', ' + json_data[i]['summonerId'] 
			+ ', DIAMOND I, ' + str(json_data[i]['leaguePoints']) + '\n')
	file.close()
	return TOTAL_PLAYERS	
	

main()