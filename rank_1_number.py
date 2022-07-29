import requests
from chessdotcom import get_player_stats
from bs4 import BeautifulSoup
from typing import Final

TITLES: Final = ["WNM", "WCM", "WFM", "WIM", "WGM", "NM", "CM", "FM", "IM", "GM"]
MODES: Final = ["bullet", "blitz", "rapid"]

def get_rank_1_number(username, mode, verbose=False):
  if mode not in MODES:
    raise Exception("Invalid mode")
  
  white = ""
  black = ""
  visited = set()
  
  number = -1
  prevRating = -1
  rating = 0
  
  while (prevRating < rating):
    visited.add(username)

    # Get player stats
    try:
      player_stats = get_player_stats(username).json
    except:
      print("username: \'" + username + "\' does not exist")
      return None
    
    # Get new best rating win
    try:
      best_game = player_stats["stats"]["chess_" + mode]["best"]["game"]
      prevRating = rating
      rating = player_stats["stats"]["chess_" + mode]["best"]["rating"]
    except:
      print("username: \'" + username + "\' does not have a best game under mode: \'" + mode + "\'")
      return None

    # Break if highest rating has already been reached
    if(prevRating > rating):
      break
    if (verbose):
      print(str(number + 1) + ": " + username)
    
    # Get opponent of best rating win
    page = requests.get(best_game).text
    soup = BeautifulSoup(page, 'html.parser')
    title = soup.title.text.split(" ")
    if(title[1] in TITLES):
      white = title[2]
      black = title[5] if title[4] in TITLES else title[4]
    else:
      white = title[1]
      black = title[4] if title[3] in TITLES else title[3]
    username = white if username == black else black

    if(username in visited):
      print("There appears to be no path/number to #1")
      return None
    number += 1

  print("Your rank 1 number/distance is: " + str(number))
  return number

def get_titled_number(username, mode, title_list=TITLES, verbose=False):
  if mode not in MODES:
    raise Exception("Invalid mode")

  white = ""
  black = ""
  visited = set()
  
  number = 0
  game_title = []
  if(verbose):
    print("0: " + username)
  
  while (set(title_list).isdisjoint(game_title)):
    visited.add(username)
        
    # Get player stats
    try:
      player_stats = get_player_stats(username).json
    except:
      print("username: \'" + username + "\' does not exist")
      return None
    
    # Get best rating win
    try:
      best_game = player_stats["stats"]["chess_" + mode]["best"]["game"]
    except:
      print("username: \'" + username + "\' does not have a best game under mode: \'" + mode + "\'")
      return None

    # Get opponent of best rating win
    page = requests.get(best_game).text
    soup = BeautifulSoup(page, 'html.parser')
    game_title = soup.title.text.split(" ")
      
    if(game_title[1] in TITLES):
      white = game_title[2]
      black = game_title[5] if game_title[4] in TITLES else game_title[4]
    else:
      white = game_title[1]
      black = game_title[4] if game_title[3] in TITLES else game_title[3]
      
    username = white if username == black else black
    
    if(username in visited):
      print("There appears to be no path/number to title(s): " + title_list)
      return None
    
    number += 1
    
    if (verbose):
      print(str(number) + ": " + username)
    
    # Break if desired title is reached
    if(not set(title_list).isdisjoint(game_title)):
      break;

  print("Your titled number/distance is: " + str(number))
  return number