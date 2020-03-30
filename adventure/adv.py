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


traversal_path = [] # needs to be a list of directions
room_list = []


visited = set()

def dft_recursive(room_id):
    room_list.append(room_id)
    if room_id not in visited:
        visited.add(room_id)

        for k, v in room_graph.vertices[room_id]['exits']: # tuple w/ k, v pair
            if v not in visited:
                dft_recursive(v)
                room_list.append(room_id)
                print('YO', room_id)

def convert_to_directions(rooms_list):
    for i in range(0, len(rooms_list) - 1):
        for direction, room_id in room_graph[rooms_list[i]][1].items():
            if room_id == rooms_list[i + 1]:
                traversal_path.append(direction)

url = "https://lambda-treasure-hunt.herokuapp.com/api/adv/move/"
init = "https://lambda-treasure-hunt.herokuapp.com/api/adv/init/"
head = { 
    "Content-Type": "application/json",
    "Authorization": "Token 40f723b2160bbfed3578b03ccbc150ac394bd78e"
    }

cooldown = 0

f = open('map.txt', 'w')

while len(room_graph.vertices) < 2:
    print('len of arr', len(room_list))
    print('len graph', len(room_graph.vertices))
    if len(room_list) < 1:
        r = requests.get(url=init, headers=head)
        try:
            res = r.json()
            cooldown = int(res['cooldown'])
            room_id = res['room_id']
            # f.write("%s\n" % res)
            # f.write("%s\n" % room_id: {res})
            room_graph.vertices[room_id] = res
            room_list.append(room_id)
        except ValueError:
            print('Error: Non-json response')
            break

    else:
        sleep(cooldown)
        exits = room_graph.vertices[room_list[-1]]['exits']
        direction = exits[random.randint(0, len(exits) - 1)] # choose random direction
        print(direction)
        obj  = { "direction": direction}
        # r = requests.post(url, data = obj, headers = head)
        r = requests.post(url=url, data=json.dumps(obj), headers=head)
        print(r)
        try:
            res = r.json()
            cooldown=int(res['cooldown'])
            room_id = res['room_id']
            room_graph.vertices[room_id] = res
            room_list.append(room_id)
            # f.write("%s\n" % room_id: res)
            # f.write(json.dumps({room_id: res}))
            print('rooms list', room_list)
            print(res)
        except ValueError:
            print('Error: non-json response')
            break

f.write(json.dumps(room_graph.vertices))
# with open('map.txt', 'w') as f:
#    for line in room_graph.vertices:
#        f.write(json.dumps(line))

# f.close()