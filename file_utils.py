import os
import json

#文件检查
def check_players_json():

    if not os.path.exists("resource/Players.json"):
        with open("resource/Players.json", "w") as outfile:
            json.dump([], outfile)

#文件信息检查
def read_players_data():
    try:
        with open('resource/Players.json', 'r') as file:
            players_data = json.load(file)
    except FileNotFoundError:
        players_data = []
    return players_data