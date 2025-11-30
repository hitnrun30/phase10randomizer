import phase10typelogic
from phase10typelogic import create_phase_logic 
import random
from collections import Counter
import phase10config

SHOW_PHASE_PROBABILITY = phase10config.CONFIG["SHOW_PHASE_PROBABILITY"]
MIN_CARDS_PER_PHASE = phase10config.CONFIG["MIN_CARDS_PER_PHASE"]
TYPE_MAX_PER_TYPE_GLOBAL = phase10config.CONFIG["TYPE_MAX_PER_TYPE_GLOBAL"]

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

def normalize_phase_str(s: str) -> str:
    if not s:
        return ""
    t = s.strip().lower()
    t = t.replace("1 run of", "run of")
    t = t.replace("1 set of", "set of")
    while "  " in t:
        t = t.replace("  ", " ")
    return t

def is_selection_allowed_by_global_cap(selection, global_type_counts):
    # Each PhasePart in 'selection' contributes 1 to its .type global usage
    # Block if accepting this selection would push any type over TYPE_MAX_PER_TYPE_GLOBAL
    local_add = Counter([p.type for p in selection if getattr(p, "type", None)])
    for t, add in local_add.items():
        if global_type_counts.get(t, 0) + add > TYPE_MAX_PER_TYPE_GLOBAL:
            return False
    return True
        
def create_phase():
    
    phase_tot = []
    total_cards = 0
         
    while True:
        if (total_cards < MIN_CARDS_PER_PHASE) or (total_cards <= 7 and bool(random.getrandbits(1))):
            phase_tot = create_phase_logic(phase_tot)
        else:
            break
        
        total_cards = phase10typelogic.Total_Cards(phase_tot)
        if total_cards > 7:
            break
        
    return phase_tot

def generate_phases():
    """
    Generate the 10 phases as a list of selections (each selection is a list of PhasePart).
    Sorting and probability attachment is handled via phase10typelogic.Sort_Total_Prob.
    """
    chosen = []
    seen_strings = set()
    global_type_counts = Counter()

    for n in range(10):
        while True:
            selection = create_phase()

            # Enforce global uniform per-type cap across ALL phases
            if not is_selection_allowed_by_global_cap(selection, global_type_counts):
                continue

            # Enforce cross-phase exact-string uniqueness (normalized)
            if any(normalize_phase_str(p.str) in seen_strings for p in selection):
                continue

            # Accept selection
            chosen.append(selection)

            # Update global counts and seen strings
            for p in selection:
                if getattr(p, "type", None):
                    global_type_counts[p.type] += 1
                s_norm = normalize_phase_str(p.str)
                if s_norm:
                    seen_strings.add(s_norm)
            break

    # Sort by probability (MC) and attach .probability per phase in Sort_Total_Prob
    chosen = phase10typelogic.Sort_Total_Prob(chosen)
    return chosen

def main():
    phases = generate_phases()
    for n, phase in enumerate(phases, start=1):
        if SHOW_PHASE_PROBABILITY and len(phase) > 0:
            prob = phase[0].probability  # MC probability stored in Sort_Total_Prob
            print(f'<li key={n:>2d}>{concatenate_strings(phase)} (Prob {prob:.6f})</li>')
        else:
            print(f'<li key={n:>2d}>{concatenate_strings(phase)}</li>')

if __name__ == "__main__":
    main()


