import requests
import json
from room_graph import room_graph
from time import sleep
from player import Player
from room import Room
import random
import pickle


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

while len(room_graph.vertices) < 10:
    print('len of arr', len(room_list))
    print('len graph', len(room_graph.vertices))
    print('vistied', visited)
    backtrack = False
    if len(room_list) < 1:
        r = requests.get(url=init, headers=head)
        try:
            res = r.json()
            cooldown = int(res['cooldown'])
            room_id = res['room_id']
            exits = res['exits']
            room_list.append(room_id)
            room_graph.vertices[room_id] = [None, None]
            room_graph.vertices[room_id][0] = res
            room_graph.vertices[room_id][1] = {}
            last_move = exits[random.randint(0, len(exits) - 1)]
            visited[room_id] = last_move
        except ValueError:
            print('Error: Non-json response')
            break

    else:
        print(last_move, 'last_move')
        sleep(cooldown)
        last_room = room_list[-1]
        exits = room_graph.vertices[room_list[-1]][0]['exits']
        print(exits, 'exits')

        if last_move in exits: # try to keep going the same way
            direction = last_move
        elif len(exits) == 1:
            # send the next room as a param
            backtrack = True
            direction = exits[0]
        else:
            try:
                direction = opposite_pairs[last_move][random.randint(0, 2)]
            # direction = exits[random.randint(0, len(exits) - 1)]
            except:
                direction = exits[random.randint(0, len(exits) - 1)]
        
        
        # direction = exits[-1]
        

        print(direction)


        obj  = { "direction": direction}
        if backtrack is False:
            r = requests.post(url=url, data=json.dumps(obj), headers=head)
        else:
            obj_back = { 'direction': direction, 'next_room_id': str(room_list[-2])}
            r = requests.post(url=url, data=json.dumps(obj_back), headers=head)
        print('BACKTRACK', backtrack)
        try:
            res = r.json()
            print(f'\n{res}\n')
            cooldown=int(res['cooldown'])
            room_id = res['room_id']
            print(f'\nROOM {room_id}\n')
            exits = res['exits']
            room_graph.vertices[room_id] = [None, None]
            room_graph.vertices[room_id][0] = res
            room_graph.vertices[room_id][1] = {}
            room_graph.vertices[room_id][1][opposite_dir[direction]] = room_list[-1]
            room_graph.vertices[room_list[-1]][1][opposite_dir[direction]] = room_id
            room_list.append(room_id)
            visited[room_id] = direction
            print('rooms list', room_list)
        except KeyError:
            cooldown=int(math.ceil(res['cooldown']))
        except ValueError:
            print('Error: non-json response')
            break

f.write(json.dumps(room_graph.vertices))

