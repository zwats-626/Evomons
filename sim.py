import random 
from enum import Enum


class STATS(Enum):
    HP = "HP"
    A = "A"
    SA = "SA"
    D = "D"
    SD = "SD"
    S = "S"

class ELEMENTS(Enum):
    def __init__(self, element, strong, weak):
        self.element = element
        self.strong = strong
        self.weak = weak
    NORMAL = ("Normal", [], [])
    FIRE = ("Fire", ["Plant"], ["Water"])
    WATER = ("Water", ["Fire"], ["Plant"])
    PLANT = ("Plant", ["Water"], ["Fire"])

class TRAITS(Enum):
    HERBAVOR = "herbavor"
    CARNIVOR = "carnivor"
    OMNIVOR = "omnivor"


class BASIC_MOVES(Enum):
    REST = "rest"
    SEARCH_PLANT = "search plant"
    SEARCH_ANIMAL = "search animal"
    SEARCH_MATE = "search mate"
    
class ENCOUNTER_MOVES(Enum):
    SPECIAL_ATTACK = "special attack"
    ATTACK = "attack"
    RUN = "run"

class Neuron():
    def __init__(self, bias, threshold, activation_function, dendrites, axons):
        pass

class Neural_Network():
    def __init__(self, inputs, hiddens, outputs):
        self.inputs = inputs
        self.outputs = outputs 
        self.hiddens = hiddens
    

class Mon():
    def __init__(self, stats, level, element, traits, encounter_moves, basic_moves, brain):
        self.stats = stats
        self.level = level
        self.element = element
        self.traits = traits
        self.encounter_moves = encounter_moves
        self.basic_moves = basic_moves
        self.brain = brain

class Environment():
    def __init__(self, temp, humidity, vegitation):
        self.temp = temp
        self.humidity = humidity
        self.vegitation = vegitation

all_stats = [stat for stat in STATS]
all_elements = [el for el in ELEMENTS]
all_encounter_moves = [m for m in ENCOUNTER_MOVES]
all_basic_moves = [m for m in BASIC_MOVES]

def random_mon():

    stat_val = []
    for stat in all_stats:
        stat_val.append(random.randrange(1, 100))
    ran_stats = dict(zip(all_stats, stat_val))

    level = 1

    ran_element = all_elements[random.randrange(0, len(all_elements))]

    temp_traits = []
    temp_skills = []

    rand_encounter_m = rand_elements(all_encounter_moves)

    ran_basic_moves = rand_elements(all_basic_moves)




    temp_brain = []
    return Mon(ran_stats, level, ran_element, temp_traits, rand_encounter_m, ran_basic_moves, temp_brain)
    
def rand_elements(all):
    key = []
    value = []
    for i in range(random.randrange(1, len(all))):
        key.append(all[random.randrange(0, len(all))])
        value.append(random.randrange(1, 100))

    return dict(zip(key, value))

enviroment = Environment(80, 50, 1000)
def main():
    #are there animals in ecosystem?

    #if no generate batch of random mons

    #run simulation
    mon = random_mon()
    print(mon.stats)
    print(mon.level)
    print(mon.element)
    print(mon.encounter_moves)
    print(mon.basic_moves)

main()


# stats are the basic numbers while traits give bonuses to certain skills ie walking vs swimming

#traits walking stat