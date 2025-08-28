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
    RANDOM = "RANDOM"
    SELF_HP = "SELF HP"
    SELF_ENERGY = "SELF ENERGY"
    SELF_ATTACK = "SELF ATTACK"
    SELF_SA = "SELF SA"
    SELF_DEFENSE = "SELF DEFENCE"
    SELF_SD = "SELF SD"
    SELF_SPEED = "SELF SPEED"
    SELF_LEVEL = "SELF LEVEL"
    SELF_HPB = "SELF HP BUFF"
    SELF_ENERGYB = "SELF ENERGY BUFF"
    SELF_ATTACKB = "SELF ATTACK BUFF"
    SELF_SAB = "SELF SA BUFF"
    SELF_DEFENSEB = "SELF DEFENCE BUFF"
    SELF_SDB = "SELF SD BUFF"
    SELF_SPEEDB = "SELF SPEED BUFF"
    
class ENCOUNTER_INPUTS(Enum):
    OTHER_HP = "OTHER HP"
    OTHER_ENERGY = "OTHER ENERGY"
    OTHER_ATTACK = "OTHER ATTACK"
    OTHER_SA = "OTHER SA"
    OTHER_DEFENSE = "OTHER DEFENCE"
    OTHER_SD = "OTHER SD"
    OTHER_SPEED = "OTHER SPEED"
    OTHER_LEVEL = "OTHER LEVEL"
    SIMILAR_SPECIES = "SIMILAR SPECIES"
    OTHER_HPB = "OTHER HPB"
    OTHER_ENERGYB = "OTHER ENERGY BUFF"
    OTHER_ATTACKB = "OTHER ATTACK BUFF"
    OTHER_SAB = "OTHER SA BUFF"
    OTHER_DEFENSEB = "OTHER DEFENCE BUFF"
    OTHER_SDB = "OTHER SD BUFF"
    OTHER_SPEEDB = "OTHER SPEED BUFF"
    
class BASIC_MOVES(Enum):
    REST = "rest"
    SEARCH_PLANT = "search plant"
    SEARCH_ANIMAL = "search animal"
    SEARCH_MATE = "search mate"

class ENCOUNTER_MOVES(Enum):
    SPECIAL_ATTACK = "special attack"
    ATTACK = "attack"
    RUN = "run"
    MATE = "mate"

class NEURON_FUNCTIONS(Enum):
    MULT = "*"
    ADD = "+"
    DIVIDE = "/"
    SUBTRACT = "-"

class Neuron():
    def __init__(self, action, input_value, threshold, output, axons, bias, afunction):
        self.action = action
        self.input_value = input_value
        self.threshold = threshold
        self.output = output
        self.axons = axons
        self.bias = bias
        self.afunction = afunction

class Neural_Network():
    def __init__(self, inputs, hiddens, outputs):
        self.inputs = inputs
        self.outputs = outputs 
        self.hiddens = hiddens
    
class Mon():
    def __init__(self, stats, buffs, level, element, traits, encounter_moves, basic_moves, brain):
        self.stats = stats
        self.buffs = buffs
        self.level = level
        self.element = element
        self.traits = traits
        self.encounter_moves = encounter_moves
        self.basic_moves = basic_moves
        self.brain = brain
        self.energy = 0

class plant():
    def __init__(self, stats, element, buffs):
        self.stats = stats
        self.element = element
        self.buffs = buffs

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
all_funcions = [func for func in NEURON_FUNCTIONS]


TOTAL_SPACE = 10000
SPACE_TAKEN = 0

ALL_PLANTS = []
ALL_MONS = []

def random_plant():

    value = []
    buff = []
    for stats in all_stats:
        value.append(random.randrange(1, 100))
        buff.append(0)
    stats = dict(zip(all_stats, value))

    element = all_elements[random.randrange(0, len(all_elements))]

    buffs = dict(zip(all_stats, buff))

    return plant(stats, element, buffs)


def plant_turn(plant):
    global SPACE_TAKEN
    global TOTAL_SPACE
    global ALL_PLANTS
    size = 0

    for stat in plant.stats:
        size += plant.stats[stat]
    
    regen = size // 8

    if plant.buffs[STATS.HP] < 0:
        plant.buffs[STATS.HP] += regen
    
    if plant.buffs[STATS.HP] > 0:
        plant.buffs[STATS.HP] = 0

    if SPACE_TAKEN < TOTAL_SPACE:
        new_plant = spawn_plant(plant)
        ns = 0
        for stat in new_plant.stats:
            ns += new_plant.stats[stat]

        SPACE_TAKEN += ns
        ALL_PLANTS.append(new_plant)


