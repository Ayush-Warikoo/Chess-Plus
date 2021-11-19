import requests
from chessdotcom import get_player_stats, get_leaderboards
from bs4 import BeautifulSoup
from typing import Final

TITLES: Final = ["WNM", "WCM", "WFM", "WIM", "WGM", "NM", "CM", "FM", "IM", "GM"]
MODES: Final = ["bullet", "blitz", "rapid"]

# TODO: Add a GM number
# TODO: More robust if you stop when next FIDE rating is lower than current rating
def get_rank_1_number(username, mode, verbose=False):
  if mode not in MODES:
    raise Exception("Invalid mode")
  
  class Colour:
    white = ""
    black = ""
  visited = set()
  
  data = get_leaderboards().json
  top_player = data["leaderboards"]["live_" + mode][0]["username"]
  number = 0
  
  while (top_player != username):
    visited.add(username)
    if (verbose):
      print(username)
    try:
      player_stats = get_player_stats(username).json
    except:
      print("username: \'" + username + "\' does not exist")
      return None

    try:
      best_game = player_stats["stats"]["chess_" + mode]["best"]["game"]
    except:
      print("username: \'" + username + "\' does not have a best game under mode: \'" + mode + "\'")
      return None
    
    page = requests.get(best_game).text
    soup = BeautifulSoup(page, 'html.parser')
    title = soup.title.text.split(" ")
    if(title[1] in TITLES):
      Colour.white = title[2]
      Colour.black = title[5] if title[4] in TITLES else title[4]
    else:
      Colour.white = title[1]
      Colour.black = title[4] if title[3] in TITLES else title[3]
      
    username = Colour.white if username == Colour.black else Colour.black
    if(username in visited):
      print("Unfortunately there appears to be no path/number to #1")
      return None
    if(username == top_player and verbose):
      print(top_player)

    number += 1
  print(number)
  return number