import copy
import random 
from enum import Enum

import sys
import gc



################Classes##############

class STATS(Enum):
    HP = "HP"
    A = "A"
    SA = "SA"
    D = "D"
    SD = "SD"
    S = "S"
    CON = "CON"

class ELEMENTS(Enum):
    NORMAL = {"element": "Normal", "strong": [], "weak": []}
    FIRE = {"element": "Fire", "strong": ["Plant"], "weak": ["Water"]}
    WATER = {"element": "Water", "strong": ["Fire"], "weak": ["Plant"]}
    PLANT = {"element": "Plant", "strong": ["Water"], "weak": ["Fire"]}
    HOLY = {"element": "Holy", "strong": ["Demonic"], "weak": ["Demonic"]}
    DEMONIC = {"element": "Demonic", "strong": ["Holy"], "weak": ["Holy"]}
    LIGHTNING = {"element": "Lightning", "strong": ["Air"], "weak": ["Earth"]}
    EARTH = {"element": "Earth", "strong": ["Lightning"], "weak": ["Air"]}
    AIR = {"element": "Air", "strong": ["Earth"], "weak": ["lightning"]}

class TRAITS(Enum):
    HERBAVOR = "Herbavor"
    CARNIVOR = "Carnivor"

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
    OTHER_ANIMAL = "OTHER IS ANIMAL"
    OTHER_PLANT = "OTHER IS PLANT"
    OTHER_REMAINS = "OTHER REMAINS"
    
class BASIC_MOVES(Enum):
    REST = "Rest"
    SEARCH_PLANT = "Search plant"
    SEARCH_ANIMAL = "Search animal"
    SEARCH_MATE = "Search mate"
    SEARCH_REMAINS = "Seach remains" 

class ENCOUNTER_MOVES(Enum):
    SPECIAL_ATTACK = "Special attack"
    ATTACK = "Attack"
    RUN = "Run"
    MATE = "Mate"

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
    def __init__(self, stats, buffs, max_level, max_age, traits, encounter_moves, basic_moves, brain):
        self.stats = stats
        self.buffs = buffs
        self.max_level = max_level
        self.level = 1
        self.max_age = max_age
        self.age = 0
        self.traits = traits
        self.encounter_moves = encounter_moves
        self.basic_moves = basic_moves
        self.brain = brain
        self.energy = 0
        self.exp = 0
        self.child = None
        self.turns_carried = 0

class Plant():
    def __init__(self, stats, traits, buffs, max_age, max_level):
        self.stats = stats
        self.stats[STATS.CON] = 0
        self.traits = traits
        self.buffs = buffs
        self.max_age = max_age
        self.age = self.exp = 0
        self.level = 1
        self.max_level = max_level

class Remains():
    def __init__(self, stats, traits, buffs, level):
        self.stats = stats
        self.traits = traits
        self.buffs = buffs
        self.stats[STATS.CON] = 0
        self.level = level
        self.exp = 0
        self.age = 0
        self.max_age = 8

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
DIST_BETWEEN_SPECIES = 50

ECO = []
NEW_OBJs = []
######Main ####

def main():
    global ECO, NEW_OBJs
    total_turns = turns = 0
    while True:
        if total_turns == 0:
            randmons = [random_mon() for _ in range(4)]
            ECO = [copy.deepcopy(mon) for mon in randmons for _ in range(10)]
            ECO += [random_plant() for _ in range(50)]
            s = ''
        debug_memory_usage()
        if turns > 200:
            turns = input(f"{s} turns ({total_turns}): ")
            if turns == "q":
                    break
            try:
                    turns = int(turns)
            except ValueError:
                print("input number!")
                turns = 0
        else:
            turns = 1
        
        for _ in range(turns):
            total_turns += 1

            print(f"\n__TURN: {total_turns}__")
            i = 0
            print(f"Space taken = {SPACE_TAKEN}")
            for idx, obj in enumerate(ECO):
                if obj == None:
                    continue
                i += 1
                obj = obj_death(obj)
                if isinstance(obj, Plant):
                    print(f"__plant: {i}__")
                    print_obj(obj)
                    obj = plant_turn(obj)
                elif isinstance(obj, Remains):
                    print(f"__Remains: {i}__")
                    print_obj(obj)
                    obj = remains_turn(obj)
                elif isinstance(obj, Mon):
                    print(f"__mon: {i}__")
                    print_obj(obj)
                    obj = monturn(obj)
                print()

                obj = end_turn(obj)
                ECO[idx] = obj


            ECO += NEW_OBJs
            ECO, NEW_OBJs = [obj for obj in ECO if obj is not None], []

            mons = sum(1 for obj in ECO if isinstance(obj, Mon))
            plants = sum(1 for obj in ECO if isinstance(obj, Plant))
            remains = sum(1 for obj in ECO if isinstance(obj, Remains))
            s = f'Mons:{mons} Plants:{plants} Remains:{remains}'
            if 0 in (mons, plants):
                print(f"ecosystem collapsed at turn: {total_turns} {s}")
                total_turns = 0
                break


