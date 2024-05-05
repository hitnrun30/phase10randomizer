import math
import random
#from random import randint as rand
color_rand = 8
wild_rand = 20

def create_phase_logic(phase, total_cards):
    choice = random.choice(["run", "set", "color", "e-o", "hi-lo", "run-set"])
    match choice:
        case "run":
            phase, total_cards = run_type(phase, total_cards)
            
        case "set":
            phase, total_cards = set_type(phase, total_cards)
            
        case "color":
            phase, total_cards = color_type(phase, total_cards) 
            
        case "e-o":
            phase, total_cards = e_o_type(phase, total_cards) 
        
        case "hi-lo":
            phase, total_cards = high_low_type(phase, total_cards)
        
        case "run-set":
            phase, total_cards = run_set_type(phase, total_cards)
            
    return phase, total_cards
            
def run_type(phase, cards):
    
    if cards < 5:
        x_value = random.randint(1, 2)
    else:
        x_value = 1
        
    color = ""    
    if random.randint(1, color_rand) == 1:
        color = "Color "
    
    wild = ""    
    if random.randint(1, wild_rand) == 1:
        wild = " with Wild"
        
    if x_value == 1:
        y_value = random.randint(3, 10 - cards)        
        phase = f"{color}Run of {y_value}{wild}"
    else:
        y_value = random.randint(3, min(5, math.floor((10 - cards)/x_value)))
        phase = f"{x_value} {color}Runs of {y_value}"
        
    cards = x_value * y_value
    return phase, cards
    
def set_type(phase, cards):
    plural = ""
    
    x_value = random.randint(1, min(5, math.floor((10 - cards)/3)))
        
    y_value = random.randint(3, min(5, math.floor((10 - cards)/x_value)))
    
    if x_value != 1:
        plural = "s"
        
    phase = f"{x_value} Set{plural} of {y_value}"
    cards = x_value * y_value
    return phase, cards
    
def color_type(phase, cards):
    x_value = random.randint(3, 10 - cards)
    
    wild = ""    
    if random.randint(1, wild_rand) == 1:
        wild = " with Wild"
        
    phase = f"{x_value} of One Color{wild}"
    cards = x_value
    return phase, cards
    
def e_o_type(phase, cards):
    rand = random.randint(1, 12)
    
    if (rand > 10):
        e_o = "Even or Odd"
    elif (rand % 2) == 0:
        e_o = "Even"   
    else:
        e_o = "Odd"
        
    x_value = 1
    y_value = random.randint(3, 10 - cards)
    
    color = ""
    if random.randint(1, color_rand) == 1:
        color = "Color "
            
    phase = f"{x_value} {color}{e_o} of {y_value}"
    cards = x_value * y_value
    return phase, cards
    
def high_low_type(phase, cards):
    x_value = random.randint(3, 10 - cards)
    hi_lo_value = random.choice(["Over", "Under"])
    y_value = random.randint(3, 9)
    #if hi_lo_value == "Over":
    #    y_value = random.randint(8, 9)
    #else:
    #    y_value = random.randint(4, 5)
    
    color = ""
    if random.randint(1, color_rand) == 1:
        color = "of One Color "
        
    phase = f"{x_value} {hi_lo_value} {y_value}"
    cards = x_value
    return phase, cards
    
def run_set_type(phase, cards):
    if (math.floor((10 - cards)/2)) >= 3:
        x_value = random.randint(3, math.floor((10 - cards)/2))
        hi_lo_value = random
        
        
            
        phase = f"Run of {x_value} Pairs"
        cards = x_value * 2
    else:
        phase = ""
        cards = 0
        
    return phase, cards