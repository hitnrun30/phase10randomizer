import math
import random
from random import randint as rand
import json

f = open('src/data/phase10data.json',)
data = json.load(f)

chosen = []
for n in range(10):
    while True:
        selection = random.choice(data[str(n+1)])
        if selection not in chosen:
            chosen.append(selection)
            break
for n in range(10):
    print(f'Phase {n+1}: {chosen[n]}')