def spawn_plant(parent):
    values = []
    buffv = []
    for stat in parent.stats:
        value = parent.stats[stat]
        buffv.append(0)
        if random.randrange(0, 100) < 3:
            value += random.randrange(-1, 2)
        if value < 1:
            value = 1
        values.append(value)

    stats = dict(zip(all_stats, values))
    buffs = dict(zip(all_stats, buffv))

    element = parent.element 
    if random.randrange(0, 1000) < 3:
        if element != ELEMENTS.NORMAL:
            element = ELEMENTS.NORMAL
        else:
            element = all_encounter_moves[random.randrange(0, len(all_encounter_moves))]
    
    return plant(stats, element, buffs)


def random_mon():

    stat_val = []
    for stat in all_stats:
        if stat != STATS.HP:
            stat_val.append(random.randrange(1, 100))
        else:
            stat_val.append(4 * random.randrange(1, 100))

    ran_stats = dict(zip(all_stats, stat_val))

    buffs = dict.fromkeys(all_stats, 0)

    level = 1

    ran_element = all_elements[random.randrange(0, len(all_elements))]

    rand_traits = rand_list(all_traits)

    rand_encounter_m = rand_dict(all_encounter_moves)

    ran_basic_moves = rand_dict(all_basic_moves)

    # generate random brain
    basic_inputs = rand_neurons(rand_list(all_basic_inputs))
    encounter_inputs = rand_neurons(rand_list(all_encounter_inputs) + rand_list(all_basic_inputs))

    basic_hidden = rand_neurons([])
    encounter_hidden = rand_neurons([])

    basic_outputs = rand_neurons(rand_list([key for key in ran_basic_moves]))
    encounter_outputs = rand_neurons(rand_list([key for key in  rand_encounter_m]))

    brain = {
        "basic": Neural_Network(basic_inputs, basic_hidden, basic_outputs)  ,
        "encounter": Neural_Network(encounter_inputs, encounter_hidden, encounter_outputs)
    }

    return Mon(ran_stats, buffs, level, ran_element, rand_traits, rand_encounter_m, 
               ran_basic_moves, brain)


def rand_dict(all):
    key = []
    value = []
    for i in range(random.randrange(1, len(all))):
        key.append(all[random.randrange(0, len(all))])
        value.append(random.randrange(1, 100))

    return dict(zip(key, value))


def rand_list(all):
    l = []
    for i in range(random.randrange(1, len(all) + 1)):
        trait = all[random.randrange(0, len(all))]
        if trait not in l:
            l.append(trait)
    return l


def rand_neurons(values):
    l = []
    if values == []:
        values = ["hidden" for i in range(random.randrange(1, max(len(all_basic_moves), len(all_encounter_moves))))]

    for v in values:
        
        input = 0
        thresh = random.randrange(-10, 10)
        output = 0
        axons = [random.randrange(0, len(values)) for i in range(len(values))]
        bias = random.randrange(-1, 1)
        func = all_funcions[random.randrange(0, len(all_funcions))]

        n = Neuron(v, input, thresh, output, axons, bias, func)
        l.append(n)
    return l


def process_network(network, mon, other_mon):
    for neuron in network.inputs:
        neuron.input_value = get_input(neuron.action, mon, other_mon)

    section = network.inputs
    next_sec = network.hiddens
    for i in range(3):
        for neuron in section:
            if i == 1:
                section = network.hiddens
                next_sec = network.outputs
            elif i == 2:
                section = network.outputs
                next_sec = None
            
            for neuron in section:
                if neuron.input_value >= neuron.threshold:
                    out = get_neuron_function(neuron.input_value, neuron.bias, neuron.afunction)
                    for axon in neuron.axons:
                        if  next_sec != None and axon < len(next_sec):
                            next_sec[axon].input_value += out
                        if next_sec == None:
                            neuron.output = out
    highest = network.outputs[0]
    for neuron in network.outputs:
        if neuron.output > highest.output:
            highest = neuron

    return highest.action


def get_neuron_function(input, bias, func):
    match func:
        case NEURON_FUNCTIONS.MULT:
            return (input * bias)
        case NEURON_FUNCTIONS.ADD:
            return (input + bias)
        case NEURON_FUNCTIONS.DIVIDE:
            if bias == 0:
                bias = 1
            return (input / bias)
        case NEURON_FUNCTIONS.SUBTRACT:
            return (input - bias)
        case _:
            print("failed path to neuron function")
            return 0


