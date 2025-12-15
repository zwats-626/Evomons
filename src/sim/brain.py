from .classes import *
import random
from . import sim_h as h

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
    from .sim import DIST_BETWEEN_SPECIES
    match request:
        case BASIC_INPUTS.RANDOM:
            return random.randrange(-100, 100)
        case BASIC_INPUTS.SELF_HP:
            return h.get_encstat(STATS.HP, mon)
        case BASIC_INPUTS.SELF_ENERGY:
            return h.calculate_size(mon, mon.level)
        case BASIC_INPUTS.SELF_ATTACK:
            return h.get_encstat(STATS.A, mon)
        case BASIC_INPUTS.SELF_SA:
            return h.get_encstat(STATS.SA, mon)
        case BASIC_INPUTS.SELF_DEFENSE:
            return h.get_encstat(STATS.D, mon)
        case BASIC_INPUTS.SELF_SD:
            return h.get_encstat(STATS.SD, mon)
        case BASIC_INPUTS.SELF_SPEED:
            return h.get_encstat(STATS.S, mon)
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
            return h.get_encstat(STATS.HP, obj)

        case ENCOUNTER_INPUTS.OTHER_ENERGY:
            return h.calculate_size(obj, obj.level)
        case ENCOUNTER_INPUTS.OTHER_ATTACK:
            return h.get_encstat(STATS.A, obj)
        case ENCOUNTER_INPUTS.OTHER_SA:
            return h.get_encstat(STATS.SA, obj)
        case ENCOUNTER_INPUTS.OTHER_DEFENSE:
            return h.get_encstat(STATS.D, obj)
        case ENCOUNTER_INPUTS.OTHER_SD:
            return h.get_encstat(STATS.SD, obj)
        case ENCOUNTER_INPUTS.OTHER_SPEED:
            return h.get_encstat(STATS.S, obj)
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
            if isinstance(obj, Mon) and h.compare_species(mon, obj) < DIST_BETWEEN_SPECIES:
                return 100
            else:
                return 0
        case ENCOUNTER_INPUTS.DIF_SPECIES:
            if not isinstance(obj, Mon) or h.compare_species(mon, obj) > DIST_BETWEEN_SPECIES:
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