import requests
import json
import csv
import os
import time
from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import datetime

PRODUCTION_KEY = False
API_KEY = ''
current_date = datetime.today().strftime('%Y-%m-%d')
valid_regions = ['BR1', 'EUN1', 'EUW1', 'JP', 'KR', 'LA1', 'LA2', 'NA1', 'OC1', 'RU']



def main():
	print('------------------------------')
	print('1. Get ranked data')
	print('2. Get tournament data')
	
	if not os.path.isdir('match_cache'):
		os.mkdir('match_cache')
	if not os.path.isdir('ranked_data'):
		os.mkdir('ranked_data')
	
	user_response = input()
	
	# TODO: Need to implement checks
	if user_response == '1':
		_print_regions()
		region = input('Region: ')
		if region not in valid_regions:
			if region in 'ALL':
				for it in valid_regions:
					print('Currently gathering data for: ' + it)
					get_ranked_data(API_KEY, it)
					if not PRODUCTION_KEY:
						time.sleep(2)  # rate limits
				
			print(region + ' is not a valid region.')
		if region in valid_regions:
			get_ranked_data(API_KEY, region)
	elif user_response == '2':
		url = input('Enter valid Leaguepedia Tournament Match History Url: ')
		tournament_data(url)
	else:
		print('Invalid input')
		
	

def get_ranked_data(apikey, region):
	
	TOTAL_PLAYERS = 0
	filename = 'ranked_data/' + current_date + "_{}_DATA.csv".format(region)
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

	
	filename = 'ranked_data/' + current_date + "_{}_DATA.csv".format(region)
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
	
	filename = 'ranked_data/' + current_date + "_{}_DATA.csv".format(region)
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
	
	filename = 'ranked_data/' + current_date + "_{}_DATA.csv".format(region)
	file = open(filename, "a+", encoding='utf-8')
	
	for i in range(len(json_data['entries'])):
		file.write(json_data['entries'][i]['summonerName'] + ', ' + json_data['entries'][i]['summonerId']
		+ ', GRANDMASTER I, ' + str(json_data['entries'][i]['leaguePoints']) + '\n')
	file.close()
	return TOTAL_PLAYERS

def diamond_data(apikey, region, TOTAL_PLAYERS):
	URL = 'https://{region}.api.riotgames.com/lol/league/v4/entries/RANKED_SOLO_5x5/DIAMOND/I?page={page}&api_key={key}'
	
	filename = 'ranked_data/' + current_date + "_{}_DATA.csv".format(region)
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
	
def tournament_data(url):
	mh_links = []
	realm = []
	match_id = []
	gameHash = []
	names_data = []
	names = []
	names_list = []
	
	title = input('Tournament/Event Title: ')
	
	data = BeautifulSoup(urlopen(url), 'lxml')
	collect = data.find_all('a')
	
	for it in collect:
		if 'MH' in it:
			mh_links.append(it)
			
	for i, mh_link_data in enumerate(mh_links):
	
		#break links apart
		tail, scrape = str(mh_links[i]).split('href=\"')
		scrape, tail = scrape.split('\" rel=\"n')
		
		print("Currently extracting data: " + str(i+1) + "/" + str(len(mh_links)) +" Done")
		
		#collect realm data and append to list
		realm_data, tail = scrape.split('/')[5:]
		realm.append(realm_data)
		print(realm_data)
		
		#collect match_id and gameHash 
		match_id_data, gameHash_data = tail.split('?gameHash=')
		
		if '&amp' in gameHash_data:
			gameHash_data, tail = gameHash_data.split('&amp')
		
		match_id.append(match_id_data)
		gameHash.append(gameHash_data) 
		print(match_id_data)
		print(gameHash_data)
		
	tdlinks = data.find_all('td')
	
	
	# For some reason Leaguepedia handles "names" differently so these are the two that I've seen.
	
	for it in tdlinks:
		if('_toggle players' in str(it)):
			names_data.append(str(it))
			
	print(names_data)
	
	if('Tooltip:' in names_data[0]):
		for i, it in enumerate(names_data):
			
			names_track = names_data[i].split("Tooltip:")[1:]
		
			for j in range(len(names_track)):
		
				names_list.append(names_track[j].split('\"')[0])

		
		
			names.append(names_list)
			names_list = []
	
		
	for i, it in enumerate(names_data):
			
		names_track = names_data[i].split("title=\"")[1:]
		
		for j in range(len(names_track)):
		
			names_list.append(names_track[j].split('\"')[0])
			print(names_list)
		# print(names_data[i].split('\"')[0])
		
		
		names.append(names_list)
		names_list = []
	title_file = open(title + '.txt', 'w+', encoding='utf-8')
	for i, it in enumerate(match_id):
		print('Match ID: {} \n RED:  {} \n BLUE: {}'.format(match_id[i], names[i*2], names[i*2+1]))
		print('ACSURL = https://acs.leagueoflegends.com/v1/stats/game/{}/{}/timeline?gameHash={}'.format(realm[i], match_id[i], gameHash[i]))
		print('MHURL  = https://matchhistory.na.leagueoflegends.com/en/#match-details/{}/{}?gameHash={}\n'.format(realm[i], match_id[i], gameHash[i]))
		title_file.write('Match ID: {} \n RED:  {} \n BLUE: {}\n'.format(match_id[i], names[i*2], names[i*2+1]))
		title_file.write('ACSURL = https://acs.leagueoflegends.com/v1/stats/game/{}/{}/timeline?gameHash={}\n'.format(realm[i], match_id[i], gameHash[i]))
		title_file.write('MHURL  = https://matchhistory.na.leagueoflegends.com/en/#match-details/{}/{}?gameHash={}\n'.format(realm[i], match_id[i], gameHash[i]))
	title_file.close()
		
	
	extract_tournament_data(realm, match_id, gameHash)
	
def extract_tournament_data(realm, match_id, gameHash):
	
	for i, it in enumerate(match_id):
		json_data = requests.get('https://acs.leagueoflegends.com/v1/stats/game/{}/{}/timeline?gameHash={}'.format(realm[i], match_id[i], gameHash[i])).json()
		file_name = 'match_cache/{}_{}_{}_{}.json'.format(i+1, realm[i], match_id[i], gameHash[i])
		with open(file_name, "w+", encoding='utf-8') as output_file:
			json.dump(json_data, output_file)
		print(file_name.split('/')[1])

	
	
	
def _print_regions():
	print(	'\n BR1  - Brazil \n',
			'EUN1 - Europe Nordic East \n',
			'EUW1 - Europe West \n',
			'JP   - Japan \n',
			'KR   - Korea \n',
			'LA1  - Latin America North \n',
			'LA2  - Latin America South \n',
			'NA1  - North America \n',
			'OC1  - Oceanic \n',
			'TR1  - Tournament Realm \n',
			'PBE1 - Public Beta Environment \n',
			'RU   - Russia \n')
	

main()