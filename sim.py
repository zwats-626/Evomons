import copy
import random 
from enum import Enum
import sys
import gc
""" All Classes """

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

class HIDDEN(Enum):
    HIDDEN = "HIDDEN"

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

class Obj():
    def __init__(self, stats, traits, buffs, max_age, max_level, level, exp, age, type):
        self.stats = stats
        self.traits = traits
        self.buffs = buffs
        self.max_age = max_age
        self.max_level = max_level
        self.level = level
        self.exp = exp
        self.age = age
        self.type = type
        
    def to_dict_base(self):
        return {
            "type": self.type,
            "stats": {k.value: v for k, v in self.stats.items()},
            "current_stats": self.stat_ty_to_dict(self.level, "s"),
            "max_stats": self.stat_ty_to_dict(self.max_level, "s"),
            "buffs": {k.value: v for k, v in self.buffs.items()},
            "level": self.level,
            "max_level": self.max_level,
            "age": self.age,
            "max_age": self.max_age,
            "exp": self.exp,
            "traits": self._traits_to_dict(),
            "size": calculate_size(self, 100),
            "current_size": calculate_size(self, self.level),
            "max_size": calculate_size(self, self.max_level)
        }

    def _traits_to_dict(self):
        traits = {}
        for trait in self.traits:
            nd = {}
            if  isinstance(trait, TRAITS):
                nd = {trait.value:  self.traits[trait]}
            else:
                nd = {trait.value["element"]: self.traits[trait]}
            traits = traits | nd
        return traits
    
    def stat_ty_to_dict(self, level, flag):
        d = calculate_stats(self, level, "stats")
        if flag == "m":
            d = calculate_stats(self, level, "") | calculate_stats(self, level, "e moves") 
        return {k.value: v for k, v in d.items()}
    
    def print_obj(self):
        s = ""
        s += f"Level: {self.level}(exp: {self.exp}) Age:{self.age} Clade: #TODO\n"

        for trait in self.traits:
            
            if isinstance(trait, ELEMENTS):
                s += f"type {trait.value['element']}"
            else:
                s += f"{trait.value}"
            s += f": {self.traits[trait]}, "
        s += "\n"

        for stat in self.stats:
            s += f"{stat.value}: "
            if stat == STATS.HP:
                hp = get_encstat(STATS.HP, self)
                s += f"({hp}){hp - self.buffs[STATS.HP]} "
            else:
                s += f"{get_encstat(stat, self)} "
        s += "\n"

        return s
    
    def base_turn(self):
        return self

    
class Mon(Obj):
    def __init__(self, stats, buffs, max_level, max_age, traits, encounter_moves, 
                 basic_moves, brain, energy, child, turns_carried,
                 level, exp, age, type):

        super().__init__(stats, traits, buffs, max_age, max_level, level, exp, age, type)
        self.encounter_moves = encounter_moves
        self.basic_moves = basic_moves
        self.brain = brain
        self.energy = energy
        self.child = child
        self.turns_carried = turns_carried
        self.type = "mon"
        
    def to_dict(self):
        brain = {}        
        for net in ['encounter', 'basic']:
            brain[net] = {}
            for layer in [["inputs", self.brain[net].inputs], 
                        ["hiddens", self.brain[net].hiddens],
                        ["outputs", self.brain[net].outputs]]:
                brain[net][layer[0]] = []
                for neuron in layer[1]:
                    n = {
                        "action": neuron.action.value,
                        "threshold": neuron.threshold,
                        "axons": [axon for axon in neuron.axons],
                        "bias": neuron.bias,
                        "afunction": neuron.afunction.value
                        }
                    brain[net][layer[0]].append(n)
        
        child = "None"
        if self.child != None: 
            child = self.child.to_dict()

        return {
            **self.to_dict_base(),
            "encounter_moves": {k.value: v for k, v in self.encounter_moves.items()},
            "basic_moves": {k.value: v for k, v in self.basic_moves.items()},
            "current_moves": self.stat_ty_to_dict(self.level, "m"),
            "max_moves": self.stat_ty_to_dict(self.max_level, "m"),
            "energy": self.energy,
            "brain": brain,
            "turns_carried": self.turns_carried,
            "child": child 
        }
    def print_self(self):
        s = self.print_obj()
        s += f"Energy: {calculate_size(self, self.level)}({calculate_size(self, self.level) - self.energy})"
        for moves in [self.basic_moves, self.encounter_moves]:
            for move in moves:
                s += f"{move.value}: "
                s += f"{moves[move]} "
                
        if self.child != None:
            s += f"Child: {self.child} carried: {self.turns_carried}"
        s += "\n"

        for net in ['encounter', 'basic']:
            for layer in ['inputs', 'hiddens', 'outputs']:
                neurons = getattr(self.brain[net], layer)
                for neuron in neurons:
                    for attr in [net + " " + layer, neuron.action, neuron.axons, neuron.threshold, neuron.afunction.value, neuron.bias]:
                        s += attr + " "
                        
                    s += "\n"
        print(s)
    
    def turn(self):
        global ECO
        self.age += 1
        action =  process_network(self.brain['basic'], self, None)
        power = get_move(action, self, "b")
        self, other = make_move(action, self, None, power)
        if other == None:
            return self
        oth_idx = -1
        for idx, obj in enumerate(ECO):
            if obj is other:
                oth_idx = idx
        self, other = run_encounter(self, other)
        ECO[oth_idx] = other 
        return self

