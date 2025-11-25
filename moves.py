from classes import *
import sim_h as h
import brain as b
import random
def make_move(action, mon, other, power):
    from sim import DEBUGGER
    if DEBUGGER:
        print(f"mon chose to {action}")
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
"""Basic Moves"""
def rest(mon, power):
    for buff in [mon.buffs[STATS.HP], mon.buffs[STATS.HP]]:
        if buff > 0:
            buff = max(buff - power, 0)
    return mon, None

def search(mon, cls, flag, power):
    from sim import ECO, DIST_BETWEEN_SPECIES
    partner = flag == 'mate'

    for _ in range(power):
        i = random.randrange(0, len(ECO))
        if isinstance(ECO[i], cls) and ECO[i] is not mon and partner == False:
            return mon, ECO[i]
        elif isinstance(ECO[i], cls) and ECO[i] is not mon and partner and h.compare_species(mon, ECO[i]) < DIST_BETWEEN_SPECIES:    
            return mon, ECO[i]

    return mon, ECO[i]

def spawn_plant(parent: Plant) -> Plant:
    values = []
    buffv = []
    for stat in parent.stats:
        value = parent.stats[stat] + h.mutate_val()
        buffv.append(0)
        if value < 1:
            value = 1
        values.append(value)

    seedling = max(1, parent.seedling + h.mutate_val())

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

    max_level = parent.max_level + h.mutate_val()
    max_age = parent.max_age + h.mutate_val()
    
    return Plant(stats, {element: 50}, buffs, max_age, max_level, 1, 0, 0, seedling, "plant")

