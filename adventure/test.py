from ast import literal_eval
import json
from player import Player
from room import Room
from util import Stack

# map_file = 'map.txt'

# room_graph = literal_eval(open(map_file, 'r').read())

# result = json.loads(room_graph)

# # for line in mapfile:
# #     print(line)

# print(result)

starting_room = Room('A Dark Room', 'You cannot see anything.', 432, 60, 60)
player = Player(starting_room)

with open('map.txt') as f:
    data = json.load(f)
 

room_graph = {int(k): v for k,v in data.items()}




traversal_path = [] # needs to be a list of directions
room_list = []


visited = set()

def dft_recursive(room_id):
    room_list.append(room_id)
    if room_id not in visited:
        visited.add(room_id)

        for k, v in room_graph[room_id][1].items(): # tuple w/ k, v pair
            if v not in visited:
                dft_recursive(v)
                room_list.append(room_id)
                print('YO', room_id)



def convert_to_directions(rooms_list):
    for i in range(0, len(rooms_list) - 1):
        for direction, room_id in room_graph[rooms_list[i]][1].items():
            if room_id == rooms_list[i + 1]:
                traversal_path.append(direction)

dft_recursive(player.current_room.room_id)
convert_to_directions(room_list)

print(room_list)
print(traversal_path)
print(len(visited))
