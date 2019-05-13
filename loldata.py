# thanks to josh for this one


import os
import sys
import csv
import json
import time
import requests

try:
    available_matches = sorted(
        os.listdir('match_cache'),
        key=lambda it: int(it.split('_', 1)[0]))
    assert len(available_matches)
except:
    print("No matches in the match_cache directory. Try adding the '-d' switch?")
    sys.exit(1)

print('Processing...')

players = {}

for file_name in available_matches:
    with open('match_cache/{}'.format(file_name)) as cached_match_file:
        match_data = json.load(cached_match_file)

    # Collect holding data
    team_kills, team_damage = [0, 0], [0, 0]
    holding_data = {}
    print(file_name)
    for index, participant_data in enumerate(match_data['participants']):
        full_name = match_data['participantIdentities'][index]['player']['summonerName']
        name_split = full_name.split(' ', 1)
        if len(name_split) == 1:  # No team name
            name = name_split[0]
        else:
            name = name_split[1].replace(' ', '')
        team_index = int(participant_data['teamId'] / 100 - 1)
        stats = participant_data['stats']
        data = {
            'team': team_index,
            'kills': stats['kills'],
            'deaths': stats['deaths'],
            'assists': stats['assists'],
            'damage': stats['totalDamageDealtToChampions'],
            'cs': (stats['totalMinionsKilled'] + stats['neutralMinionsKilled']) / (match_data['gameDuration'] / 60)
        }
        holding_data[name] = data
        team_kills[team_index] += data['kills']
        team_damage[team_index] += data['damage']

    for name, data in holding_data.items():

        # Add name to the players dictionary if they aren't in it
        if name not in players:
            players[name] = {
                'kills': 0,
                'deaths': 0,
                'assists': 0,
                'kp_data': [],
                'dp_data': [],
                'cs_data': [],
                'games': 0
            }

        # Add data
        for key in ['kills', 'deaths', 'assists']:
            players[name][key] += data[key]
        players[name]['kp_data'].append(data['kills'] / (team_kills[data['team']] or 1))
        players[name]['dp_data'].append(data['damage'] / (team_damage[data['team']] or 1))
        players[name]['cs_data'].append(data['cs'])
        players[name]['games'] += 1

# Write data
average = lambda d: sum(d) / len(d)
with open('output2.csv', 'w') as output_file:

    # Write headers
    writer = csv.writer(output_file)
    writer.writerow(['Player', 'totalKills', 'totalDeaths', 'totalAssists', 'KDA', 'avgKP', 'avgDP', 'avgCS', 'totalGames'])

    for name, data in sorted(players.items()):
        writer.writerow([
            name,
            data['kills'],
            data['deaths'],
            data['assists'],
            '{:.2f}'.format((data['kills'] + data['assists']) / (data['deaths'] or 1)),
            '{:.2f}%'.format(average(data['kp_data'])),
            '{:.2f}%'.format(average(data['dp_data'])),
            '{:.2f}'.format(average(data['cs_data'])),
            data['games']
        ])