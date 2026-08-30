import math
import random
import matplotlib.pyplot as plt

C_return_min = -20
C_return_max = 20

C_rand_avg_bias_chance = 0.5
C_average_weight = 0.25
C_momentum_weight = 0.15

def get_apply_rand_avg_bias_w(rand_avg_bias_chance = C_rand_avg_bias_chance):
    def apply_rand_avg_bias_w(target_average, curr_sequence, return_min, return_max) -> tuple[int, int]:
        if (random.random() > rand_avg_bias_chance):
            return (return_min, return_max)
        
        return (return_min + target_average * 2, return_max + target_average * 2)
    
    return apply_rand_avg_bias_w

def get_apply_average_w(average_weight = C_average_weight):
    def apply_average_w(target_average, curr_sequence, return_min, return_max) -> tuple[int, int]:
        curr_avg = sum(curr_sequence) / len(curr_sequence)
        curr_avg_diff = (curr_avg - target_average) / target_average

        mod_min = return_min * (1 + curr_avg_diff * average_weight)       
        mod_max = return_max * (1 - curr_avg_diff * average_weight)

        #print((mod_min, mod_max))
        return (mod_min, mod_max)
    
    return apply_average_w

def get_apply_momentum_w(momentum_weight = C_momentum_weight):
    def apply_momentum_w(target_average, curr_sequence, return_min, return_max) -> tuple[int, int]:
        if len(curr_sequence) <= 0:
            return (return_min, return_max)

        mod_min = return_min * (1 - momentum_weight if curr_sequence[-1] >= 0
                                else 1 + momentum_weight)
        mod_max = return_max * (1 + momentum_weight if curr_sequence[-1] >= 0
                                else 1 - momentum_weight)

        #print((mod_min, mod_max))
        return (mod_min, mod_max)
    
    return apply_momentum_w

C_weight_funcs = [
    get_apply_rand_avg_bias_w(),
    get_apply_average_w(),
    get_apply_momentum_w()
]


def lerp(x, y, w) -> float:
   return  x + w * (y - x)

def roll(sequence: list[int]) -> list[int]:
    res = []
    for num in sequence:
        res.append(res[-1] + num if len(res) > 0 else num)
    return res

def multi_num_roll(num: int, sequence: list[int]) -> list[int]:
    res = []
    for s_num in sequence:
        s_num_multi = s_num / 100
        res.append(res[-1] + (res[-1] * s_num_multi)
                   if len(res) > 0 else num + num * s_num_multi)
    return res

def plot(sequences: list[list[int]], show_black = True):
    if len(sequences) == 2 and len(sequences[0]) == len(sequences[1]):
        fig, ax1 = plt.subplots()
        ax1.plot(sequences[0], color='#10DE94')
        if show_black:
            plt.axhline(0, color='black', linestyle='-', linewidth=1.5)
        
        ax2 = ax1.twinx()
        ax2.plot(sequences[1], color='#FFD700')
        
        fig.tight_layout()
        return plt.show()
    
    for sequence in sequences:
        plt.plot(sequence, color='#10DE94')
    if show_black:
        plt.axhline(0, color='black', linestyle='-', linewidth=1.5)
    plt.show()

def get_sequence(target_average,
                 count,
                 return_min = C_return_min,
                 return_max = C_return_max,
                 weight_funcs = C_weight_funcs) -> list[int]:
    sequence = [random.randint(return_min, return_max)]
    while len(sequence) < count:
        mod_min = return_min       
        mod_max = return_max
        for w_func in weight_funcs:
            w_min, w_max = w_func(target_average, sequence, mod_min, mod_max)
            mod_min = w_min
            mod_max = w_max
        
        avg_needed_num = (target_average * (len(sequence) + 1)) - sum(sequence)
        lerp_weight = 0.0 if len(sequence) / count < 0.5 else 0.1
        lerp_weight = lerp_weight if len(sequence) / count < 0.75 else 0.2
        lerp_weight = lerp_weight if len(sequence) / count < 0.90 else 0.3
        lerped_min = lerp(mod_min, avg_needed_num, (len(sequence) / count) * lerp_weight) 
        lerped_max = lerp(mod_max, avg_needed_num, (len(sequence) / count) * lerp_weight)

        sequence.append(round(random.uniform(lerped_min, lerped_max), 2))

        
    curr_avg = sum(sequence) / len(sequence)
    print(curr_avg)
    
    return sequence


sequence = get_sequence(6, 30)
rolled_seq = roll(sequence)
multi_num_roll_seq = multi_num_roll(100000, sequence)

print(sequence)
print(multi_num_roll_seq)

#plot([sequence])
#plot([rolled_seq])
plot([multi_num_roll_seq], show_black=False)


#sequences = [get_sequence(6, 30) for i in range(10)]
#multi_num_roll_seqs = [multi_num_roll(100000, s) for s in sequences]
#plot(multi_num_roll_seqs, show_black=False)










