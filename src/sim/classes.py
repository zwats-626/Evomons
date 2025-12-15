from enum import Enum
from . import sim_h as h
import copy



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
    DIF_SPECIES = "DIF SPECIES"
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
            "size": h.calculate_size(self, 100),
            "current_size": h.calculate_size(self, self.level),
            "max_size": h.calculate_size(self, self.max_level)
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
        d = h.calculate_stats(self, level, "stats")
        if flag == "m":
            d = h.calculate_stats(self, level, "") | h.calculate_stats(self, level, "e moves") 
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
                hp = h.get_encstat(STATS.HP, self)
                s += f"({hp}){hp - self.buffs[STATS.HP]} "
            else:
                s += f"{h.get_encstat(stat, self)} "
        s += "\n"

        return s
    
  
class Mon(Obj):
    def __init__(self, stats, buffs, max_level, max_age, traits, encounter_moves, 
                 basic_moves, brain, energy, child, turns_carried,
                 level, exp, age, type, species):

        super().__init__(stats, traits, buffs, max_age, max_level, level, exp, age, type)
        self.encounter_moves = encounter_moves
        self.basic_moves = basic_moves
        self.brain = brain
        self.energy = energy
        self.child = child
        self.turns_carried = turns_carried
        self.type = "mon"
        self.species = species
        
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
            "child": child,
            "species": self.species
        }
    
    def print_self(self):
        s = self.print_obj()
        s += f"Energy: {h.calculate_size(self, self.level)}({h.calculate_size(self, self.level) - self.energy})"
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
                    for attr in [net + " " + layer, neuron.action.value, neuron.axons, neuron.threshold, neuron.afunction.value, neuron.bias]:
                        s += f"{attr}" + " "
                        
                    s += "\n"
        print(s)
    


class Plant(Obj):
    def __init__(self, stats, traits, buffs, max_age, max_level, level, exp, age, seedling, type):
        super().__init__(stats, traits, buffs, max_age, max_level, level, exp, age, type)
        self.stats[STATS.CON] = 0
        self.seedling = seedling
        self.type = "plant"

    def to_dict(self):
        return self.to_dict_base()
    
    def print_self(self):
        print(self.print_obj())


        
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
        







all_stats = [stat for stat in STATS]
all_elements = [el for el in ELEMENTS]
all_encounter_moves = [m for m in ENCOUNTER_MOVES]
all_basic_moves = [m for m in BASIC_MOVES]
all_encounter_inputs = [el for el in ENCOUNTER_INPUTS]
all_basic_inputs = [el for el in BASIC_INPUTS]
all_traits = [t for t in TRAITS]
all_funcions = [func for func in NEURON_FUNCTIONS]