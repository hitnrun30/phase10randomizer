import phase10typelogic
from phase10typelogic import create_phase_logic
import random

def create_phase():
    cards = 0
    total_cards = 0
    phase = ""
    phase_tot = ""
        
    while True:
        if (total_cards < 4) or (total_cards <= 7 and bool(random.getrandbits(1))):
            phase, cards = create_phase_logic(phase, total_cards)
        else:
            break
            
        if phase_tot != "":
            phase_tot += " + " + phase
        else:
            phase_tot = phase
        
        total_cards += cards
        if total_cards > 7:
            break
        
    return phase_tot


#f = open('src/data/phase10data.json',)
#data = json.load(f)
chosen = []
for n in range(10):
    while True:
        selection = create_phase()
        if selection not in chosen:
            chosen.append(selection)
            break
for n in range(10):
    print(f'Phase {n+1:2}: {chosen[n]}')


