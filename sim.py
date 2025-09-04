import copy
import random 
from enum import Enum


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
    def __init__(self, stats, buffs, max_level, traits, encounter_moves, basic_moves, brain):
        self.stats = stats
        self.buffs = buffs
        self.max_level = max_level
        self.level = 1
        self.traits = traits
        self.encounter_moves = encounter_moves
        self.basic_moves = basic_moves
        self.brain = brain
        self.energy = 0
        self.exp = 0

class Plant():
    def __init__(self, stats, traits, buffs):
        self.stats = stats
        self.traits = traits
        self.buffs = buffs


class Remains():
    def __init__(self, stats, traits, buffs):
        self.stats = stats
        self.traits = traits
        self.buffs = buffs
        self.stats[STATS.CON] = 0
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
ALL_REMAINS = []

def random_plant():

    value = []
    buff = []
    for stats in all_stats:
        if stats != STATS.HP:
            value.append(random.randrange(1, 100))
        else:
            value.append(random.randrange(1, 100) * 4)
        buff.append(0)
    stats = dict(zip(all_stats, value))

    element = all_elements[random.randrange(0, len(all_elements))]

    buffs = dict(zip(all_stats, buff))

    stats[STATS.CON] = 0

    return Plant(stats, [element], buffs)


def plant_turn(plant):
    global SPACE_TAKEN
    global TOTAL_SPACE
    global ALL_PLANTS

    regen = plant.stats[STATS.HP] // 8

    if plant.buffs[STATS.HP] > 0:
        plant.buffs[STATS.HP] -= regen
    
    if plant.buffs[STATS.HP] < 0:
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

    element = parent.traits[0] 
    if random.randrange(0, 1000) < 3:
        if element != ELEMENTS.NORMAL:
            element = ELEMENTS.NORMAL
        else:
            element = all_encounter_moves[random.randrange(0, len(all_encounter_moves))]
    stats[STATS.CON] = 0
    return Plant(stats, [element], buffs)