def plant_turn(plant: Plant) -> Plant:
    global NEW_OBJs
    global SPACE_TAKEN
    

    plant.age = plant.age + 1

    regen = get_encstat(STATS.HP, plant) // 8

    if plant.buffs[STATS.HP] > 0:
        plant.buffs[STATS.HP] -= regen
    
    if plant.buffs[STATS.HP] < 0:
        plant.buffs[STATS.HP] = 0

    if SPACE_TAKEN < TOTAL_SPACE:
        plant = gain_exp(plant, 10)
        new_plant = spawn_plant(plant)
        ns = 0
        for stat in new_plant.stats:
            ns += new_plant.stats[stat]

        SPACE_TAKEN += ns
        NEW_OBJs.append(new_plant)
        

    if get_encstat(STATS.HP, plant) <= plant.buffs[STATS.HP]:
        return None

    return plant


def remains_turn(remains: Remains) -> Remains:
    return remains


def monturn(mon: Mon) -> Mon:
    global ECO
    mon.age += 1
    
    action =  process_network(mon.brain['basic'], mon, None)
    print(f"Mon chose to {action.value}")
    mon, other = make_move(action, mon, None)
    if other == None:
        return mon
    
    oth_idx = -1
    for idx, obj in enumerate(ECO):
        if obj is other:
            oth_idx = idx

    mon, other = run_encounter(mon, other)
    ECO[oth_idx] = other 
    return mon


def run_encounter(actor, recp):
    for guy in [actor, recp]:
        guy.buffs[STATS.CON] = 0
    print("encounter started")
    
    max_encounter_turns = 10
    for _ in range(max_encounter_turns): 

        enc_fin = False
        for a, r in [(actor, recp),(recp, actor)]:
            if r == None:
                    print("other object has been destroyed")
                    enc_fin = True
                    break

            if isinstance(a, Mon):
                action = process_network(a.brain['encounter'], a, r)
                print(f"{a} Chose to {action}")
                na, nr = make_move(action, a, r)
                
                if (a, r) == (actor, recp):
                    actor, recp = na, nr
                else:  # (a, r) == (recp, actor)
                    recp, actor = na, nr
                if ran_away(r) and action == ENCOUNTER_MOVES.RUN:
                    print("Ran away")
                    enc_fin = True

            

            if enc_fin:
                break
        if enc_fin:
            break

    return actor, recp


#CLEAN TODO  ####################### INIT SIM  ###################################

def random_plant():
    value = []
    buff = []
    for stats in all_stats:
        value.append(random.randrange(100, 400))
        buff.append(0)

    stats = dict(zip(all_stats, value))
    element = all_elements[random.randrange(0, len(all_elements))]
    buffs = dict(zip(all_stats, buff))
    stats[STATS.CON] = 0

    max_age = random.randrange(400, 1000)
    max_level = random.randrange(10, 200)

    return Plant(stats, {element: 50}, buffs, max_age, max_level)