class Plant(Obj):
    def __init__(self, stats, traits, buffs, max_age, max_level, level, exp, age, type):
        super().__init__(stats, traits, buffs, max_age, max_level, level, exp, age, type)
        self.stats[STATS.CON] = 0
        self.type = "plant"

    def to_dict(self):
        return self.to_dict_base()
    
    def print_self(self):
        print(self.print_obj())

    def turn(self):
        global SEED_BANK, SPACE_TAKEN

        self.age += 1
        regen = max(get_encstat(STATS.HP, self) // 8, 1)
        if self.buffs[STATS.HP] > 0:
            self.buffs[STATS.HP] -= regen
            
        if self.buffs[STATS.HP] < 0:
            self.buffs[STATS.HP] = 0
        
        SEED_BANK.append(spawn_plant(self))
        size = plant_size(self)

        if SPACE_TAKEN + size < TOTAL_SPACE:    
            self = gain_exp(self, 10)
            
        if get_encstat(STATS.HP, self) <= self.buffs[STATS.HP]:
            SPACE_TAKEN -= size
            return None
        return self
        

class Remains(Obj):
    def __init__(self, stats, traits, buffs, max_age, max_level, level, exp, age, type):
        super().__init__(stats, traits, buffs, max_age, max_level, level, exp, age, type)
        self.level = level
        self.max_age = 8
        self.stats[STATS.CON] = 0
        self.type = "remains"

    def to_dict(self):
        return self.to_dict_base()
    
    def print_self(self):
        print(self.print_obj())

    def turn(self):
        return self.base_turn()


all_stats = [stat for stat in STATS]
all_elements = [el for el in ELEMENTS]
all_encounter_moves = [m for m in ENCOUNTER_MOVES]
all_basic_moves = [m for m in BASIC_MOVES]
all_encounter_inputs = [el for el in ENCOUNTER_INPUTS]
all_basic_inputs = [el for el in BASIC_INPUTS]
all_traits = [t for t in TRAITS]
all_funcions = [func for func in NEURON_FUNCTIONS]


# max amount of plant bio-mass
TOTAL_SPACE = 40000
# current bio-mass in simulation
SPACE_TAKEN = 0

# how close in stats and traits do two mons need to be
# in irder to reproduce
DIST_BETWEEN_SPECIES = 200

# chance to mutate small values
MUTATE_VALUE = 25
# chance to mutate traits
MUTATE_TRAIT = 5
# denominator to the values above
MUTATE_DENOM = 1000

ECO = []
NEW_OBJs = []
SEED_BANK = []
#### Main ####
total_turns = 0
def run_sim(eco, total_turns, turns):
    global ECO, NEW_OBJs, SPACE_TAKEN, SEED_BANK
    NEW_OBJs = []
    ECO = eco
    
    SPACE_TAKEN = 0
    for plant in [plant for plant in ECO if isinstance(plant, Plant)]:
        print(f"space: {SPACE_TAKEN}")

        SPACE_TAKEN += plant_size(plant)
 
    for _ in range(turns):
        total_turns += 1

        print(f"\n__TURN: {total_turns}__")
        for idx, obj in enumerate(ECO):
            if not isinstance(obj, Obj):
                continue
            obj = obj_death(obj)
            if not isinstance(obj, Obj):
                continue
            obj.turn()
            obj = end_turn(obj)
            ECO[idx] = obj
        ECO.extend(NEW_OBJs)
        #print(f"New OBJ {NEW_OBJs}")
        NEW_OBJs = []
        #print(f"New OBJ after clear {NEW_OBJs}")
        if SPACE_TAKEN < TOTAL_SPACE:
            for seed in SEED_BANK:
                if plant_size(seed) < TOTAL_SPACE - SPACE_TAKEN and (sum(1 for obj in ECO if isinstance(obj, Mon)) * 4) > sum(1 for obj in ECO if isinstance(obj, Plant)):
                    ECO.append(seed)
                    SPACE_TAKEN += plant_size(seed)
            if len(SEED_BANK) > (sum(1 for obj in ECO if isinstance(obj, Mon)) * 4):
                SEED_BANK = []
        ECO = [obj for obj in ECO if obj is not None]
        mons, plants, remains = get_dem()
        s = f'Mons:{mons} Plants:{plants} Remains:{remains}'
        if plants <= 0:
           ECO.extend([random_plant() for _ in range(5)]) 
        if 0 in (mons, plants):
            #print(f"ecosystem collapsed at turn: {total_turns} {s}")
            break
    #print(f"total space {TOTAL_SPACE} \nspace taken {SPACE_TAKEN}")
    #debug_memory_usage()
    return ECO, total_turns

def create_new_eco():
    global ECO
    startmons = [starter_mon()]
    eco = [copy.deepcopy(mon) for mon in startmons for _ in range(20)]
    eco += [random_plant() for _ in range(200)]
    ECO = eco
    return ECO

def plant_size(plant: Plant) -> Plant:
    d = calculate_stats(plant, plant.level, "stats")
    s = sum(d[stat] for stat in d)
    return s


def run_encounter(actor, recp):
    for guy in [actor, recp]:
        guy.buffs[STATS.CON] = 0
    # print("encounter started")
    
    max_encounter_turns = 10
    for _ in range(max_encounter_turns): 

        enc_fin = False
        for a, r in [(actor, recp),(recp, actor)]:
            if r == None:
                    enc_fin = True
                    break

            if isinstance(a, Mon):
                action = process_network(a.brain['encounter'], a, r)
                if action != None:
                    power = get_move(action, a, "e moves")
                    na, nr = make_move(action, a, r, power)
                    
                    if (a, r) == (actor, recp):
                        actor, recp = na, nr
                    else:
                        recp, actor = na, nr
                    if ran_away(r) and action == ENCOUNTER_MOVES.RUN:
                        enc_fin = True
                    elif a.energy <= 0 and not isinstance(r, Mon):
                        enc_fin = True

            if enc_fin:
                break
        if enc_fin:
            break

    return actor, recp





def coinflip(heads, tales):
    coin = random.randrange(0,2)
    result = heads
    if coin == 0:
        result = heads
    else:
        result = tales
    return result

def get_dem():
    mons = sum(1 for obj in ECO if isinstance(obj, Mon))
    plants = sum(1 for obj in ECO if isinstance(obj, Plant))
    remains = sum(1 for obj in ECO if isinstance(obj, Remains))
    return mons, plants, remains
  
def get_biomass():
    mons = sum(calculate_size(obj, obj.level) for obj in ECO if isinstance(obj, Mon))
    plants = sum(calculate_size(obj, obj.level) for obj in ECO if isinstance(obj, Plant))
    remains = sum(calculate_size(obj, obj.level) for obj in ECO if isinstance(obj, Remains))
    return mons, plants, remains


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

def calculate_stats(obj, objlv, flag):
    lv = objlv / 100
   
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
    if STATS.CON in dic.keys():
        dic[STATS.CON] *= 4
        dic[STATS.HP] *= 4
    
    return dic



#CLEAN TODO  ####################### INIT SIM  ###################################

def random_plant():
    value = []
    buff = []
    for stats in all_stats:
        value.append(random.randrange(0, 100))
        buff.append(0)

    stats = dict(zip(all_stats, value))
    element = all_elements[random.randrange(0, len(all_elements))]
    buffs = dict(zip(all_stats, buff))
    stats[STATS.CON] = 0

    max_age = random.randrange(10, 200)
    max_level = random.randrange(1, 10)

    return Plant(stats, {element: 50}, buffs, max_age, max_level, 0, 0, 0, "plant")


def starter_mon():

    stat_val = []
    for stat in all_stats:
        stat_val.append(random.randrange(1, 10))

    ran_stats = dict(zip(all_stats, stat_val))

    buffs = dict.fromkeys(all_stats, 0)

    level = 1
    age = random.randrange(50, 100)
    element = ELEMENTS.NORMAL

    key_traits = [TRAITS.HERBAVOR]
    key_traits.append(element)
    trait_val = []
    for _ in key_traits:
        trait_val.append(random.randrange(1, 10))
    traits = dict(zip(key_traits, trait_val))

    # rand_encounter_m = rand_dict(all_encounter_moves)
    rand_encounter_m = keys_to_rand_dic([ENCOUNTER_MOVES.MATE, ENCOUNTER_MOVES.ATTACK,
                                         ENCOUNTER_MOVES.RUN])


    rand_basic_moves = keys_to_rand_dic([BASIC_MOVES.SEARCH_MATE, BASIC_MOVES.SEARCH_PLANT])

    brain = {
        "basic": Neural_Network(
            # inputs
            [Neuron(BASIC_INPUTS.SELF_ENERGYB, 0,
                    0, 0, [0, 1], 0, NEURON_FUNCTIONS.ADD)],
            # hiddens  
            [Neuron(HIDDEN.HIDDEN, 0, 
                    0, 0, [0], 5, NEURON_FUNCTIONS.ADD),
            Neuron(HIDDEN.HIDDEN, 0,
                    3, 0, [1], 10, NEURON_FUNCTIONS.ADD)],
            # outputs
            [Neuron(BASIC_MOVES.SEARCH_MATE, 0,
                    0, 0, [0], 0, NEURON_FUNCTIONS.ADD),
            Neuron(BASIC_MOVES.SEARCH_PLANT, 0,
                    0, 0, [0], 0, NEURON_FUNCTIONS.ADD)]),
        "encounter":  Neural_Network(
            # inputs
            [Neuron(ENCOUNTER_INPUTS.OTHER_ANIMAL, 0,
                    90, 0, [0], 0, NEURON_FUNCTIONS.ADD),
            Neuron(ENCOUNTER_INPUTS.OTHER_PLANT, 0,
                    90, 0, [1], 0, NEURON_FUNCTIONS.ADD)],
            
            # hiddens  
            [Neuron(HIDDEN.HIDDEN, 0, 
                    0, 0, [0], 0, NEURON_FUNCTIONS.ADD),
            Neuron(HIDDEN.HIDDEN, 0,
                    0, 0, [1], 0, NEURON_FUNCTIONS.ADD),
            Neuron(HIDDEN.HIDDEN, 0, 
                    0, 0, [2], 10, NEURON_FUNCTIONS.ADD)],
            # outputs
            [Neuron(ENCOUNTER_MOVES.MATE, 0,
                    0, 0, [0], 0, NEURON_FUNCTIONS.ADD),
            Neuron(ENCOUNTER_MOVES.ATTACK, 0,
                    0, 0, [0], 0, NEURON_FUNCTIONS.ADD),
            Neuron(ENCOUNTER_MOVES.RUN, 0,
                    0, 0, [0], 0, NEURON_FUNCTIONS.ADD)])
    }
    energy = 20
    return Mon(ran_stats, buffs, level, age, traits, rand_encounter_m, 
               rand_basic_moves, brain, energy, None, 0, 1, 0, 0, "mon")


def keys_to_rand_dic(keys):
    value = []
    for _ in keys:
        value.append(random.randrange(1, 10))
    return dict(zip(keys, value))

def rand_neuron(actions, axon_range):
    action = random.choice(actions)
    input = 0
    thresh = random.randrange(-10, 10)
    output = 0
    axons = [random.randrange(0, axon_range)]
    bias = random.randrange(-3, 3)
    func = all_funcions[random.randrange(0, len(all_funcions))]

    n = Neuron(action, input, thresh, output, axons, bias, func)
    return n


#CLEAN TODO   #################    Neural Network   #####################################


def process_network(network, mon, other_mon): 
    for neuron in network.inputs + network.hiddens + network.outputs:
        neuron.output = 0
        neuron.input_value = 0


    for neuron in network.inputs:
        neuron.input_value = get_input(neuron.action, mon, other_mon)
        # print(f"Neuron input {neuron.action} {neuron.input_value}")
    for section in [network.inputs, network.hiddens, network.outputs]:
        next_sec = network.hiddens
        if section == network.hiddens:
            next_sec = network.outputs
        elif section == network.outputs:
            next_sec = None
        
        for neuron in section:
            if neuron.input_value >= neuron.threshold:
                out = get_neuron_function(neuron.input_value, neuron.bias, neuron.afunction)
            else:
                out = 0
            # print(f"Neuron out {neuron.action} {out} ")
            for axon in neuron.axons:
                # print(f"Neuron axon:{axon}")
                if  next_sec != None and axon < len(next_sec):
                    
                    next_sec[axon].input_value += int(out)
                    
                if next_sec == None:
                    neuron.output = int(out)
    if len(network.outputs) < 1:
        return None
    highest = network.outputs[0]
    for neuron in network.outputs:
        # print(f"Neuron: {neuron.action} ({neuron.output})")
        if neuron.output > highest.output:
            highest = neuron
    return highest.action


def get_neuron_function(input, bias, func):
    
    match func:
        case NEURON_FUNCTIONS.MULT:
            return ((input * -1) + bias) # was *
        case NEURON_FUNCTIONS.ADD:
            return (input + bias)
        case NEURON_FUNCTIONS.DIVIDE:
            if bias == 0:
                bias = 1
            return (input - bias) # was /
        case NEURON_FUNCTIONS.SUBTRACT:
            return (input - bias)
        case _:
            # print("failed path to neuron function")
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
            # print("neuron input request/path not found")
            return 0


def make_move(action, mon, other, power):
    match action:
        case BASIC_MOVES.REST:
            return rest(mon, power)
        case BASIC_MOVES.SEARCH_PLANT:
            return search(mon, Plant, 'not mate', power)
        case BASIC_MOVES.SEARCH_ANIMAL:
            return search(mon, Mon, 'not mate', power)
        case BASIC_MOVES.SEARCH_MATE:
            return search(mon, Mon, 'mate', power)
        case BASIC_MOVES.SEARCH_REMAINS:
            return search(mon, Remains, 'not mate', power)


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
    return d[stat]

def get_move(action, obj, flag):
    lv = obj.level
    d = calculate_stats(obj, lv, flag)
    return d[action]










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

   
def rest(mon, power):
    for buff in [mon.buffs[STATS.HP], mon.buffs[STATS.HP]]:
        if buff > 0:
            buff = max(buff - power, 0)
    return mon, None


def search(mon, cls, flag, power):
    global ECO

    partner = False
    if flag == 'mate':
        partner = True

    
    for _ in range(power):
        i = random.randrange(0, len(ECO))
        if isinstance(ECO[i], cls) and ECO[i] is not mon and partner == False:
            #print(f"found {ECO[i]}")
            return mon, ECO[i]
        elif isinstance(ECO[i], cls) and ECO[i] is not mon and partner and compare_species(mon, ECO[i]) < DIST_BETWEEN_SPECIES:
            #print(f"found {ECO[i]}")
            return mon, ECO[i]

    
    if ECO[i] is not mon:
        #print("could not find _ but instead found")
        return mon, ECO[i]
    else:
        #print("only found its own shaddow")
        return mon, ECO[i]


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
    
    return Plant(stats, {element: 50}, buffs, max_age, max_level, 1, 0, 0, "plant")


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
    # print_dmg(mon, obj, action, hit_points, power, dmg)

    mon = took_bite(mon, obj, hit_points, dmg)        
    obj = obj_death(obj)
    
    return mon, obj 

def mate(parent_a, parent_b):

    if not isinstance(parent_b, Mon):
        # print("tried to mate a non animal")
        return parent_a, parent_b
    elif  isinstance(parent_a.child, Mon):
        # print("mon was already carrying a child")
        return parent_a, parent_b
    elif process_network(parent_b.brain['encounter'], parent_b, parent_a) != ENCOUNTER_MOVES.MATE:
        # print("other did not consent")
        return parent_a, parent_b
    elif compare_species(parent_a, parent_b) > DIST_BETWEEN_SPECIES:

        print(f"offspring not viable distance {compare_species(parent_a, parent_b)}")
        return parent_a, parent_b
    

    """Age Level Stats and Buffs"""
    child_buffs = dict(zip([sta for sta in all_stats], [0 for _ in all_stats]))
    child_stats = copy.deepcopy(child_buffs)
    for stat in all_stats:
        child_stats[stat] = max(coinflip(parent_a, parent_b).stats[stat] + mutate_val(), 1)
    child_max_level = inheret_val(parent_a, parent_b, "max_level")
    child_max_age = inheret_val(parent_a, parent_b, "max_age")
    

    """non Elemental Traits"""
    unique_traits_a = [trait for trait in parent_a.traits if trait not in parent_b.traits and isinstance(trait, TRAITS)] 
    unique_traits_b = [trait for trait in parent_b.traits if trait not in parent_a.traits and isinstance(trait, TRAITS)]
    shared_traits = [trait for trait in parent_a.traits if trait in parent_b.traits and isinstance(trait, TRAITS)]
    child_traits = {}
    for trait in shared_traits:
        child_traits[trait] = max(coinflip(parent_a, parent_b).stats[stat] + mutate_val(), 1)
    for u_trait, parent in [(unique_traits_a, parent_a), (unique_traits_b, parent_b)]:
        for trait in u_trait:
            if coinflip(True, False):
                max(parent.stats[stat] + mutate_val(), 1)
    """ add random trait"""
    if mutate_trait():
        i = random.randrange(0, len(all_traits))
        if all_traits[i] not in child_traits:
            child_traits[all_traits[i]] = 10
    """ remove random trait"""
    if mutate_trait() and len(list(child_traits)) > 0:
        t = random.choice(list(child_traits))
        del child_traits[t]
    """inherit elemental Traits"""
    parent = coinflip(parent_a, parent_b)
    for trait in parent.traits:
        if isinstance(trait, ELEMENTS):
            if mutate_trait() and parent.traits[trait] <= 10:
                if trait == ELEMENTS.NORMAL:
                    child_traits[all_elements[random.randrange(0, len(all_elements))]] = 10
                elif trait != ELEMENTS.NORMAL:
                    child_traits[ELEMENTS.NORMAL] = 1
            else:
                child_traits[trait] = max(parent.traits[trait] + mutate_val(), 1)



    """Inheret brain"""
    
    brain_a = copy.deepcopy(parent_a.brain)
    brain_b = copy.deepcopy(parent_b.brain)
    child_brain = {'basic': Neural_Network([], [], []), 'encounter': Neural_Network([], [], [])}

    for net, layers in [('basic', [('hiddens', [HIDDEN.HIDDEN]), ('outputs', all_basic_moves), ('inputs', all_basic_inputs)]), 
                        ('encounter', [('hiddens', [HIDDEN.HIDDEN]), ('outputs', all_encounter_moves), ('inputs', all_encounter_inputs)])]:
        for layer, actions in layers:
            neurons_a = getattr(brain_a[net], layer)
            neurons_b = getattr(brain_b[net], layer)
            
            child_neurons = []
            short_list, long_list = neurons_a, neurons_b
            if len(neurons_a) > len(neurons_b):
                short_list, long_list = neurons_b, neurons_a
            i = 0 
            for n in long_list:
                
                if i < len(short_list):
                    child_neurons.append(coinflip(neurons_a, neurons_b)[i])
                else:
                    if coinflip(True, False):
                        child_neurons.append(long_list[i])
                
                i += 1
                """Mutate Neurons"""
                if len(child_neurons) < 1:
                    continue
                n = child_neurons[len(child_neurons)-1]
                n.threshold += mutate_val()
                n.bias += mutate_val()
                if mutate_trait():
                    if coinflip(True, False) and len(n.axons) > 0:
                        j = random.randrange(0, len(n.axons))
                        n.axons[j] = max(n.axons[j] + mutate_val(), 0)
                    else:
                        if coinflip(True, False) and len(n.axons) > 0:
                            n.axons.pop()
                        else:
                            n.axons.append(random.randrange(0, len(long_list)))
                if mutate_trait():
                    n.afuction = all_funcions[random.randrange(0, len(all_funcions))]
                if mutate_trait():
                    n.action = actions[random.randrange(0, len(actions))]
            empty = getattr(child_brain[net], layer)
            empty += child_neurons

                #print(f"end of secound loop {layer} {node_list}")
    
    #print(f"child brain {child_brain['basic'].inputs}, {child_brain['encounter'].inputs}")
    if mutate_trait():
        net, layers = random.choice([(child_brain["basic"], [('inputs', all_basic_inputs), ('hiddens', [HIDDEN.HIDDEN]), ('outputs', all_basic_moves)]), 
                                     (child_brain["encounter"], [('inputs', all_encounter_inputs), ('hiddens', [HIDDEN.HIDDEN]), ('outputs', all_encounter_moves)])])
        layer, actions = random.choice(layers)
        if coinflip(True, False) and len(getattr(net, layer)) > 0:
            getattr(net, layer).pop()
        else:
            getattr(net, layer).append(rand_neuron(actions, 5))

    """Inherit and mutate moves"""
    child_bmoves, child_emoves = {}, {} 

    for net, new_mvs, mv_l in [('encounter', child_emoves, 'encounter_moves'), ('basic', child_bmoves, 'basic_moves')]:
        for act in [neuron.action for neuron in child_brain[net].outputs]:
            #print(getattr(parent_a, mv_l))
            sorce_a = [move_act for move_act in getattr(parent_a, mv_l)] 
            sorce_b = [move_act for move_act in getattr(parent_b, mv_l)]

            if act in sorce_a and act in sorce_b:
                new_mvs[act] = coinflip(getattr(parent_a, mv_l), getattr(parent_b, mv_l))[act]
            elif act in sorce_b:
                new_mvs[act] = getattr(parent_b, mv_l)[act]
            elif act in sorce_a:
                new_mvs[act] = getattr(parent_a, mv_l)[act]
            else:
                new_mvs[act] = 10

    #print(child_emoves)
    #print(child_bmoves)
        

                        
    new_mon = Mon(stats=child_stats, buffs=child_buffs, max_level=child_max_level, max_age=child_max_age, traits=child_traits, encounter_moves=child_emoves, 
                  basic_moves=child_bmoves, brain=child_brain, energy=0, child=None, turns_carried=0, level=1, exp=0, age=0, type="mon")
    #print_obj(new_mon)
    #print_brain(new_mon.brain)
    parent_a.child = new_mon
    parent_a.turns_carried = 0
    # print("mons mated")
    return parent_a, parent_b

def inheret_val(parent_a, parent_b, attr):
    return max(getattr(coinflip(parent_a, parent_b), attr) + mutate_val(), 1)

def mutate_val():
    if random.randrange(0, MUTATE_DENOM) <= MUTATE_VALUE:
        return random.randrange(-1,2)
    return 0

def mutate_trait():
    if random.randrange(0, MUTATE_DENOM) <= MUTATE_TRAIT:
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
    elif obj.age >= obj.max_age:
        if s != '':
            s += ', it '
        s += 'was old'
    elif isinstance(obj, Mon) and calculate_size(obj, obj.level) - obj.energy  <= 0:
        if s != '':
            s += ', it '
        s += 'was hungry'
    elif s == '':
        return obj

    global SPACE_TAKEN
    if isinstance(obj, Plant):
        SPACE_TAKEN -= plant_size(obj)
    if not isinstance(obj, Mon):
        for cls, old, dmg in [(Remains, "corpse rotted away", "the last scraps were eaten"), 
                              (Plant, "plant grew dry and barren and withered away", "plant was completely consumed")]:
            if isinstance(obj, cls):
                if 'was old' in s:
                    # print(old)
                    return None
                else:
                   # print(dmg)
                   return None
        return None
    else:
        # print(f"animal died it {s}.")
        stats = copy.deepcopy(obj.stats)
        traits = copy.deepcopy(obj.traits)
        buffs = {key: 0 for key in stats}
        return Remains(stats, traits, buffs, obj.max_age, obj.level, obj.level, 0, 0, "remains")

def end_turn(obj):
    if obj == None:
        return None
    global ECO, NEW_OBJs
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