def get_input(request, mon, other_mon):
    match request:
        case BASIC_INPUTS.RANDOM:
            return random.randrange(0, 100)
        case BASIC_INPUTS.SELF_HP:
            return get_encstat(STATS.HP, mon)
        case BASIC_INPUTS.SELF_ENERGY:
            return calculate_size(mon)
        case BASIC_INPUTS.SELF_ATTACK:
            return get_encstat(STATS.A, mon)
        case BASIC_INPUTS.SELF_SA:
            return get_encstat(STATS.SA, mon)
        case BASIC_INPUTS.SELF_DEFENSE:
            return get_encstat(STATS.D, mon)
        case BASIC_INPUTS.SELF_SD:
            return get_encstat(STATS.SD, mon)
        case BASIC_INPUTS.SELF_SPEED:
            return get_encstat(STATS.S, mon)
        case BASIC_INPUTS.SELF_HPB:
            return get_buffs(STATS.HP, mon)
        case BASIC_INPUTS.SELF_ENERGYB:
            return mon.energy
        case BASIC_INPUTS.SELF_ATTACKB:
            return get_buffs(STATS.A, mon)
        case BASIC_INPUTS.SELF_SAB:
            return get_buffs(STATS.SA, mon)
        case BASIC_INPUTS.SELF_DEFENSEB:
            return get_buffs(STATS.D, mon)
        case BASIC_INPUTS.SELF_SDB:
            return get_buffs(STATS.SD, mon)
        case BASIC_INPUTS.SELF_SPEEDB:
            return get_buffs(STATS.S, mon)
        case BASIC_INPUTS.SELF_LEVEL:
            return mon.level
        case ENCOUNTER_INPUTS.OTHER_HP:
            return get_encstat(STATS.HP, other_mon)
        case ENCOUNTER_INPUTS.OTHER_ENERGY:
            return calculate_size(other_mon)
        case ENCOUNTER_INPUTS.OTHER_ATTACK:
            return get_encstat(STATS.A, other_mon)
        case ENCOUNTER_INPUTS.OTHER_SA:
            return get_encstat(STATS.SA, other_mon)
        case ENCOUNTER_INPUTS.OTHER_DEFENSE:
            return get_encstat(STATS.D, other_mon)
        case ENCOUNTER_INPUTS.OTHER_SD:
            return get_encstat(STATS.SD, other_mon)
        case ENCOUNTER_INPUTS.OTHER_SPEED:
            return get_encstat(STATS.S, other_mon)
        case ENCOUNTER_INPUTS.OTHER_HPB:
            return get_buffs(STATS.HP, other_mon)
        case ENCOUNTER_INPUTS.OTHER_ENERGYB:
            return calculate_size(other_mon)
        case ENCOUNTER_INPUTS.OTHER_ATTACKB:
            return get_buffs(STATS.A, other_mon)
        case ENCOUNTER_INPUTS.OTHER_SAB:
            return get_buffs(STATS.SA, other_mon)
        case ENCOUNTER_INPUTS.OTHER_DEFENSEB:
            return get_buffs(STATS.D, other_mon)
        case ENCOUNTER_INPUTS.OTHER_SDB:
            return get_buffs(STATS.SD, other_mon)
        case ENCOUNTER_INPUTS.OTHER_SPEEDB:
            return get_buffs(STATS.S, other_mon)
        case ENCOUNTER_INPUTS.OTHER_LEVEL:
            return other_mon.level
        case ENCOUNTER_INPUTS.SIMILAR_SPECIES:
            return compare_species(mon, other_mon)
        case _:
            print("neuron input request/path not found")
            return 0


def get_encstat(stat, mon):
    d = calculate_stats(mon, "stats")
    return d[stat]


def get_buffs(stat, mon):
    buff = mon.buffs[stat]
    return buff


def calculate_stats(mon, flag):
    foo = mon.level / 100
    all = all_basic_moves
    stat_value = []
    if flag == "stats":
        all = all_stats
        d = mon.stats
    elif flag == "e moves":
        d = mon.encounter_moves
        all = all_encounter_moves
    else:
        d = mon.basic_moves
        all = all_basic_moves
    for key in d:
        stat_value.append(max(1, int(foo * d[key])))
    return dict(zip(all, stat_value))


def calculate_size(mon):
    size = 0
    flag = "stats"

    for i in range(3):
        if i == 1:
            flag = "e moves"
        elif i == 2:
            flag = ""
        d = calculate_stats(mon, flag)
        size += sum(list(d.values()))

    network = mon.brain['basic']
    for i in range(2):
        if i == 1:
            network = mon.brain['encounter']
        network_section = network.inputs
        for i in range(3):
            if i == 1:
                network_section = network.hiddens
            elif i == 2:
                network_section = network.outputs
            for neuron in network_section:
                size += 1
    return size