def random_mon():

    stat_val = []
    for stat in all_stats:
        stat_val.append(random.randrange(1, 100))

    ran_stats = dict(zip(all_stats, stat_val))

    buffs = dict.fromkeys(all_stats, 0)

    level = random.randrange(1, 10)
    age = random.randrange(50, 100)
    ran_element = all_elements[random.randrange(0, len(all_elements))]

    rand_traits = rand_list(all_traits)
    rand_traits.append(ran_element)
    trait_val = []
    for trait in rand_traits:
        trait_val.append(random.randrange(1, 100))
    traits = dict(zip(rand_traits, trait_val))

    # rand_encounter_m = rand_dict(all_encounter_moves)
    rand_encounter_m = rand_dict([ENCOUNTER_MOVES.MATE, ENCOUNTER_MOVES.ATTACK], all_encounter_moves)


    rand_basic_moves = rand_dict([BASIC_MOVES.SEARCH_MATE, BASIC_MOVES.SEARCH_PLANT], all_basic_moves)

    # generate random brain
    temp = [BASIC_INPUTS.SELF_HPB, BASIC_INPUTS.SELF_ENERGYB, BASIC_INPUTS.RANDOM, BASIC_INPUTS.RANDOM]
    # basic_inputs = rand_neurons(rand_list(all_basic_inputs))

    basic_inputs = rand_neurons(temp)
    # encounter_inputs = rand_neurons(rand_list(all_encounter_inputs) + rand_list(all_basic_inputs))
    other_temp = [ENCOUNTER_INPUTS.SIMILAR_SPECIES, ENCOUNTER_INPUTS.OTHER_PLANT]
    both_tmp = other_temp + temp
    encounter_inputs = rand_neurons(both_tmp)
    basic_hidden = rand_neurons([])
    encounter_hidden = rand_neurons([])

    basic_outputs = rand_neurons(list([key for key in rand_basic_moves]))
    encounter_outputs = rand_neurons(list([key for key in  rand_encounter_m]))

    brain = {
        "basic": Neural_Network(basic_inputs, basic_hidden, basic_outputs)  ,
        "encounter": Neural_Network(encounter_inputs, encounter_hidden, encounter_outputs)
    }

    return Mon(ran_stats, buffs, level, age, traits, rand_encounter_m, 
               rand_basic_moves, brain)


def rand_dict(keys, all_keys):
    

    for i in range(random.randrange(0, len(all_keys) - len(keys))):
        foo = random.randrange(0, len(all_keys))
        if all_keys[foo] not in keys:
            keys.append(all_keys[foo])
    value = []
    for key in keys:
        value.append(random.randrange(1, 100))
    return dict(zip(keys, value))


def rand_list(all_keys):

    l = []
    for i in range(random.randrange(1, len(all_keys) + 1)):
        trait = all_keys[random.randrange(0, len(all_keys))]
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
        bias = random.randrange(-3, 3)
        func = all_funcions[random.randrange(0, len(all_funcions))]

        n = Neuron(v, input, thresh, output, axons, bias, func)
        l.append(n)
    return l


#CLEAN TODO   ######################Neural Network##########################################


def process_network(network, mon, other_mon): 
    for neuron in network.inputs + network.hiddens + network.outputs:
        neuron.output = 0
        neuron.input_value = 0


    for neuron in network.inputs:
        neuron.input_value = get_input(neuron.action, mon, other_mon)
    for section in [network.inputs, network.hiddens, network.outputs]:
        next_sec = network.hiddens
        if section == network.hiddens:
            next_sec = network.outputs
        elif section == network.outputs:
            next_sec = None
        
        for neuron in section:
            if neuron.input_value >= neuron.threshold:
                out = get_neuron_function(neuron.input_value, neuron.bias, neuron.afunction)
                for axon in neuron.axons:
                    if  next_sec != None and axon < len(next_sec):
                        
                        next_sec[axon].input_value += int(out)
                        
                    if next_sec == None:
                        neuron.output = int(out)

    highest = network.outputs[0]
    for neuron in network.outputs:
        if neuron.output > highest.output:
            highest = neuron
    return highest.action


def get_neuron_function(input, bias, func):
    
    match func:
        case NEURON_FUNCTIONS.MULT:
            return (input + bias) # was *
        case NEURON_FUNCTIONS.ADD:
            return (input + bias)
        case NEURON_FUNCTIONS.DIVIDE:
            if bias == 0:
                bias = 1
            return (input - bias) # was /
        case NEURON_FUNCTIONS.SUBTRACT:
            return (input - bias)
        case _:
            print("failed path to neuron function")
            return 0


