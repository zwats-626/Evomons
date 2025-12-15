import copy
import random 
import sys
import gc
from . import sim_h as h
from . import brain as b
from . import moves as m
from .classes import *


TOTAL_SPACE = 20000
SPACE_TAKEN = 0
STARTING_MONS = 120
DIST_BETWEEN_SPECIES = 200
MUTATE_VALUE = 25
MUTATE_TRAIT = 5
MUTATE_DENOM = 1000
DEBUGGER = False
ECO = []
NEW_OBJs = []
#### Main ####
total_turns = 0
def run_sim(eco, total_turns, turns):
    global ECO, NEW_OBJs, SPACE_TAKEN
    NEW_OBJs = []
    ECO = eco
    reset_space()

    for _ in range(turns):
        total_turns += 1
        reset_space()
        print(f"\n__TURN: {total_turns}__")
        print(f"Total Space {TOTAL_SPACE} Space Taken {SPACE_TAKEN}")
        for idx, obj in enumerate(ECO):
            if obj == None:
                continue
            if DEBUGGER:
                print(obj)
                obj.print_self()
            obj = turn(obj)
            obj = end_turn(obj)
            
            
            ECO[idx] = obj
        
        ECO.extend(NEW_OBJs)
        NEW_OBJs = []
        ECO = [obj for obj in ECO if obj is not None]
        mons, plants, remains = h.get_dem(ECO)
        print(f'Mons:{mons} Plants:{plants} Remains:{remains}')
        print(f"Total Space {TOTAL_SPACE} Space Taken {SPACE_TAKEN}")
        if 0 in (mons, plants):
            break
    return ECO, total_turns


def run_encounter(mon: Mon, obj: Obj):
    
    end_encounter = False
    max_encounter_turns = 10
    for _ in range(max_encounter_turns):
        for a, b in [(mon, obj), (obj, mon)]:
            end_encounter, mon, obj = encounter_turn(a, b)
            if (end_encounter):
                return mon, obj
    return mon, obj


def encounter_turn(actor, recp):
    global SPACE_TAKEN
    if isinstance(actor, Mon):
            action = b.process_network(actor.brain['encounter'], actor, recp)
            if action != None:
                power = h.get_move(action, actor, "e moves")
                actor, recp = m.make_move(action, actor, recp, power)
                recp = obj_death(recp)
                if recp == None or h.ran_away(recp, action) or h.full(actor, action):
                    return True, actor, recp
    return False, actor, recp



def turn(obj: Obj) -> Obj:
    if isinstance(obj, Mon):
        obj = mon_turn(obj)
    elif isinstance(obj, Plant):
        obj = plant_turn(obj)
    elif isinstance(obj, Remains):
        obj = remains_trun(obj)
    return obj



def remains_trun(remains) -> Remains:
    return remains



def mon_turn(mon: Mon) -> Mon: 
    global ECO
    mon.age += 1
    action =  b.process_network(mon.brain['basic'], mon, None)
    power = h.get_move(action, mon, "b")
    mon, other = m.make_move(action, mon, None, power)
    if other == None:
        return mon
    oth_idx = -1
    for idx, obj in enumerate(ECO):
        if obj is other:
            oth_idx = idx
    mon, other = run_encounter(mon, other)
    ECO[oth_idx] = other 
    return mon



