import json
from pprint import pprint

with open('load_data1.json', 'r') as f:
  loads = json.loads(f.read())

  print(len(loads))

  for load in loads:
    pprint(load)
    print()