def combat_move(action, mon, obj):
    
    if obj == None:
        return True, mon, obj

    mon_el, obj_el = h.get_element(mon), h.get_element(obj)
    
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
    attack, defence = h.get_encstat(act_a, mon), h.get_encstat(act_d, obj)
   
    moves = h.calculate_stats(mon, mon.level, 'e moves')
    power =  moves[action]

    dmg = max((attack * power * mod) // defence, 1)

    if dmg + obj.buffs[hit_points] >= h.get_encstat(hit_points, obj):
        dmg = h.get_encstat(hit_points, obj) - obj.buffs[hit_points]
        
    
    obj.buffs[hit_points] += dmg
    mon = h.digest(mon, obj, hit_points, dmg)

    from sim import DEBUGGER
    if DEBUGGER:
        print(f"mon {action} obj:{obj.type} {hit_points}({h.get_encstat(hit_points, obj)}) {h.get_encstat(hit_points, obj) - obj.buffs[hit_points]}")
    
    return mon, obj

def mate(parent_a, parent_b):

    from sim import DIST_BETWEEN_SPECIES
    if not isinstance(parent_b, Mon):
        
        return parent_a, parent_b
    elif  isinstance(parent_a.child, Mon):
        
        return parent_a, parent_b
    elif b.process_network(parent_b.brain['encounter'], parent_b, parent_a) != ENCOUNTER_MOVES.MATE:
        
        return parent_a, parent_b
    elif h.compare_species(parent_a, parent_b) > DIST_BETWEEN_SPECIES:

        print(f"offspring not viable distance {h.compare_species(parent_a, parent_b)}")
        return parent_a, parent_b
    

    """Age Level Stats and Buffs"""
    child_buffs = dict(zip([sta for sta in all_stats], [0 for _ in all_stats]))
    child_stats = copy.deepcopy(child_buffs)
    for stat in all_stats:
        child_stats[stat] = max(h.coinflip(parent_a, parent_b).stats[stat] + h.mutate_val(), 1)
    child_max_level = h.inheret_val(parent_a, parent_b, "max_level")
    child_max_age = h.inheret_val(parent_a, parent_b, "max_age")
    

    """non Elemental Traits"""
    unique_traits_a = [trait for trait in parent_a.traits if trait not in parent_b.traits and isinstance(trait, TRAITS)] 
    unique_traits_b = [trait for trait in parent_b.traits if trait not in parent_a.traits and isinstance(trait, TRAITS)]
    shared_traits = [trait for trait in parent_a.traits if trait in parent_b.traits and isinstance(trait, TRAITS)]
    child_traits = {}
    for trait in shared_traits:
        child_traits[trait] = max(h.coinflip(parent_a, parent_b).traits[trait] + h.mutate_val(), 1)
    for u_trait, parent in [(unique_traits_a, parent_a), (unique_traits_b, parent_b)]:
        for trait in u_trait:
            if h.coinflip(True, False):
                child_traits[trait] = max(parent.traits[trait] + h.mutate_val(), 1)
    """ add random trait"""
    newtraits = [trait for trait in all_traits if trait not in child_traits]
    if h.mutate_trait() and len(newtraits) > 0:
        i = random.randrange(0, len(newtraits))
        if newtraits[i] not in child_traits:
            child_traits[newtraits[i]] = 10
    """ remove random trait"""
    if h.mutate_trait() and len(list(child_traits)) > 0:
        t = random.choice(list(child_traits))
        del child_traits[t]
    """inherit elemental Traits"""
    parent = h.coinflip(parent_a, parent_b)
    for trait in parent.traits:
        if isinstance(trait, ELEMENTS):
            if h.mutate_trait() and parent.traits[trait] <= 10:
                if trait == ELEMENTS.NORMAL:
                    child_traits[all_elements[random.randrange(0, len(all_elements))]] = 10
                elif trait != ELEMENTS.NORMAL:
                    child_traits[ELEMENTS.NORMAL] = 1
            else:
                child_traits[trait] = max(parent.traits[trait] + h.mutate_val(), 1)



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
                    child_neurons.append(h.coinflip(neurons_a, neurons_b)[i])
                else:
                    if h.coinflip(True, False):
                        child_neurons.append(long_list[i])
                
                i += 1
                """Mutate Neurons"""
                if len(child_neurons) < 1:
                    continue
                n = child_neurons[len(child_neurons)-1]
                n.threshold += h.mutate_val()
                n.bias += h.mutate_val()
                if h.mutate_trait():
                    if h.coinflip(True, False) and len(n.axons) > 0:
                        j = random.randrange(0, len(n.axons))
                        n.axons[j] = max(n.axons[j] + h.mutate_val(), 0)
                    else:
                        if h.coinflip(True, False) and len(n.axons) > 0:
                            n.axons.pop()
                        else:
                            n.axons.append(random.randrange(0, len(long_list)))
                if h.mutate_trait():
                    n.afuction = all_funcions[random.randrange(0, len(all_funcions))]
                if h.mutate_trait():
                    n.action = actions[random.randrange(0, len(actions))]
            empty = getattr(child_brain[net], layer)
            empty += child_neurons


    if h.mutate_trait():
        net, layers = random.choice([(child_brain["basic"], [('inputs', all_basic_inputs), ('hiddens', [HIDDEN.HIDDEN]), ('outputs', all_basic_moves)]), 
                                     (child_brain["encounter"], [('inputs', all_encounter_inputs), ('hiddens', [HIDDEN.HIDDEN]), ('outputs', all_encounter_moves)])])
        layer, actions = random.choice(layers)
        if h.coinflip(True, False) and len(getattr(net, layer)) > 0:
            getattr(net, layer).pop()
        else:
            getattr(net, layer).append(h.rand_neuron(actions, 5))

    """Inherit and mutate moves"""
    child_bmoves, child_emoves = {}, {} 

    for net, new_mvs, mv_l in [('encounter', child_emoves, 'encounter_moves'), ('basic', child_bmoves, 'basic_moves')]:
        for act in [neuron.action for neuron in child_brain[net].outputs]:

            sorce_a = [move_act for move_act in getattr(parent_a, mv_l)] 
            sorce_b = [move_act for move_act in getattr(parent_b, mv_l)]

            if act in sorce_a and act in sorce_b:
                new_mvs[act] = h.coinflip(getattr(parent_a, mv_l), getattr(parent_b, mv_l))[act]
            elif act in sorce_b:
                new_mvs[act] = getattr(parent_b, mv_l)[act]
            elif act in sorce_a:
                new_mvs[act] = getattr(parent_a, mv_l)[act]
            else:
                new_mvs[act] = 10

        

                        
    new_mon = Mon(stats=child_stats, buffs=child_buffs, max_level=child_max_level, max_age=child_max_age, traits=child_traits, encounter_moves=child_emoves, 
                  basic_moves=child_bmoves, brain=child_brain, energy=0, child=None, turns_carried=0, level=1, exp=0, age=0, type="mon")
    
    parent_a.child = new_mon
    parent_a.turns_carried = 0
    return parent_a, parent_b