def plant_turn(plant: Plant) -> Plant:
    global NEW_OBJs, SPACE_TAKEN
    
    plant.age += 1
    regen = max(h.get_encstat(STATS.HP, plant) // 8, 1)
    if plant.buffs[STATS.HP] > 0:
        plant.buffs[STATS.HP] -= regen
        
    if plant.buffs[STATS.HP] < 0:
        plant.buffs[STATS.HP] = 0
    
    grown_plant = h.plant_size(plant, plant.level + 1)
    if SPACE_TAKEN + grown_plant < TOTAL_SPACE:   
        SPACE_TAKEN += grown_plant
        plant = h.gain_exp(plant, 10 * plant.level)
        if DEBUGGER:
            print("plant gained lv")
    
    for _ in range(random.randrange(0, plant.seedling + 1)):
        if SPACE_TAKEN < TOTAL_SPACE:
            new_plant = m.spawn_plant(plant)
            if h.plant_size(new_plant, new_plant.level) + SPACE_TAKEN < TOTAL_SPACE:
                NEW_OBJs.append(new_plant)
                SPACE_TAKEN += h.plant_size(new_plant, new_plant.level)
                if DEBUGGER:
                    print("new plant spawned")
        
    return plant



def end_turn(obj: Obj):
    if obj == None:
        return None
    global ECO, NEW_OBJs
    obj.age += 1
    if  isinstance(obj, Mon):
        obj.energy += max(h.calculate_size(obj, obj.level) // 30, 1)
        if isinstance(obj.child, Mon):
            obj.energy += max(h.calculate_size(obj.child, 1) // 8, 1)
            obj.turns_carried += 1
            if isinstance(obj.child, Mon) and obj.turns_carried >= 16:
                NEW_OBJs.append(obj.child)
                obj.child, obj.turns_carried = None, 0
    obj = obj_death(obj)
    return obj


def obj_death(obj: Obj):
    global SPACE_TAKEN
    s = ''
    if h.get_encstat(STATS.HP, obj) <= obj.buffs[STATS.HP]:
        s += 'was attacked'
    elif obj.age >= obj.max_age:
        if s != '':
            s += ', it '
        s += 'was old'
    elif isinstance(obj, Mon) and h.calculate_size(obj, obj.level) - obj.energy  <= 0:
        if s != '':
            s += ', it '
        s += 'was hungry'
    elif s == '':
        return obj

    if isinstance(obj, Plant):
        SPACE_TAKEN -= h.plant_size(obj, obj.level)
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





def reset_space():
    global SPACE_TAKEN, ECO
    SPACE_TAKEN = 0
    for plant in [plant for plant in ECO if isinstance(plant, Plant)]:
        if SPACE_TAKEN + h.plant_size(plant, plant.level) > TOTAL_SPACE:
            plant = None
        else:
            SPACE_TAKEN += h.plant_size(plant, plant.level)
    ECO = [obj for obj in ECO if obj is not None]


def create_new_eco():
    global ECO
    startmons = [starter_mon(i) for i in range(4)]
    startplants = [starter_plant() for _ in range(STARTING_MONS)]
    eco = [copy.deepcopy(mon) for mon in startmons for _ in range(STARTING_MONS // 4)]
    eco += [copy.deepcopy(plant) for plant in startplants for _ in range(1)]
    ECO = eco
    return ECO

def starter_plant():
    value = []
    buff = []
    for stats in all_stats:
        value.append(random.randrange(50, 500))
        buff.append(0)

    stats = dict(zip(all_stats, value))
    element = all_elements[random.randrange(0, len(all_elements))]
    buffs = dict(zip(all_stats, buff))
    stats[STATS.CON] = 0

    max_age = random.randrange(10, 200)
    max_level = random.randrange(1, 10)

    return Plant(stats, {element: 50}, buffs, max_age, max_level, max_level, 0, 0, 3, "plant")

def starter_mon(i):

    stat_val = []
    for stat in all_stats:
        stat_val.append(random.randrange(1, 100))

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
    rand_encounter_m = h.keys_to_rand_dic([ENCOUNTER_MOVES.MATE, ENCOUNTER_MOVES.ATTACK,
                                         ENCOUNTER_MOVES.RUN])


    rand_basic_moves = h.keys_to_rand_dic([BASIC_MOVES.SEARCH_MATE, BASIC_MOVES.SEARCH_PLANT])

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
            [Neuron(ENCOUNTER_INPUTS.SIMILAR_SPECIES, 0,
                    90, 0, [0], 0, NEURON_FUNCTIONS.ADD),
            Neuron(ENCOUNTER_INPUTS.OTHER_PLANT, 0,
                    90, 0, [1], 0, NEURON_FUNCTIONS.ADD),
            Neuron(ENCOUNTER_INPUTS.DIF_SPECIES, 0,
                    90, 0, [2], 0, NEURON_FUNCTIONS.ADD)],
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
            Neuron(ENCOUNTER_MOVES.ATTACK, 0,
                    0, 0, [0], 0, NEURON_FUNCTIONS.ADD)])
    }
    energy = 20
    return Mon(ran_stats, buffs, 4, age, traits, rand_encounter_m, 
               rand_basic_moves, brain, energy, None, 0, 1, 0, 0, "mon", i)

