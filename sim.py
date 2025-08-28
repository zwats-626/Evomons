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


class BASIC_INPUTS(Enum):
    SELF_HP = "SELF HP"
    SELF_ENERGY = "SELF ENERGY"
    SELF_ATTACK = "SELF ATTACK"
    SELF_SA = "SELF SA"
    SELF_DEFENSE = "SELF DEFENCE"
    SELF_SD = "SELF SD"
    SELF_SPEED = "SELF SPEED"
    SELF_LEVEL = "SELF LEVEL"
    

class ENCOUNTER_INPUTS(Enum):
    OTHER_HP = "OTHER HP"
    OTHER_ENERHY = "OTHER ENERGY"
    OTHER_ATTACK = "OTHER ATTACK"
    OTHER_SA = "OTHER SA"
    OTHER_DEFENSE = "OTHER DEFENCE"
    OTHER_SD = "OTHER SD"
    OTHER_SPEED = "OTHER SPEED"
    OTHER_LEVEL = "OTHER LEVEL"
    

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
    def __init__(self, input_value, threshold, output, axons):
        self.input_value = input_value
        self.threshold = threshold
        self.output = output
        self.axons = axons


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
all_encounter_inputs = [el for el in ENCOUNTER_INPUTS]
all_basic_inputs = [el for el in BASIC_INPUTS]
all_traits = [t for t in TRAITS]


def random_mon():

    stat_val = []
    for stat in all_stats:
        stat_val.append(random.randrange(1, 100))
    ran_stats = dict(zip(all_stats, stat_val))

    level = 1

    ran_element = all_elements[random.randrange(0, len(all_elements))]

    rand_traits = []
    for i in range(random.randrange(1, len(all_traits) + 1)):

        trait = all_traits[random.randrange(0, len(all_traits))]
        if trait not in rand_traits:
            rand_traits.append(trait)

    rand_encounter_m = rand_dict(all_encounter_moves)

    ran_basic_moves = rand_dict(all_basic_moves)

    # maybe brain could just be ann array of values that 




    temp_brain = []
    return Mon(ran_stats, level, ran_element, rand_traits, rand_encounter_m, ran_basic_moves, temp_brain)
    
def rand_dict(all):
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
    print(mon.traits)

main()




# stats are the basic numbers while traits give bonuses to certain skills ie walking vs swimming

#traits walking stat