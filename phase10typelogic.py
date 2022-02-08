import math
import random
#from random import randint as rand

def create_phase_logic(phase, total_cards):
    choice = random.choice(["run", "set", "color", "e-o"])
    match choice:
        case "run":
            phase, total_cards = run_type(phase, total_cards)
            
        case "set":
            phase, total_cards = set_type(phase, total_cards)
            
        case "color":
            phase, total_cards = color_type(phase, total_cards) 
            
        case "e-o":
            phase, total_cards = e_o_type(phase, total_cards) 
            
    return phase, total_cards
            
def run_type(phase, cards):
    plural = ""
    
    if cards < 5:
        x_value = random.randint(1, 2)
    else:
        x_value = 1
        
    if x_value == 1:
        y_value = random.randint(3, 10 - cards)        
    else:
        y_value = random.randint(3, min(5, math.floor((10 - cards)/x_value)))
        plural = "s"
    
    color = ""    
    if random.randint(0, 1) == 1:
        color = "color "
        
    phase = f"{x_value} {color}run{plural} of {y_value}"
    cards = x_value * y_value
    return phase, cards
    
def set_type(phase, cards):
    plural = ""
    
    x_value = random.randint(1, min(5, math.floor((10 - cards)/2)))
        
    y_value = random.randint(2, min(5, math.floor((10 - cards)/x_value)))
    
    if x_value != 1:
        plural = "s"
        
    phase = f"{x_value} set{plural} of {y_value}"
    cards = x_value * y_value
    return phase, cards
    
def color_type(phase, cards):
    x_value = random.randint(3, 10 - cards)
    phase = f"{x_value} of one color"
    cards = x_value
    return phase, cards
    
def e_o_type(phase, cards):
    e_o = random.choice(["even", "odd", "even or odd"])
            
    if cards < 5:
        x_value = random.randint(1, 2)
    else:
        x_value = 1
        
    if x_value == 1:
        y_value = random.randint(3, 10 - cards)
    else:
        y_value = random.randint(3, math.floor((10 - cards) / 2))
    
    color = ""
    if random.randint(0, 1) == 1:
        color = "color "
    phase = f"{x_value} {color}{e_o} of {y_value}"
    cards = x_value * y_value
    return phase, cards