def get_input(request, mon, obj):
    match request:
        case BASIC_INPUTS.RANDOM:
            return random.randrange(-100, 100)
        case BASIC_INPUTS.SELF_HP:
            return get_encstat(STATS.HP, mon)
        case BASIC_INPUTS.SELF_ENERGY:
            return calculate_size(mon, mon.level)
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
            return mon.buffs[STATS.HP]
        case BASIC_INPUTS.SELF_ENERGYB:
            return mon.energy
        case BASIC_INPUTS.SELF_ATTACKB:
            return mon.buffs[STATS.A]
        case BASIC_INPUTS.SELF_SAB:
            return mon.buffs[STATS.SA]
        case BASIC_INPUTS.SELF_DEFENSEB:
            return mon.buffs[STATS.D]
        case BASIC_INPUTS.SELF_SDB:
            return mon.buffs[STATS.SD]
        case BASIC_INPUTS.SELF_SPEEDB:
            return mon.buffs[STATS.S]
        case BASIC_INPUTS.SELF_LEVEL:
            return mon.level
        case ENCOUNTER_INPUTS.OTHER_HP:
            return get_encstat(STATS.HP, obj)

        case ENCOUNTER_INPUTS.OTHER_ENERGY:
            return calculate_size(obj, obj.level)
        case ENCOUNTER_INPUTS.OTHER_ATTACK:
            return get_encstat(STATS.A, obj)
        case ENCOUNTER_INPUTS.OTHER_SA:
            return get_encstat(STATS.SA, obj)
        case ENCOUNTER_INPUTS.OTHER_DEFENSE:
            return get_encstat(STATS.D, obj)
        case ENCOUNTER_INPUTS.OTHER_SD:
            return get_encstat(STATS.SD, obj)
        case ENCOUNTER_INPUTS.OTHER_SPEED:
            return get_encstat(STATS.S, obj)
        case ENCOUNTER_INPUTS.OTHER_HPB:
            return mon.buffs[STATS.HP]
        case ENCOUNTER_INPUTS.OTHER_ENERGYB:
            if not isinstance(obj, Mon):
                return 0
            else:
                return obj.energy
        case ENCOUNTER_INPUTS.OTHER_ATTACKB:
            return mon.buffs[STATS.A]
        case ENCOUNTER_INPUTS.OTHER_SAB:
            return mon.buffs[STATS.SA]
        case ENCOUNTER_INPUTS.OTHER_DEFENSEB:
            return mon.buffs[STATS.D]
        case ENCOUNTER_INPUTS.OTHER_SDB:
            return mon.buffs[STATS.SD]
        case ENCOUNTER_INPUTS.OTHER_SPEEDB:
            return mon.buffs[STATS.S]
        case ENCOUNTER_INPUTS.OTHER_LEVEL:
            if isinstance(obj, Mon):
                return obj.level
            return 0
        case ENCOUNTER_INPUTS.SIMILAR_SPECIES:
            if isinstance(obj, Mon) and compare_species(mon, obj) < DIST_BETWEEN_SPECIES:
                return 100
            else:
                return 0
        case ENCOUNTER_INPUTS.OTHER_ANIMAL:
            if isinstance(obj, Mon):
                return 100
            else:
                return 0
        case ENCOUNTER_INPUTS.OTHER_PLANT:
            if isinstance(obj, Plant):
                return 100
            else:
                return 0
        case ENCOUNTER_INPUTS.OTHER_REMAINS:
            if isinstance(obj, Remains):
                return 100
            else:
                return 0
        case _:
            print("neuron input request/path not found")
            return 0


def make_move(action, mon, other):
    match action:
        case BASIC_MOVES.REST:
            return rest(mon)
        case BASIC_MOVES.SEARCH_PLANT:
            return search(mon, Plant, 'not mate')
        case BASIC_MOVES.SEARCH_ANIMAL:
            return search(mon, Mon, 'not mate')
        case BASIC_MOVES.SEARCH_MATE:
            return search(mon, Mon, 'mate')
        case BASIC_MOVES.SEARCH_REMAINS:
            return search(mon, Remains, 'not mate')


        case ENCOUNTER_MOVES.SPECIAL_ATTACK:
            return combat_move(action, mon, other)
        case ENCOUNTER_MOVES.ATTACK:
            return combat_move(action, mon, other)
        case ENCOUNTER_MOVES.RUN:
            return combat_move(action, mon, other)
        case ENCOUNTER_MOVES.MATE:
            return mate(mon, other)
  


#CLEAN TODO    ##########Helper functions#########################

def get_encstat(stat, obj):
    lv = obj.level
         
    d = calculate_stats(obj, lv, "stats")
    if stat == STATS.HP or stat == STATS.CON:
        d[stat] *= 4
    return d[stat]


def calculate_stats(obj, monlv, flag):

    lv = monlv / 100
   
   
    if flag == "stats":
        d = obj.stats

    elif flag == "e moves" and isinstance(obj, Mon):
        d = obj.encounter_moves
    elif isinstance(obj, Mon):
        d = obj.basic_moves
    else:
        d = {}
    dic = {key: max(1, int(lv * d[key])) for key in d}
    if STATS.CON in dic.keys() and (isinstance(obj, Plant) or isinstance(obj, Remains)):
        dic[STATS.CON] = 0
    return dic


