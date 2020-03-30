from ast import literal_eval
import json

# map_file = 'map.txt'

# room_graph = literal_eval(open(map_file, 'r').read())

# result = json.loads(room_graph)

# # for line in mapfile:
# #     print(line)

# print(result)

with open('map.txt') as f:
    data = json.load(f)
    print(type(data))

d = {int(k): v for k,v in data.items()}

print(len(d))