import re

def parse_episode(record):
    # Parse the season and episode numbers
    season, episode = re.compile('S(\d+)E(\d+)').match(record['episode']).group(1, 2)
    record['season_episode_text'] = record['episode']
    record['season'] = int(season)
    record['episode'] = int(episode)
    record['title'] = record['title'].title()
    return record