def calculate_size(obj, monlv):
    size = 0
    flag = "stats"
    for i in range(3):
        if i == 1:
            flag = "e moves"
        elif i == 2:
            flag = ""
        d = calculate_stats(obj, monlv, flag)
        size += sum(list(d.values()))

    if not isinstance(obj, Mon):
        return size

    network = obj.brain['basic']
    for i in range(2):
        if i == 1:
            network = obj.brain['encounter']
        network_section = network.inputs
        for i in range(3):
            if i == 1:
                network_section = network.hiddens
            elif i == 2:
                network_section = network.outputs
            for neuron in network_section:
                size += 1
    return size


def coinflip(heads, tales):
    coin = random.randrange(0,2)

    result = heads
    if coin == 0:
        result = heads
    else:
        result = tales
    return result


def compare_species(mon, other_mon):

    if not isinstance(other_mon, Mon) and other_mon != None:
        return 100
    
    dif = 0
    # compare base_stats
    for stat in all_stats:
        dif += abs(mon.stats[stat] - other_mon.stats[stat])

    


    for moves in ['basic_moves', 'encounter_moves']:
        m_mov = getattr(mon, moves)
        o_mov = getattr(other_mon, moves)

        if len(o_mov) > len(m_mov):
            o_mov = getattr(mon, moves)
            m_mov = getattr(other_mon, moves)
        
        for move in m_mov:
            if move not in o_mov:
                dif += 10
            else:
                dif += abs(m_mov[move] - o_mov[move])
        dif += abs(len(m_mov) - len(o_mov))


    # compare traits
    for trait in mon.traits:
        if trait not in other_mon.traits:
            dif += 10
        else:
            dif += abs(mon.traits[trait] - other_mon.traits[trait])
    for trait in other_mon.traits:
        if trait not in mon.traits:
            dif += 10


    # brain comp
    for key in ['encounter', 'basic']:
        for layer in ['inputs', 'hiddens', 'outputs']:
            
            l = getattr(mon.brain[key], layer)
            ol = getattr(other_mon.brain[key], layer)
            
            dif += abs(len(l) - len(ol))
            
            j = min(len(l), len(ol))
            for i in range(j):
                if l[i].action != ol[i].action:
                    dif += 1
    # print(f"dif: {dif}")
    return dif


def get_element(obj):
    for trait in obj.traits:
            if isinstance(trait, ELEMENTS):
                return trait
    return ELEMENTS.NORMAL