def random_mon():

    stat_val = []
    for stat in all_stats:
        stat_val.append(random.randrange(1, 100))

    ran_stats = dict(zip(all_stats, stat_val))

    buffs = dict.fromkeys(all_stats, 0)

    level = random.randrange(1, 10)

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
    temp = [BASIC_INPUTS.RANDOM, BASIC_INPUTS.RANDOM, BASIC_INPUTS.RANDOM, BASIC_INPUTS.RANDOM]
    # basic_inputs = rand_neurons(rand_list(all_basic_inputs))

    basic_inputs = rand_neurons(temp)
    # encounter_inputs = rand_neurons(rand_list(all_encounter_inputs) + rand_list(all_basic_inputs))
    
    encounter_inputs = rand_neurons(temp)
    basic_hidden = rand_neurons([])
    encounter_hidden = rand_neurons([])

    basic_outputs = rand_neurons(list([key for key in rand_basic_moves]))
    encounter_outputs = rand_neurons(list([key for key in  rand_encounter_m]))

    brain = {
        "basic": Neural_Network(basic_inputs, basic_hidden, basic_outputs)  ,
        "encounter": Neural_Network(encounter_inputs, encounter_hidden, encounter_outputs)
    }

    return Mon(ran_stats, buffs, level, traits, rand_encounter_m, 
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


def process_network(network, mon, other_mon): 
    for neuron in network.inputs + network.hiddens + network.outputs:
        neuron.output = 0
        neuron.input_value = 0


    for neuron in network.inputs:
        neuron.input_value = get_input(neuron.action, mon, other_mon)
        # print(f"Acton({neuron.action}) in_value({neuron.input_value})")
    #print("____________________________________")  
    for section in [network.inputs, network.hiddens, network.outputs]:
        #print("------------------------------------------")
        #print(section)
        next_sec = network.hiddens
        if section == network.hiddens:
            next_sec = network.outputs
        elif section == network.outputs:
            next_sec = None
        
        for neuron in section:
            #print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
            #print(f"neuron axons: {neuron.axons}")
            if neuron.input_value >= neuron.threshold:
                out = get_neuron_function(neuron.input_value, neuron.bias, neuron.afunction)
                #print(f"neuron in {neuron.input_value} neron out:{out}")
                for axon in neuron.axons:
                    if  next_sec != None and axon < len(next_sec):
                        
                        next_sec[axon].input_value += int(out)
                        
                    if next_sec == None:
                        neuron.output = int(out)

    highest = network.outputs[0]
    for neuron in network.outputs:
        print(f"action: {neuron.action} out: {neuron.output}")
        if neuron.output > highest.output:
            highest = neuron
    return highest.action


def get_neuron_function(input, bias, func):
    #print(f"input: {input} bias: {bias} function: {func}")
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
            if not isinstance(other_mon, Mon):
                return 0
            return calculate_size(other_mon, other_mon.level)
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
            if not isinstance(other_mon, Mon):
                return 0
            else:
                return other_mon.energy
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
            if isinstance(other_mon, Mon):
                return other_mon.level
            return 1
        case ENCOUNTER_INPUTS.SIMILAR_SPECIES:
            return compare_species(mon, other_mon)
        case _:
            print("neuron input request/path not found")
            return 0


def get_encstat(stat, mon):
    lv = 100
    if isinstance(mon, Mon):
        lv = mon.level
        
    d = calculate_stats(mon, lv, "stats")
    if stat == STATS.HP or stat == STATS.CON:
        d[stat] *= 4
    return d[stat]


def get_buffs(stat, mon):
    buff = mon.buffs[stat]
    return buff


def calculate_stats(mon, monlv, flag):

    if not isinstance(mon, Mon):
        monlv = 100

    lv = monlv / 100
   
    stat_value = []
    if flag == "stats":
        d = mon.stats

    elif flag == "e moves":
        d = mon.encounter_moves
    else:
        d = mon.basic_moves
    for key in d:
        stat_value.append(max(1, int(lv * d[key])))
    return {key: max(1, int(lv * d[key])) for key in d}


def calculate_size(mon, monlv):
    size = 0
    flag = "stats"

    for i in range(3):
        if i == 1:
            flag = "e moves"
        elif i == 2:
            flag = ""
        d = calculate_stats(mon, monlv, flag)
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
            
    return dif


def make_move(action, mon, other):
    match action:
        case BASIC_MOVES.REST:
            return rest(mon)
        case BASIC_MOVES.SEARCH_PLANT:
            return search_plant()
        case BASIC_MOVES.SEARCH_ANIMAL:
            return search_animal(mon)
        case BASIC_MOVES.SEARCH_MATE:
            return search_mate(mon)
        case BASIC_MOVES.SEARCH_REMAINS:
            return search_remains()


        case ENCOUNTER_MOVES.SPECIAL_ATTACK:
            return combat_move(action, mon, other)
        case ENCOUNTER_MOVES.ATTACK:
            return combat_move(action, mon, other)
        case ENCOUNTER_MOVES.RUN:
            return combat_move(action, mon, other)
        case ENCOUNTER_MOVES.MATE:
            return mate(mon, other)
        
            


def rest(mon):
    if mon.buffs[STATS.HP] > 0:
        mon.buffs[STATS.HP] = max(mon.buffs[STATS.HP] - (calculate_size(mon, mon.level) // 8), 1)
    if mon.buffs[STATS.CON] > 0:
        mon.buffs[STATS.CON] = max(mon.buffs[STATS.CON] - (calculate_size(mon, mon.level) // 8), 1)
    return None

def search_plant():
    global ALL_PLANTS

    for i in range(0, len(ALL_PLANTS)): 
        i = random.randrange(0, len(ALL_PLANTS))
        if ALL_PLANTS[i] != None:
            return ALL_PLANTS[i]
    return None


def search_animal(mon):
    global ALL_MONS
    for i in range(0, len(ALL_MONS)): 
        i = random.randrange(0, len(ALL_MONS))
        if ALL_MONS[i] != mon and ALL_MONS[i] != None:
            return ALL_MONS[i]
    return None

def search_mate(mon):
    global ALL_MONS
    for i in range(len(ALL_MONS)):
        i = random.randrange(0, len(ALL_MONS))
        if ALL_MONS[i] != None and compare_species(mon, ALL_MONS[i]) <  max(calculate_size(mon, mon.level) // 5, 1) and ALL_MONS[i] != mon:
            print("found mon of similar species")
            return ALL_MONS[i]
    print("could not find mate")
    return None

def search_remains():
    global ALL_REMAINS
    for i in range(len(ALL_REMAINS)):
        i = random.randrange(0, len(ALL_REMAINS))
        if ALL_REMAINS[i] != None:
            return ALL_REMAINS[i]
    print("could not find remains")

def combat_move(action, mon, other):

    m_el = ELEMENTS.NORMAL
    o_el = ELEMENTS.NORMAL
    for comb in [mon, other]:
        traits = getattr(comb, 'traits')
        el = ELEMENTS.NORMAL
        for trait in traits:
            if isinstance(trait, ELEMENTS):
                el = trait
        if comb == mon:
            m_el = el
        else:
            o_el = el

    mod = 1
    if m_el.value['element'] in o_el.value['weak']:
        mod = 2
    elif  m_el.value['element'] in o_el.value['strong']:
        mod = .5

    # change to work with S SA and A
    hit_points = STATS.HP
    if action == ENCOUNTER_MOVES.ATTACK:
        attack = get_encstat(STATS.A, mon)
        defence = get_encstat(STATS.D, other)
    elif action == ENCOUNTER_MOVES.SPECIAL_ATTACK:
        attack = get_encstat(STATS.SA, mon)
        defence = get_encstat(STATS.SD, other)
    else:
        hit_points = STATS.CON
        attack = get_encstat(STATS.S, mon)
        defence = get_encstat(STATS.S, other)
    
    
    e_dict = calculate_stats(mon, mon.level, 'e moves')
    power =  e_dict[action]


    
    


    dmg = max((attack * power * mod) // defence, 1)
    # print(f"mon {action.value}s with a power of {power} for {dmg} points", end=" ")
    # print(f"Reducing targets {hit_points.value} from {get_encstat(hit_points, other)}:({get_encstat(hit_points, other) - other.buffs[hit_points]}) to", end=" ")
    other.buffs[hit_points] += dmg
    # print(get_encstat(hit_points, other) - other.buffs[hit_points])


    if not isinstance(other, Mon) and hit_points == STATS.HP:
        other_hp = get_encstat(hit_points, other) - other.buffs[hit_points]
        if  other_hp < 0:
            dmg += other_hp
        mon = took_bite(mon, other, dmg)

    if (isinstance(other, Plant) or isinstance(other, Remains)) and get_encstat(STATS.HP, other) - other.buffs[STATS.HP] <= 0:
        other = None
    if isinstance(other, Mon) and get_encstat(STATS.HP, other) - other.buffs[STATS.HP] <= 0:
        energy = other.energy + calculate_size(other, other.level)
        other.traits[STATS.HP] = energy
        other.buffs[STATS.HP] = 0
        remains = Remains(other.stats, other.traits, other.buffs)
        print("other should be remains")
        other = remains

    


    return [mon, other] 

def mate(mon, other):
    return [mon, other]
def main():
    #are there animals in ecosystem?

    #if no generate batch of random mons

    #run simulation
    global ALL_PLANTS
    global SPACE_TAKEN
    global ALL_MONS
    global ALL_REMAINS

    
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
                print()
                j += 1
                plant_turn(plant)
                
                print(f"__plant: {j}__")
                print_plant(plant)
                print()

            if len(ALL_MONS) < 1:
                copies = []
                ALL_MONS = [random_mon() for i in range(4)]
                for mon in ALL_MONS:
                    for j in range(4):
                        copies.append(copy.deepcopy(mon))
                ALL_MONS = ALL_MONS + copies
            k = 0
            for mon in ALL_MONS:
                mon_idx = ALL_MONS.index(mon)
                k += 1
                if isinstance(mon, Mon):
                
                    print()
                    print(f"__mon: {k}__")
                    print_mon(mon)
                    move =  process_network(mon.brain['basic'], mon, None)
                    other = make_move(move, mon, None)
                    
                if other != None and mon != None:
                    
                    oth_idx = 0
                    l = []
                    f = ""  
                    if isinstance(other, Plant):
                        oth_idx = ALL_PLANTS.index(other)
                        l = ALL_PLANTS
                    elif isinstance(other, Mon):
                        oth_idx = ALL_MONS.index(other)
                        f = "was mon"
                        l = ALL_MONS
                    elif isinstance(other, Remains):
                        oth_idx = ALL_REMAINS.index(other)
                        l = ALL_REMAINS
                    else:
                        print("other obj not found in any relevent list main()")
                    
                    after_enc = run_encounter(mon, other)
                    mon = after_enc[0] 
                    other = after_enc[1]

                    ALL_MONS[mon_idx] = mon
                    if isinstance(other, Plant):
                        l[oth_idx] = other
                    elif isinstance(other, Mon):
                        l[oth_idx] = other
                    elif isinstance(other, Remains):
                        if f == "was mon":
                            ALL_MONS[oth_idx] = None
                            ALL_REMAINS.append(other)
                        else:
                            l[oth_idx] = other
                    else:
                        print("error updating events in main")

                    
            for mon in ALL_MONS:
                if not isinstance(mon, Mon):
                    continue
                i = ALL_MONS.index(mon)
                mon = energy_drain(mon)
                if isinstance(mon, Mon):
                    ALL_MONS[i] = mon
                elif isinstance(mon, Remains):
                    ALL_MONS[i] = None
                    ALL_REMAINS.append(mon)
                else:
                    ALL_MONS[i] = None


            ALL_REMAINS = [remains for remains in ALL_REMAINS if isinstance(remains, Remains)]
            ALL_MONS = [mons for mons in ALL_MONS if isinstance(mons, Mon)]
            ALL_PLANTS = [plant for plant in ALL_PLANTS if isinstance(plant, Plant)]
            print()

        
        for obj in ALL_PLANTS + ALL_MONS + ALL_REMAINS:
            # print_guy(obj)
            pass


            

def run_encounter(actor, recp):
    for guy in [actor, recp]:
        guy.buffs[STATS.CON] = 0
    print("encounter started")
    re = False
    for t in range(10):
        i = 0 
        for a in [actor, recp]:
            # print_guy(a)

            if a == actor:
                r = recp
            else:
                r = actor
            #print(a)
            if not isinstance(a, Mon):
                continue
            action = process_network(a.brain['encounter'], a, r)
            print(f"Chose to {action}")
            a, r = make_move(action, a, r)
            if ran_away(r):
                print("Ran away")
                re = True
            elif all_gone(r):
                re = True
                r = None
                print("Was completly consumed")
                
            
            if i == 0:
                actor = a
                recp = r
            else:
                actor = r
                recp = a
            i += 1
            print()
            if re:
                return actor, recp
    return actor, recp

def print_guy(guy):
    if isinstance(guy, Mon):
        print_mon(guy)
    elif isinstance(guy, Plant):
        print_plant(guy)
    elif isinstance(guy, Remains):
        print("oh my god it's a body")
def ran_away(mon):
    if get_encstat(STATS.CON, mon) <= mon.buffs[STATS.CON]:
        return True
    return False

def all_gone(prey):
    if get_encstat(STATS.HP, prey) <= prey.buffs[STATS.HP]:
        return True
    return False

def took_bite(perp, target, dmg):
    if isinstance(target, Plant) or isinstance(target, Remains):
        #print(f"Mon gained {dmg} energy", end=" ")
        perp.energy -= dmg
        if perp.energy < 0:
            #print("mon couldn't eat any more")
            perp.energy = 0
    return perp


def energy_drain(mon):
    if not isinstance(mon, Mon):
        return mon
    mon.energy += max(calculate_size(mon, mon.level) // 30, 1)
    if mon.energy >= calculate_size(mon, mon.level) and isinstance(mon, Mon):
        energy = calculate_size(mon, mon.level)
        mon.stats[STATS.HP] = energy
        mon.buffs[STATS.HP] = 0
        mon = Remains(mon.stats, mon.traits, mon.buffs)
    return mon

def print_plant(plant):
    
    print("HP " + str(plant.stats[STATS.HP]) + ":(" + str(plant.stats[STATS.HP] - plant.buffs[STATS.HP]) + ") " +
        "D: " + str(plant.stats[STATS.D]) + " " + "SD: " + str(plant.stats[STATS.SD]))
    print()
def print_mon(mon):
    i = 0
    for trait in mon.traits:
        if isinstance(trait, ELEMENTS):
            print(str(trait.value['element'] + "type"), end=", ")
        else:
            print(str(trait.value), end=", ")
    print()
    for lv in [mon.max_level, mon.level]:
        if i == 0:
            print("Max Level")
        else:
            print("Current Level")
        mls = calculate_stats(mon, lv, "stats")
        print("Lv: " + str(lv) + " HP " + str(mls[STATS.HP] * 4) + ":(" + str((mls[STATS.HP] * 4) - mon.buffs[STATS.HP]) + ") " +
              " C " + str(mls[STATS.CON] * 4) + ":(" + str((mls[STATS.CON] * 4) - mon.buffs[STATS.CON]) + ") " +
              "D: " + str(mls[STATS.D]) + " " + "SD: " + str(mls[STATS.SD]) + " " + "A: " + str(mls[STATS.A]) + " " +
              "SA: " + str(mls[STATS.SA]) + " " + "S: " + str(mls[STATS.S]) + " E " + str(calculate_size(mon, lv)) + 
              ":(" + str(calculate_size(mon, lv) - mon.energy) + ") ")
        

        mems = calculate_stats(mon, lv, "e moves")
        mbms = calculate_stats(mon, lv, "")
        big_d = mbms | mems
        for key in big_d:
            print("(" + str(key.value) + " P: " + str(big_d[key]) + ")", end=" ")
        print()
        i += 1
    print()

main()


# stats are the basic numbers while traits give bonuses to certain skills ie walking vs swimming

#traits walking stat