def compare_species(mon, other_mon):
    dif = 0
    # compare base_stats
    for stat in all_stats:
        dif += abs(mon.stats[stat] - other_mon.stats[stat])

    # compare element
    if mon.element != other_mon.element:
        dif += 50
        if mon.element != ELEMENTS.NORMAL or other_mon.element != ELEMENTS.NORMAL:
            dif += 50

    # compare base_moves + encounter moves
    mon_moves = mon.encounter_moves
    other_moves = other_mon.encounter_moves
    for i in range(2):
        if i == 1:
            mon_moves = mon.basic_moves
            other_moves = other_mon.basic_moves
        for key in mon_moves:
            if key not in other_moves:
                dif += 10
            else:
                dif += abs(mon_moves[key] - other_moves[key])
        for key in other_moves:
            if key not in mon_moves:
                dif += 10


    # compare traits
    mt = mon.traits
    ot = other_mon.traits
    for i in range(2):
        if i == 1:
            ot = mon.traits
            mt = other_mon.traits
        for trait in mt:
            if trait not in ot:
                dif += 10

    #brain
    mb = mon.brain
    ob = other_mon.brain
    for i in range(2):
        if i == 1:
            mb = other_mon.brain
            ob = mon.brain
        key = 'encounter'
        for j in range(2):
            if j == 1:
                key = 'basic'
            for neuron in mb[key].inputs + mb[key].hiddens + mb[key].outputs:
                if neuron not in ob[key].inputs + ob[key].hiddens + ob[key].outputs:
                    dif += 1

    return dif


def make_move(action, mon, other_mon):
    match action:
        case BASIC_MOVES.REST:
            print("TODO")
        case BASIC_MOVES.SEARCH_PLANT:
            print("TODO")
        case BASIC_MOVES.SEARCH_ANIMAL:
            print("TODO")
        case BASIC_MOVES.SEARCH_MATE:
            print("TODO")

        case ENCOUNTER_MOVES.SPECIAL_ATTACK:
            print("TODO")
        case ENCOUNTER_MOVES.ATTACK:
            print("TODO")
        case ENCOUNTER_MOVES.RUN:
            print("TODO")
        case ENCOUNTER_MOVES.MATE:
            print("TODO")

enviroment = Environment(80, 50, 1000)
def main():
    #are there animals in ecosystem?

    #if no generate batch of random mons

    #run simulation
    global ALL_PLANTS
    global SPACE_TAKEN
    global ALL_MONS

    
    ALL_PLANTS = [random_plant() for  i in range(5)]
    total_turns = 0
    while True:
        try:
            turns = input("turns: ")
            if turns == "q":
                break
        except:
            print("put in a int")

        
        for i in range(int(turns)):
            total_turns += 1


            print(f"__TURN: {total_turns}__")
            j = 0
            print(f"Space taken = {SPACE_TAKEN}")
            for plant in ALL_PLANTS:
                j += 1
                print()
                print(f"__plant: {j}__")
                plant_turn(plant)
                print("HP " + str(plant.stats[STATS.HP]) + ":(" + str(plant.stats[STATS.HP] - plant.buffs[STATS.HP]) + ") " +
                    "D: " + str(plant.stats[STATS.D]) + " " + "SD: " + str(plant.stats[STATS.SD]) + " " + "element: " + str(plant.element.value[0]))
                print()

            if len(ALL_MONS) < 1:
                ALL_MONS = [random_mon() for i in range(10)]
            k = 0
            for mon in ALL_MONS:
                k += 1
                print()
                print(f"__mon: {k}__")
                process_network(mon.brain['basic'], mon, None)
                print("element: " + str(mon.element.value[0]) + " HP " + str(mon.stats[STATS.HP]) + ":(" + str(mon.stats[STATS.HP] - mon.buffs[STATS.HP]) + ") " +
                    "D: " + str(mon.stats[STATS.D]) + " " + "SD: " + str(mon.stats[STATS.SD]) + " " + "A: " + str(mon.stats[STATS.A]) + " " +
                    "SA: " + str(mon.stats[STATS.SA]) + " " + "S: " + str(mon.stats[STATS.S]) + " E " + str(calculate_size(mon)) + 
                    ":(" + str(calculate_size(mon) - mon.energy) + ") ")
                big_d = mon.basic_moves | mon.encounter_moves
                for key in big_d:
                    print(str(key.value) + " P: " + str(big_d[key]))

                print()



            #for mon in ALL_MONS:





    """""""""
    mons = [random_mon() for i in range(10)]

    for mon in mons:
        action = process_network(mon.brain['basic'], mon, mon)
        make_move(action, mon, None)
    """""""""


main()


# stats are the basic numbers while traits give bonuses to certain skills ie walking vs swimming

#traits walking stat