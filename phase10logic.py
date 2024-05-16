import phase10typelogic
from phase10typelogic import create_phase_logic 
import random

def concatenate_strings(array):
    """
    Concatenates each string in an array with a " + " between them, without a trailing " + ".

    Args:
        array: The array of strings.

    Returns:
        The concatenated string.
    """

    concatenated_string = ""
    for phase_part in array:
        concatenated_string += phase_part.str + " + "

    # Remove the trailing " + ".
    concatenated_string = concatenated_string[:-2]

    return concatenated_string
        
def create_phase():
    
    phase_tot = []
    total_cards = 0
         
    while True:
        if (total_cards < 5) or (total_cards <= 7 and bool(random.getrandbits(1))):
            phase_tot = create_phase_logic(phase_tot)
        else:
            break
        
        total_cards = phase10typelogic.Total_Cards(phase_tot)
        if total_cards > 7:
            break
        
    return phase_tot


#f = open('src/data/phase10data.json',)
#data = json.load(f)
chosen = []
seen_strings = set()

for n in range(10):
    while True:
        selection = create_phase()
        # This line checks if any of the strings in the `selection` array are already in the `seen_strings` set.
        if not any(selection_part.str in seen_strings for selection_part in selection):
            # If none of the strings in the `selection` array are already in the `seen_strings` set,
            # then the `selection` array is appended to the `chosen` array.
            chosen.append(selection)

            # Add the strings in the `selection` array to the `seen_strings` set.
            for selection_part in selection:
                seen_strings.add(selection_part.str)

            break
        
chosen = phase10typelogic.Sort_Total_Prob(chosen)

for n in range(10):
    print(f'<li key={n+1:>2d}>{concatenate_strings(chosen[n])}</li>') # Prob {str(phase10typelogic.Total_Prob(chosen[n])) }</li>')