#CLEAN TODO############################BASIC MOVES#######################################

   
def rest(mon):
    if mon.buffs[STATS.HP] > 0:
        mon.buffs[STATS.HP] = max(mon.buffs[STATS.HP] - (calculate_size(mon, mon.level) // 8), 0)
    if mon.buffs[STATS.CON] > 0:
        mon.buffs[STATS.CON] = max(mon.buffs[STATS.CON] - (calculate_size(mon, mon.level) // 8), 0)
    return mon, None


def search(mon, cls, flag):
    global ECO

    partner = False
    if flag == 'mate':
        partner = True

    
    for i in range(len(ECO)):
        i = random.randrange(0, len(ECO))
        if isinstance(ECO[i], cls) and (compare_species(mon, ECO[i]) and partner) <  DIST_BETWEEN_SPECIES and ECO[i] is not mon:
            print(f"found {ECO[i]}")
            return mon, ECO[i]
    print("could not find")
    return mon, None


def spawn_plant(parent: Plant) -> Plant:
    values = []
    buffv = []
    for stat in parent.stats:
        value = parent.stats[stat] + mutate_val()
        buffv.append(0)
        if value < 1:
            value = 1
        values.append(value)

    stats = dict(zip(all_stats, values))
    buffs = {stat: 0 for stat in all_stats}

    element = ELEMENTS.NORMAL
    for trait in parent.traits:
        if isinstance(trait, ELEMENTS):
            element = trait
    if random.randrange(0, 1000) < 3:
        if element != ELEMENTS.NORMAL:
            element = ELEMENTS.NORMAL
        else:
            element = all_elements[random.randrange(0, len(all_elements))]
    stats[STATS.CON] = 0

    max_level = parent.max_level + mutate_val()
    max_age = parent.max_age + mutate_val()
    
    return Plant(stats, {element: 50}, buffs, max_age, max_level)

    


#CLEAN TODO###########################ENCOUNTER MOVES########################################

def combat_move(action, mon, obj):

    mon_el, obj_el = get_element(mon), get_element(obj)
    
    if mon_el.value['element'] in mon_el.value['weak']:
        mod = 2
    elif  obj_el.value['element'] in obj_el.value['strong']:
        mod = .5
    else:
        mod = 1

    act_map = {ENCOUNTER_MOVES.ATTACK: (STATS.A, STATS.D, STATS.HP), 
               ENCOUNTER_MOVES.SPECIAL_ATTACK: (STATS.SA, STATS.SD, STATS.HP), 
               ENCOUNTER_MOVES.RUN: (STATS.S, STATS.S, STATS.CON)}

    act_a, act_d, hit_points = act_map[action]
    attack, defence = get_encstat(act_a, mon), get_encstat(act_d, obj)
   
    moves = calculate_stats(mon, mon.level, 'e moves')
    power =  moves[action]

    dmg = min(max((attack * power * mod) // defence, 1), 
            abs(get_encstat(hit_points, obj) - obj.buffs[hit_points]))
    obj.buffs[hit_points] += dmg
    print_dmg(mon, obj, action, hit_points, power, dmg)

    mon = took_bite(mon, obj, hit_points, dmg)        
    obj = obj_death(obj)
    
    return mon, obj 


def mate(parent_a, parent_b):

    if not isinstance(parent_b, Mon):
        print("tried to mate a non animal")
        return parent_a, parent_b
    elif  isinstance(parent_a.child, Mon):
        print("mon was already carrying a child")
        return parent_a, parent_b
    elif process_network(parent_b.brain['encounter'], parent_b, parent_a) != ENCOUNTER_MOVES.MATE:
        print("other did not consent")
        return parent_a, parent_b
    elif compare_species(parent_a, parent_b) < DIST_BETWEEN_SPECIES:
        print("offspring not viable")
    

    buff_values = []
    buff_keys = []
    for stat in all_stats:
        buff_keys.append(stat)
        buff_values.append(0)
    buffs = dict(zip(buff_keys, buff_values))

    stats = copy.deepcopy(buffs)
    
    for stat in all_stats:
        parent = coinflip(parent_a, parent_b)
        stats[stat] = max(parent.stats[stat] + mutate_val(), 1)

    parent = coinflip(parent_a, parent_b)
    max_level = max(parent.max_level + mutate_val(), 1)

    parent = coinflip(parent_a, parent_b)
    max_age = max(parent.max_age + mutate_val(), 1)
    

    traits = {}
    b_moves = {}
    e_moves = {}
    for attr in ['traits', 'encounter_moves', 'basic_moves']:
        t = []
        v = []
        parent = coinflip(parent_a, parent_b)
        other_parent = parent_a
        if parent == parent_a:
            other_parent = parent_b
        parent_attr = getattr(parent, attr)
        other_pattr = getattr(other_parent, attr)
        for item in parent_attr:
            if item in other_pattr:

                t.append(item)
                win = coinflip(parent_a, parent_b)
                parent_items = getattr(win, attr)
                v.append(parent_items[item])
            else:
                win = coinflip(parent_a, parent_b)
                parent_items = getattr(win, attr)
                if win == parent:
                    t.append(item)
                    v.append(parent_items[item])

        items = dict(zip(t, v))

        if not items:
            print("DEBUG: items went empty for", attr, parent_a, parent_b)
            return parent_a, parent_b
        for item in items:
            items[item] = max(items[item] + mutate_val(), 1)
        item = random.choice(list(items))
        if isinstance(item, ELEMENTS) and mutate_trait(items[item]):
            if item != ELEMENTS.NORMAL:
                items[ELEMENTS.NORMAL] = items.pop(item)
            else:
                items[all_elements[random.randrange(0, len(all_elements))]] = items.pop(item)
            
        elif not isinstance(item, ELEMENTS) and mutate_trait(items[item]): 
            if coinflip(0, 1) == 0:
                all_list = all_traits
                if attr == 'traits':
                    all_list = all_traits
                elif attr == 'encounter_moves':
                    all_list = all_encounter_moves
                else:
                    all_list = all_basic_moves            
                items[all_list[random.randrange(0, len(all_list))]] = 1
            else:
                if not len(items) > 2:
                    items.pop(item) 

        all_list = all_traits
        if attr == 'traits':
            traits = items
        elif attr == 'encounter_moves':
            e_moves = items
        else:
            b_moves = items


    brain = copy.deepcopy(parent_a.brain)
    

    for net in ['basic', 'encounter']:
        for section in ['hiddens', 'outputs', 'inputs']:
            neurons = getattr(brain[net], section)
            for neuron in neurons:
                b_neurons = getattr(parent_b.brain[net], section)
                if 1 == coinflip(0, 1):
                    idx = neurons.index(neuron)
                    if idx <= len(b_neurons) and idx > len(b_neurons):
                        neurons[idx] = b_neurons[idx]
                
                # finished inheritance now mutate 
                for nur_attr in ['threshold', 'axons', 'bias']:
                    ru_val = getattr(neuron, nur_attr)
                    if nur_attr == 'axons':
                        for axon in ru_val:
                            axon += max(mutate_val() + axon, 0)
                    else:
                        ru_val += mutate_val()
                        
            if mutate_trait(0):
                neuron.afunction = all_funcions[random.randrange(0, len(all_funcions))]

            if section == 'inputs' and mutate_trait(0):
                if net == 'basic':
                    neuron.action == all_basic_inputs[random.randrange(0, len(all_basic_inputs))]
                else:
                    all_ins = all_basic_inputs + all_encounter_inputs
                    neuron.action = all_ins[random.randrange(0, len(all_ins))]
    
    for net in ['basic', 'encounter']:
        moves = b_moves
        if net == 'encounter':
            moves = e_moves
        for move in moves:
            found = False
            for neuron in brain[net].outputs:
                if move == neuron.action:
                    found = True
                    break

            if not found:
                input = 0
                thresh = random.randrange(-10, 10)
                output = 0
                axons = []
                bias = random.randrange(-3, 3)
                func = all_funcions[random.randrange(0, len(all_funcions))]
                brain[net].outputs.append(Neuron(move, input, thresh, output, axons, bias, func))

        for neuron in brain[net].outputs:
            if neuron.action not in moves:
                neuron.action = random.choice(list(moves.keys()))

    for net in ['basic', 'encounter']:
        for section in ['hiddens', 'inputs']:
            neurons = getattr(brain[net], section)
            for neuron in neurons:
                if mutate_trait(0):
                    if coinflip(0, 1) == 1:
                        input = 0
                        thresh = random.randrange(-10, 10)
                        output = 0
                        axons = [random.randrange(0, len(neurons))]
                        bias = random.randrange(-3, 3)
                        func = all_funcions[random.randrange(0, len(all_funcions))]
                        v = "hidden"

                        if section == 'inputs':
                            if net == 'basic':
                                v = all_basic_inputs[random.randrange(0, len(all_basic_inputs))]
                            else:
                                all_in = all_encounter_inputs + all_basic_inputs
                                v  = all_in[random.randrange(0, len(all_in))]
                        neurons.append(Neuron(v, input, thresh, output, axons, bias, func))
                    else:
                        if len(neurons) > 1:
                            neurons.pop()                
                elif mutate_trait(0):
                    if coinflip(0, 1) == 1:
                        neuron.axons.append(random.randrange(0, 5))
                    else:
                        if len(neuron.axons) > 1:
                            neuron.axons.pop()
                        
    new_mon = Mon(stats, buffs, max_level, max_age, traits, e_moves, b_moves, brain)

    parent_a.child = new_mon
    parent_a.turns_carried = 0
    print("mons mated")
    return parent_a, parent_b

def mutate_val():
    if random.randrange(0, 100) < 3:
        return random.randrange(-1,2)
    return 0

def mutate_trait(val):
    if random.randrange(0, 1000) < 3 and val < 11:
        return True
    return False

def ran_away(mon):
    if not isinstance(mon, Mon) or get_encstat(STATS.CON, mon) <= mon.buffs[STATS.CON]:
        return True
    return False

def gain_exp(obj, exp):
    obj.exp += exp
    if obj.exp > obj.level * 10 and obj.level < obj.max_level:
        obj.level += 1
        obj.exp = 0
    return obj

def took_bite(perp, target, hit_points, dmg):
    if hit_points == STATS.HP and ((isinstance(target, Plant) and TRAITS.HERBAVOR in perp.traits)
                                    or (isinstance(target, Remains) and TRAITS.CARNIVOR in perp.traits)) :
        perp = gain_exp(perp, 10)
        perp.energy = max(perp.energy - dmg, 0)
    return perp

#CLEAN TODO     ##################Process end of turn##################

def obj_death(obj):
    s = ''
    if get_encstat(STATS.HP, obj) <= obj.buffs[STATS.HP]:
        s += 'was attacked'
    if obj.age >= obj.max_age:
        if s != '':
            s += ', it '
        s += 'was old'
    if isinstance(obj, Mon) and calculate_size(obj, obj.level) - obj.energy  <= 0:
        if s != '':
            s += ', it '
        s += 'was hungry'
    if s == '':
        return obj

    global SPACE_TAKEN

    if isinstance(obj, Plant):
        SPACE_TAKEN = max(SPACE_TAKEN - calculate_size(obj, obj.level), 0)
    if not isinstance(obj, Mon):
        for cls, old, dmg in [(Remains, "corpse rotted away", "the last scraps were eaten"), 
                              (Plant, "plant grew dry and barren and withered away", "plant was completely consumed")]:
            if isinstance(obj, cls):
                if 'was old' in s:
                    print(old)
                    return None
                else:
                   print(dmg)
                   return None
        return None
    else:
        print(f"animal died it {s}.")
        stats = copy.deepcopy(obj.stats)
        traits = copy.deepcopy(obj.traits)
        buffs = {key: 0 for key in stats}
        return Remains(stats, traits, buffs, obj.level)


def end_turn(obj):
    if obj == None:
        return None
    global ECO
    obj.age += 1
    if  isinstance(obj, Mon):
        obj.energy += max(calculate_size(obj, obj.level) // 30, 1)
        if isinstance(obj.child, Mon):
            obj.energy += max(calculate_size(obj.child, 1) // 8, 1)
            obj.turns_carried += 1
            if isinstance(obj.child, Mon) and obj.turns_carried >= 16:
                NEW_OBJs.append(obj.child)
                obj.child, obj.turns_carried = None, 0
    obj = obj_death(obj)
    return obj


##CLEAN TODO#################PRINT TO TERM##############################

def print_obj(obj):
    s = ""
    s += f"Level: {obj.level}(exp: {obj.exp}) Age:{obj.age} Clade: #TODO\n"

    for trait in obj.traits:
        
        if isinstance(trait, ELEMENTS):
            s += f"type {trait.value['element']}"
        else:
            s += f"{trait.value}"
        s += f": {obj.traits[trait]}, "
    s += "\n"

    print(obj.stats)
    for stat in obj.stats:
        s += f"{stat.value}: "
        if stat == STATS.HP:
            hp = get_encstat(STATS.HP, obj)
            s += f"({hp}){hp - obj.buffs[STATS.HP]} "
        else:
            s += f"{get_encstat(stat, obj)} "
    s += "\n"

    if isinstance(obj, Mon):
        s += f"Energy: {calculate_size(obj, obj.level)}({calculate_size(obj, obj.level) - obj.energy})"
        for moves in [obj.basic_moves, obj.encounter_moves]:
            for move in moves:
                s += f"{move.value}: "
                s += f"{moves[move]} "
                

        if obj.child != None:
            s += f"Child: {obj.child} carried: {obj.turns_carried}"
        s += "\n"

    print(s)


def print_brain(brain):
    print(brain)
    for net in ['encounter', 'basic']:
        for layer in ['inputs', 'hiddens', 'outputs']:
            neurons = getattr(brain[net], layer)
            for neuron in neurons:
                print(net + " " + layer)
                print(neuron.action)
                print(neuron.axons)
                print(neuron.threshold)
                print(neuron.afunction.value)
                print(neuron.bias)


def print_dmg(mon, obj, action, hit_points, power, dmg):
    print(f"{mon}: ", end='')
    print(f"mon {action.value}s with a power of {power} for {dmg} points", end=" ")
    print(f"Reducing target:{obj} {hit_points.value} to {get_encstat(hit_points, obj)}:({get_encstat(hit_points, obj) - obj.buffs[hit_points]}) ")




################# DEBUG ###################
def debug_memory_usage():
    """Track memory usage patterns using built-in tools only"""
    print("\n=== MEMORY USAGE DEBUG ===")
    
    # Python object counts
    all_objects = gc.get_objects()
    print(f"Total Python objects: {len(all_objects)}")
    
    # Count objects by type
    type_counts = {}
    total_size = 0
    
    for obj in all_objects:
        obj_type = type(obj).__name__
        type_counts[obj_type] = type_counts.get(obj_type, 0) + 1
        total_size += sys.getsizeof(obj)
    
    print(f"Approximate total size: {total_size / 1024 / 1024:.2f} MB")
    
    # Show counts for our custom objects
    custom_objects = ['Mon', 'Plant', 'Remains', 'Neuron', 'Neural_Network']
    print("Custom object counts:")
    for obj_type in custom_objects:
        count = type_counts.get(obj_type, 0)
        if count > 0:
            print(f"  {obj_type}: {count}")
    
    # Show top object types by count
    sorted_types = sorted(type_counts.items(), key=lambda x: x[1], reverse=True)
    print("Top 10 object types by count:")
    for obj_type, count in sorted_types[:10]:
        print(f"  {obj_type}: {count}")



main()

## NEW plan is to shrik and simplify