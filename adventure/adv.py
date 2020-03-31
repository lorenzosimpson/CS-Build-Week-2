import requests
import json
from room_graph import room_graph
from time import sleep
from player import Player
from room import Room
import random
import pickle
import math


starting_room = Room('A Dark Room', 'You cannot see anything.', 60, 60)
player = Player(starting_room)


# traversal_path = [] # needs to be a list of directions
room_list = []



url = "https://lambda-treasure-hunt.herokuapp.com/api/adv/move/"
init = "https://lambda-treasure-hunt.herokuapp.com/api/adv/init/"
head = { 
    "Content-Type": "application/json",
    "Authorization": "Token 40f723b2160bbfed3578b03ccbc150ac394bd78e"
    }

cooldown = 0

f = open('./map.txt', 'w')

opposite_dir = {
    'n': 's',
    's': 'n',
    'w': 'e',
    'e': 'w'
}

opposite_pairs = {
    'n': ['e', 'w'],
    's': ['e', 'w'],
    'e': ['n', 's'],
    'w': ['n', 's']
}

visited = {}
last_move = None


# get first room
# sleep 

# get first room

current_room = None

r = requests.get(url=init, headers=head)
try:
    res = r.json()
    cooldown = int(res['cooldown'])
    room_id = res['room_id']
    exits = res['exits']
    room_graph.vertices[room_id] = [None, None]
    room_graph.vertices[room_id][0] = res
    room_graph.vertices[room_id][1] = {}
    room_list.append(room_id)
    current_room = room_id


    visited[room_id] = []

    print('STARTING ROOM', room_id)
except ValueError:
    print('Error: Non-json response')


# sleep for first cooldown amount
sleep(cooldown)

# while for all other rooms


while len(room_graph.vertices) < 499:
    print('-----')
    sleep(cooldown)
    print(room_list)
    print(visited)
    print('TOTAL MOVES', len(room_list)- 1)
    print('UNIQUE ROOMS', len(room_graph.vertices))
    backtrack = False

    current_room = room_list[-1]
    if current_room in visited.keys():
        visited_directions = visited[current_room]
    else:
        visited_directions = []
    # load the previous room's exits, and get ready to exit
    exits = room_graph.vertices[current_room][0]['exits']

    print(f'EXITS: {exits}')


    # try to pick a random direction NOT in the visited 
    # gen random direction
        # if not in the visited directions, use that as direction
    dirs = ['n', 's', 'e', 'w']
    try:
        i = 3
        while dirs[i] not in exits or dirs[i] in visited_directions:
            i -= 1
        direction = dirs[i]

    except IndexError:
        if len(exits) == 1:
            direction = exits[0]
        else:
            direction = exits[random.randint(0, len(exits) - 1)]

        # if it is, generate a new one
        # if all directions have been visited, keep a random one 
    
   

    print(f'\n GUESS DIRECTION: {direction}')

   

    visited_directions.append(direction)

    if len(room_list) == 1:
        last_move = direction

    if len(room_list) > 1 and direction == opposite_dir[last_move]:
        backtrack = True

    print(f'\n ACTUAL DIRECTION: {direction}')

    obj  = {"direction": direction}

    if backtrack is False:
        r = requests.post(url=url, data=json.dumps(obj), headers=head)
    else:
        obj_back = { 'direction': direction, 'next_room_id': str(room_list[-2])}
        r = requests.post(url=url, data=json.dumps(obj_back), headers=head)
    print('BACKTRACK', backtrack)

    try:
        res = r.json()
        print(f'\n{res}\n')
        cooldown=int(math.ceil(res['cooldown']))
        room_id = res['room_id']
        print(f'\nROOM {room_id}\n')
        exits = res['exits']
        room_graph.vertices[room_id] = [None, None]
        room_graph.vertices[room_id][0] = res
        room_graph.vertices[room_id][1] = {}
        room_graph.vertices[room_id][1][opposite_dir[direction]] = room_list[-1]
        room_graph.vertices[room_list[-1]][1][opposite_dir[direction]] = room_id
        room_list.append(room_id)
        last_move = direction
        if room_id not in visited.keys():
            visited[room_id] = []
    except KeyError:
        cooldown=int(math.ceil(res['cooldown']))
    except ValueError:
        print('Error: non-json response')
        break








# while len(room_graph.vertices) < 500:
#     print('len of arr', len(room_list))
#     print('len graph', len(room_graph.vertices))
#     print('vistied', visited)
#     backtrack = False
#     if len(room_list) < 1:
#         r = requests.get(url=init, headers=head)
#         try:
#             res = r.json()
#             cooldown = int(res['cooldown'])
#             room_id = res['room_id']
#             exits = res['exits']
#             room_list.append(room_id)
#             room_graph.vertices[room_id] = [None, None]
#             room_graph.vertices[room_id][0] = res
#             room_graph.vertices[room_id][1] = {}
#             last_move = exits[random.randint(0, len(exits) - 1)]
#             print('STARTING ROOM', room_id)
#         except ValueError:
#             print('Error: Non-json response')
#             break

#     else:
#         print(last_move, 'last_move')
#         sleep(cooldown)
#         last_room = room_list[-1]
#         exits = room_graph.vertices[room_list[-1]][0]['exits']
#         print(exits, 'exits')

#         rand = random.randint(0, 1)
#         if opposite_pairs[last_move][rand] in exits:
#             direction = opposite_pairs[last_move][rand]
#         else:
#             if rand == 0 and opposite_pairs[last_move][1] in exits:
#                 if not visited[last_room] == opposite_pairs[last_move][1]:
#                     direction = opposite_pairs[last_move][1]
#             elif rand == 1 and opposite_pairs[last_move][0] in exits:
#                 if not visited[last_room] == opposite_pairs[last_move][1]:
#                     direction = opposite_pairs[last_move][0]
#             else:
#                 print(f'\nexception hit')
#                 if last_move in exits: # try to keep going the same way
#                     direction = last_move
#                 elif len(exits) == 1:
#             # send the next room as a param
#                     backtrack = True
#                     direction = exits[0]
#                     direction = exits[random.randint(0, len(exits) - 1)]

#         # direction = exits[random.randint(0, len(exits) - 1)]
            
#         if direction == opposite_dir[last_move]:
#             backtrack = True

        
#         print(f'\n{direction}\n')


#         obj  = {"direction": direction}
#         if backtrack is False:
#             r = requests.post(url=url, data=json.dumps(obj), headers=head)
#         else:
#             obj_back = { 'direction': direction, 'next_room_id': str(room_list[-2])}
#             r = requests.post(url=url, data=json.dumps(obj_back), headers=head)
#         print('BACKTRACK', backtrack)





#         try:
#             res = r.json()
#             print(f'\n{res}\n')
#             cooldown=int(math.ceil(res['cooldown']))
#             room_id = res['room_id']
#             print(f'\nROOM {room_id}\n')
#             exits = res['exits']
#             room_graph.vertices[room_id] = [None, None]
#             room_graph.vertices[room_id][0] = res
#             room_graph.vertices[room_id][1] = {}
#             room_graph.vertices[room_id][1][opposite_dir[direction]] = room_list[-1]
#             room_graph.vertices[room_list[-1]][1][opposite_dir[direction]] = room_id
#             room_list.append(room_id)
#             last_move = direction
#         except KeyError:
#             cooldown=int(math.ceil(res['cooldown']))
#         except ValueError:
#             print('Error: non-json response')
#             break


f.write(json.dumps(room_graph.vertices))

