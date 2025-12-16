from .classes import *
from typing import List
import random
from . import sim_h as h


def process_network(network: Neural_Network, attacker: Mon, defender: Obj): 
    _validate(network, attacker, defender)
    _reset_neurons(network)
    _set_inputs(network.inputs, attacker, defender)
    _prop_layers(network)
    return _chose_act(network)


def _validate(network: Neural_Network, attacker: Mon, defender: Obj) -> None:
    """Validate all inputs as valid and present"""
    if not all([network, attacker, defender]):
        raise ValueError("network, attacker, and defender are requiered")
    if not isinstance(network, Neural_Network):
        raise TypeError("network must be of type Neural_Network")
    if not isinstance(attacker, Mon):
        raise TypeError("attacker must be of type Mon")
    if not isinstance(defender, Mon):
        raise TypeError("defender must be of type Obj")    
    req_attrs = ['inputs', 'hiddens', 'outputs']
    if not all(hasattr(network, attr) for attr in req_attrs):
        raise ValueError(f"network must have {req_attrs}")
        

def _reset_neurons(network: Neural_Network) -> None:
    neurons = network.inputs + network.hiddens + network.outputs
    for neuron in neurons:
        neuron.output, neuron.input_value = 0, 0
    

def _set_inputs(inputs: Enum, attacker: Mon, defender: Obj) -> None:
    for neuron in inputs:
        neuron.input_value = _get_input(neuron.action, attacker, defender)


def _get_input(request: Enum, mon: Mon, obj: Obj) -> float:
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
            return 0 if not isinstance(obj, Mon) else obj.energy
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
            return obj.level if isinstance(obj, Mon) else 0
        case ENCOUNTER_INPUTS.SIMILAR_SPECIES:
            return 100 if isinstance(obj, Mon) and h.compare_species(mon, obj) < DIST_BETWEEN_SPECIES else 0
        case ENCOUNTER_INPUTS.DIF_SPECIES:
            return 100 if not isinstance(obj, Mon) or h.compare_species(mon, obj) > DIST_BETWEEN_SPECIES else 0
        case ENCOUNTER_INPUTS.OTHER_ANIMAL:
            return 100 if isinstance(obj, Mon) else 0
        case ENCOUNTER_INPUTS.OTHER_PLANT:
            return 100 if isinstance(obj, Plant) else 0
        case ENCOUNTER_INPUTS.OTHER_REMAINS:
            return 100 if isinstance(obj, Remains) else 0
        case _:
            return 0
        

def _prop_layers(network: Neural_Network) -> None:
    layer_pairs = [(network.inputs, network.hiddens), (network.hiddens, network.outputs), (network.outputs, None)]
    for section, next_section in layer_pairs:
        for neuron in section:
            _cal_output(neuron)
            _prop_outputs(neuron, next_section)


def _cal_output(neuron: Neuron) -> None:
    if neuron.input_value >= neuron.threshold:
        neuron.output = _get_neuron_function(neuron.input_value, neuron.bias, neuron.afunction)
        neuron.output = 0


def _get_neuron_function(input, bias, func) -> float:    
    match func:
        case NEURON_FUNCTIONS.MULT:
            return ((input * -1) + bias)
        case NEURON_FUNCTIONS.ADD:
            return (input + bias)
        case NEURON_FUNCTIONS.DIVIDE:
            return (input / bias) if bias is not 0 else 0 
        case NEURON_FUNCTIONS.SUBTRACT:
            return (input - bias)
        case _:
            return 0


def _prop_outputs(neuron: Neuron, next_layer: List[Neuron]) -> None:
    if next_layer is None:
        return
    for axon in neuron.axons:
        if axon <= len(next_layer):
            next_layer[axon] += neuron.output 


def _chose_act(outputs: List[Neuron]) -> Enum:
    if not outputs:
        return None
    choice = max(outputs, key=lambda n: n.output)
    return choice

