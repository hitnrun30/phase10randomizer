import math
import random
from math import comb
#from random import randint as rand
color_rand = 8
wild_rand = 20

class PhasePart:
    def __init__(self):
        self.cards = 0
        self.type = ""
        self.str = ""
        self.probability = 0.0
    
def Check_Type(array, value):
    """
    Checks if a value is in any of the type values in an array of PhasePart objects.

    Args:
        array: The array of PhasePart objects.
        value: The value to check.

    Returns:
        True if the value is in any of the type values in the array, False otherwise.
    """

    for phase_part in array:
        if phase_part.type == value:
            return True

    return False

def Total_Cards(array):
    """
    Adds up the value of cards in an array of PhasePart objects.

    Args:
        array: The array of PhasePart objects.

    Returns:
        The sum of the value of cards in the array.
    """

    total_value = 0
    for phase_part in array:
        total_value += phase_part.cards

    return total_value

def Total_Prob(array) -> float:
    """
    multiply the value of probability in an array of PhasePart objects.

    Args:
        array: The array of PhasePart objects.

    Returns:
        The quotient of the value of probability in the array.
    """
    
    total_value = 0.0
    for phase_part in array:
        total_value += phase_part.probability

    cards = Total_Cards(array)
    
    return round((total_value * comb((108-cards),(10-cards)))/comb(108,10),15)

def Sort_Total_Prob(array_of_arrays):
    """
    Sorts an array of arrays of PhasePart objects by the multiply_card_values.

    Args:
        array_of_arrays: The array of arrays of PhasePart objects.

    Returns:
        The sorted array of arrays of PhasePart objects.
    """
    
    return sorted(array_of_arrays, key=Total_Prob, reverse=True)

    
def create_phase_logic(phase_tot):
    
    part = PhasePart()
    
    choice = random.choice(["run", "set", "color", "e-o", "hi-lo", "run-set"])
    
    #each phase can not have the same type more than once
    if len(phase_tot) > 0:
        while Check_Type(phase_tot, choice):
            choice = random.choice(["run", "set", "color", "e-o", "hi-lo", "run-set"])
    
    part.type = choice
    cards = Total_Cards(phase_tot)
    match choice:
        case "run":
            part = run_type(part,cards)
            
        case "set":
            part = set_type(part,cards)
            
        case "color":
            part = color_type(part,cards) 
            
        case "e-o":
            part = e_o_type(part,cards) 
        
        case "hi-lo":
            part = high_low_type(part,cards)
        
        case "run-set":
            part = run_set_type(part,cards)
    
    if part.str != "":
        phase_tot.append(part)        
        
    return phase_tot
            
def run_type(part, cards_tot):
    w = 1
    clr = 1
    
    if cards_tot < 5:
        x_value = random.randint(1, 2)
    else:
        x_value = 1
        
    color = ""    
    if random.randint(1, color_rand) == 1:
        color = "Color "
        clr = comb(4,1)
    
    wild = ""    
    if random.randint(1, wild_rand) == 1:
        wild = " with Wild"
        w = 2
        
    if x_value == 1:
        y_value = random.randint(3, 10 - cards_tot)        
        part.str = f"{color}Run of {y_value}{wild}"
    else:
        y_value = random.randint(3, min(5, math.floor((10 - cards_tot)/x_value)))
        part.str = f"{x_value} {color}Runs of {y_value}{wild}"
        
    part.cards = x_value * y_value
    part.probability = (comb((12 - y_value + 1),x_value)) * clr * (pow(comb(8,1),(y_value-w)))
    
    return part
    
def set_type(part, cards_tot):
    plural = ""
    
    x_value = random.randint(1, min(5, math.floor((10 - cards_tot)/3)))
        
    y_value = random.randint(3, min(5, math.floor((10 - cards_tot)/x_value)))
    
    if x_value != 1:
        plural = "s"
        
    part.phase = f"{x_value} Set{plural} of {y_value}"
    part.cards = x_value * y_value
    part.probability = (comb(12, x_value)) * (pow(comb(8, y_value), x_value))
    
    return part
    
def color_type(part, cards_tot):
    w = 0
    wld = 1
    
    x_value = random.randint(3, 10 - cards_tot)
    
    wild = ""    
    if random.randint(1, wild_rand) == 1:
        wild = " with Wild"
        wld = comb(8,1)
        w = 1
        
    part.str = f"{x_value} of One Color{wild}"
    part.cards = x_value
    part.probability = (comb(4,1)) * wld * (comb(24, (x_value-w)))
    
    return part
    
def e_o_type(part, cards_tot):
    rand = random.randint(1, 12)
    clr = 1
    
    if (rand > 10):
        e_o = "Even or Odd"
    elif (rand % 2) == 0:
        e_o = "Even"   
    else:
        e_o = "Odd"
        
    x_value = 1
    y_value = random.randint(3, 10 - cards_tot)
    
    color = ""
    if random.randint(1, color_rand) == 1:
        color = "Color "
        clr = comb(4,1)        
        
    part.str = f"{x_value} {color}{e_o} of {y_value}"
    part.cards = x_value * y_value
    part.probability = (comb(2,1)) * clr * (comb(48, y_value))
    
    return part
    
def high_low_type(part, cards_tot):
    x_value = random.randint(3, 10 - cards_tot)
    hi_lo_value = random.choice(["Over", "Under"])
    y_value = random.randint(4, 9)
    u_o = 0
    
    if hi_lo_value == "Over":
        u_o = -y_value + 12    
    #    y_value = random.randint(8, 9)
    else:
        u_o = y_value - 1
    #    y_value = random.randint(4, 5)
    
    color = ""
    if random.randint(1, color_rand) == 1:
        color = "of One Color "
        
    part.str = f"{x_value} {hi_lo_value} {y_value}"
    part.cards = x_value
    part.probability = (comb((8 * (u_o)), x_value))
    
    return part
    
def run_set_type(part, cards_tot):
    if (math.floor((10 - cards_tot)/2)) >= 3:
        x_value = random.randint(3, math.floor((10 - cards_tot)/2))
        hi_lo_value = random
            
        part.str = f"Run of {x_value} Pairs"
        part.cards = x_value * 2
        part.probability = (comb((12 - x_value + 1), 2)) * (pow(comb(8,x_value), (x_value - 1)))
        
    else:
        part.str = ""
        part.cards = 0
        part.probability = 0
    
    
    return part