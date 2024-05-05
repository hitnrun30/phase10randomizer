import phase10typelogic
from phase10typelogic import create_phase_logic
import random

def create_phase():
    cards = 0
    total_cards = 0
    phase = ""
    phase_tot = ""
        
    while True:
        if (total_cards < 5) or (total_cards <= 7 and bool(random.getrandbits(1))):
            phase, cards = create_phase_logic(phase, total_cards)
        else:
            break
            
        if phase_tot != "":
            if ("set" in phase_tot and "set" in phase) and \
               (phase_tot[-1] == phase[-1]):
                phase_tot = f"{int(phase_tot[:1]) + int(phase[:1])} sets of {phase[-1]}"
            elif ("even" in phase_tot or "odd" in phase_tot) and \
                ("even" in phase or "odd" in phase) and \
                (phase_tot[0:-1] == phase[0:-1]):
                phase_tot = f"{phase[0:-1]}{int(phase_tot[-1]) + int(phase[-1])}"
            elif ("above" in phase_tot and "above" in phase) or \
                ("below" in phase_tot and "below" in phase) or \
                (phase == ""):
                phase = ""
                cards = 0
            else:    
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
        if not any(selection in s for s in chosen):
            chosen.append(selection)
            break
for n in range(10):
    print(f'<li key={n+1}>{chosen[n]}</li>')
