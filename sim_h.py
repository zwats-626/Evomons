import random, gc, sys
from classes import *

def get_encstat(stat, obj):
    lv = obj.level
         
    d = calculate_stats(obj, lv, "stats")
    return d[stat]

def get_move(action, obj, flag):
    lv = obj.level
    d = calculate_stats(obj, lv, flag)
    return d[action]

def inheret_val(parent_a, parent_b, attr):
    return max(getattr(coinflip(parent_a, parent_b), attr) + mutate_val(), 1)

def coinflip(heads, tales):
    coin = random.randrange(0,2)
    result = heads
    if coin == 0:
        result = heads
    else:
        result = tales
    return result

def get_dem(eco):
    mons = sum(1 for obj in eco if isinstance(obj, Mon))
    plants = sum(1 for obj in eco if isinstance(obj, Plant))
    remains = sum(1 for obj in eco if isinstance(obj, Remains))
    return mons, plants, remains
  
def get_biomass(eco):
    mons = sum(calculate_size(obj, obj.level) for obj in eco if isinstance(obj, Mon))
    plants = sum(calculate_size(obj, obj.level) for obj in eco if isinstance(obj, Plant))
    remains = sum(calculate_size(obj, obj.level) for obj in eco if isinstance(obj, Remains))
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

def plant_size(plant: Plant, level) -> Plant:
    d = calculate_stats(plant, level, "stats")
    s = sum(d[stat] for stat in d)
    return s



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

def mutate_val():
    from sim import MUTATE_VALUE, MUTATE_DENOM
    if random.randrange(0, MUTATE_DENOM) <= MUTATE_VALUE:
        return random.randrange(-1,2)
    return 0

def mutate_trait():
    from sim import MUTATE_DENOM, MUTATE_TRAIT
    if random.randrange(0, MUTATE_DENOM) <= MUTATE_TRAIT:
        return True
    return False

def keys_to_rand_dic(keys):
    value = []
    for _ in keys:
        value.append(random.randrange(1, 100))
    return dict(zip(keys, value))

def get_element(obj):
    for trait in obj.traits:
            if isinstance(trait, ELEMENTS):
                return trait
    return ELEMENTS.NORMAL

def print_dmg(mon, obj, action, hit_points, power, dmg):
    print(f"{mon}: ", end='')
    print(f"mon {action.value}s with a power of {power} for {dmg} points", end=" ")
    print(f"Reducing target:{obj} {hit_points.value} to {get_encstat(hit_points, obj)}:({get_encstat(hit_points, obj) - obj.buffs[hit_points]}) ")

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
                    dif += 10
    # print(f"dif: {dif}")
    return dif

def digest(perp, target, hit_points, dmg):
    energy = 10
    if hit_points == STATS.HP and ((isinstance(target, Plant) and TRAITS.HERBAVOR in perp.traits)
                                    or (isinstance(target, Remains) and TRAITS.CARNIVOR in perp.traits)) :
        if isinstance(target, Remains):
            energy *= 10
        perp = gain_exp(perp, energy)
        perp.energy = max(perp.energy - dmg, 0)
    return perp

def gain_exp(obj, exp):
    if obj.level == obj.max_level:
        obj.exp = 0
        return obj
    obj.exp += exp
    if obj.exp > obj.level * 10 and obj.level < obj.max_level:
        obj.level += 1
        obj.exp = 0
    return obj

def ran_away(obj, action):
    return action == ENCOUNTER_MOVES.RUN and (not isinstance(obj, Mon) or h.get_encstat(STATS.CON, obj) >= obj.buffs[STATS.CON])

def full(mon, action):
    if action == (ENCOUNTER_MOVES.SPECIAL_ATTACK or ENCOUNTER_MOVES.ATTACK) and calculate_size(mon, mon.level) - mon.energy  <= 0:
        return True
    return False