import math
import random
import matplotlib.pyplot as plt

C_return_min = -25
C_return_max = 25

C_rand_avg_bias_chance = 0.5
C_average_weight = 0.25
C_momentum_weight = 0.15


def get_apply_rand_avg_bias_w(rand_avg_bias_chance=C_rand_avg_bias_chance):
    def apply_rand_avg_bias_w(
        target_average, curr_sequence, return_min, return_max
    ) -> tuple[int, int]:
        if random.random() > rand_avg_bias_chance:
            return (return_min, return_max)

        return (return_min + target_average * 2, return_max + target_average * 2)

    return apply_rand_avg_bias_w


def get_apply_average_w(average_weight=C_average_weight):
    def apply_average_w(
        target_average, curr_sequence, return_min, return_max
    ) -> tuple[int, int]:
        curr_avg = sum(curr_sequence) / len(curr_sequence)
        curr_avg_diff = (curr_avg - target_average) / target_average

        mod_min = return_min * (1 + curr_avg_diff * average_weight)
        mod_max = return_max * (1 - curr_avg_diff * average_weight)

        # print((mod_min, mod_max))
        return (mod_min, mod_max)

    return apply_average_w


def get_apply_momentum_w(momentum_weight=C_momentum_weight):
    def apply_momentum_w(
        target_average, curr_sequence, return_min, return_max
    ) -> tuple[int, int]:
        if len(curr_sequence) <= 0:
            return (return_min, return_max)

        mod_min = return_min * (
            1 - momentum_weight if curr_sequence[-1] >= 0 else 1 + momentum_weight
        )
        mod_max = return_max * (
            1 + momentum_weight if curr_sequence[-1] >= 0 else 1 - momentum_weight
        )

        # print((mod_min, mod_max))
        return (mod_min, mod_max)

    return apply_momentum_w


C_weight_funcs = [
    get_apply_rand_avg_bias_w(),
    get_apply_average_w(),
    get_apply_momentum_w(),
]


def plot(
    sequences: list[list[float] | list[int]],
    show_black=True,
    colors: list[str] = ["#10DE94", "#FFD700", "#82C8E5"],
):
    if len(sequences) == 2 and len(sequences[0]) == len(sequences[1]):
        fig, ax1 = plt.subplots()
        ax1.plot(sequences[0], color=colors[0])
        if show_black:
            plt.axhline(0, color="black", linestyle="-", linewidth=1.5)

        ax2 = ax1.twinx()
        ax2.plot(sequences[1], color=colors[1])

        fig.tight_layout()
        return plt.show()

    for i, sequence in enumerate(sequences):
        plt.plot(sequence, color=colors[i] if i < len(colors) else colors[-1])
    if show_black:
        plt.axhline(0, color="black", linestyle="-", linewidth=1.5)
    plt.show()


def lerp(x, y, w) -> float:
    return x + w * (y - x)


def get_sequence(
    target_average,
    count,
    return_min=C_return_min,
    return_max=C_return_max,
    weight_funcs=C_weight_funcs,
) -> list[float]:
    sequence = [round(random.uniform(return_min, return_max), 2)]
    while len(sequence) < count:
        mod_min = return_min
        mod_max = return_max
        for w_func in weight_funcs:
            w_min, w_max = w_func(target_average, sequence, mod_min, mod_max)
            mod_min = w_min
            mod_max = w_max

        avg_needed_num = (target_average * (len(sequence) + 1)) - sum(sequence)
        lerp_weight = 0.0 if len(sequence) / count < 0.5 else 0.15
        lerp_weight = lerp_weight if len(sequence) / count < 0.75 else 0.25
        lerp_weight = lerp_weight if len(sequence) / count < 0.90 else 0.35
        lerped_min = lerp(
            mod_min, avg_needed_num, (len(sequence) / count) * lerp_weight
        )
        lerped_max = lerp(
            mod_max, avg_needed_num, (len(sequence) / count) * lerp_weight
        )

        sequence.append(round(random.uniform(lerped_min, lerped_max), 2))

    # curr_avg = sum(sequence) / len(sequence)
    # print(curr_avg)

    return sequence


def roll(sequence: list[float]) -> list[float]:
    res = []
    for num in sequence:
        res.append(res[-1] + num if len(res) > 0 else num)
    return res


def multi_num_roll(
    init_num: int, sequence: list[float], num_modify_funcs=[]
) -> list[int]:
    res = []
    for s_num in sequence:
        mod_num = res[-1] if len(res) > 0 else init_num
        for m_func in num_modify_funcs:
            mod_num = m_func(mod_num, s_num, sequence)

        s_num_multi = s_num / 100
        res.append(mod_num + (mod_num * s_num_multi))
    return res


def get_add_num_func(add_amount: int):
    def add_num_func(num: int, s_num: int, sequence: list[int]) -> int:
        return num + add_amount if num > 0 else num

    return add_num_func


def get_remove_num_func(remove_amount: int):
    def remove_num_func(num: int, s_num: int, sequence: list[int]) -> int:
        return num - remove_amount if num > 0 else num

    return remove_num_func


def get_remove_num_adjusted_func(
    remove_amount: int, adjust_multi: float, saved_data: dict[str, float]
):
    def remove_num_adjusted_func(num: int, s_num: int, sequence: list[float]) -> float:
        adjusted_remove = remove_amount
        seq_pos = sequence.index(s_num)
        if s_num < 0:
            adjusted_remove *= 1 - adjust_multi
        elif s_num >= 5 and (seq_pos >= 1 and sequence[seq_pos - 1] > 0):
            adjusted_remove *= 1 + adjust_multi

        saved_data["total_removed"] = (
            saved_data.get("total_removed", 0) + adjusted_remove
        )
        return num - adjusted_remove if num > 0 else num

    return remove_num_adjusted_func


def get_adjusted_removal_advnaced_func(
    remove_amount: int,
    adjust_multi: dict[int, dict[int, float]],
    adjust_default: float,
    saved_data: dict[str, float],
):
    def adjusted_removal_advnaced_func(
        num: int, s_num: int, sequence: list[float]
    ) -> float:
        adjusted_remove = remove_amount
        seq_pos = sequence.index(s_num)

        adjust_multi_num = adjust_default

        count_adjust_multi = adjust_multi.get(
            max(
                (key for key in adjust_multi.keys() if key >= 0 and key < seq_pos),
                default=0,
            ),
            None,
        )
        if count_adjust_multi:
            adjust_multi_num = count_adjust_multi.get(round(s_num), None)
            if not adjust_multi_num:
                if s_num >= 0:
                    adjust_multi_num = count_adjust_multi.get(
                        max(
                            (
                                key
                                for key in count_adjust_multi.keys()
                                if key >= 0 and key < s_num
                            ),
                            default=0,
                        ),
                        adjust_default,
                    )
                if s_num < 0:
                    adjust_multi_num = count_adjust_multi.get(
                        min(
                            (
                                key
                                for key in count_adjust_multi.keys()
                                if key < 0 and key > s_num
                            ),
                            default=0,
                        ),
                        adjust_default,
                    )

        if s_num < 0:
            adjusted_remove *= 1 - (adjust_multi_num or adjust_default)
        elif s_num >= 0 and (
            seq_pos >= 2 and sequence[seq_pos - 1] > 0 and sequence[seq_pos - 2] > 0
        ):
            adjusted_remove *= 1 + (adjust_multi_num or adjust_default)

        saved_data["total_removed"] = (
            saved_data.get("total_removed", 0) + adjusted_remove
        )
        return num - adjusted_remove if num > 0 else num

    return adjusted_removal_advnaced_func


def get_adjusted_percent_removal_func(
    minimum_remove: int,
    remove_percents: dict[int, dict[int, float]],
    default_remove_percent: float,
    saved_data: dict[str, float],
):
    def adjusted_percent_removal_func(
        num: int, s_num: int, sequence: list[float]
    ) -> float:
        seq_pos = sequence.index(s_num)
        count_remove_percents = remove_percents.get(
            max(
                (key for key in remove_percents.keys() if key >= 0 and key < seq_pos),
                default=0,
            ),
            None,
        )

        remove_percentage = default_remove_percent
        if count_remove_percents:
            remove_percentage = count_remove_percents.get(round(s_num), None)
            if not remove_percentage:
                if s_num >= 0:
                    remove_percentage = count_remove_percents.get(
                        max(
                            (
                                key
                                for key in count_remove_percents.keys()
                                if key >= 0 and key < s_num
                            ),
                            default=0,
                        ),
                        default_remove_percent,
                    )
                if s_num < 0:
                    remove_percentage = count_remove_percents.get(
                        min(
                            (
                                key
                                for key in count_remove_percents.keys()
                                if key < 0 and key > s_num
                            ),
                            default=0,
                        ),
                        default_remove_percent,
                    )

        adjusted_remove = max(
            num * ((remove_percentage or default_remove_percent) / 100), minimum_remove
        )
        saved_data["total_removed"] = (
            saved_data.get("total_removed", 0) + adjusted_remove
        )
        return num - adjusted_remove if num > 0 else num

    return adjusted_percent_removal_func


def get_percent_hit_zero_func():
    def percent_hit_zero_func(
        sequences: list[list[float]], multi_num_roll_seqs: list[list[float]]
    ) -> dict[str, float]:
        return {
            "percent_hit_zero": (
                sum(any(n <= 0 for n in seq) for seq in multi_num_roll_seqs)
                / len(multi_num_roll_seqs)
            )
            * 100
        }

    return percent_hit_zero_func


def get_sequence_averages_func():
    def percent_hit_zero_func(
        sequences: list[list[float]], multi_num_roll_seqs: list[list[float]]
    ) -> dict[str, float]:
        return {
            "sequence_avg_avg": round(
                sum(sum(seq) / len(seq) for seq in sequences) / len(sequences), 2
            ),
            "sequence_avg_min": round(min(sum(seq) / len(seq) for seq in sequences), 2),
            "sequence_avg_max": round(max(sum(seq) / len(seq) for seq in sequences), 2),
        }

    return percent_hit_zero_func


sequence = get_sequence(5.5, 30)
rolled_seq = roll(sequence)

saved_data = {}
multi_num_roll_seq = multi_num_roll(
    100000,
    sequence,
    [
        # get_remove_num_func(7500)
        get_remove_num_adjusted_func(4000, 0.25, saved_data)
    ],
)
# print("final", saved_data)

# print(sequence)
# print(multi_num_roll_seq)

# plot([sequence])
# plot([rolled_seq])
# plot([multi_num_roll_seq], show_black=False)


# sequences = [get_sequence(5.5, 30) for i in range(10)]
# multi_num_roll_seqs = [multi_num_roll(100000, s) for s in sequences]
# plot(multi_num_roll_seqs, show_black=False)


def simulate_sequences(
    init_num: int,
    target_average: float,
    count: int,
    seq_count=100,
    exclude_percent=1,
    num_modify_funcs=[],
    stat_funcs=[],
) -> tuple[
    dict[str, list[float] | list[int]], dict[int, dict[str, float]], dict[str, float]
]:
    sequences = [get_sequence(target_average, count) for i in range(seq_count)]

    sequences.sort(key=lambda seq: sum(seq) / len(seq))
    exclude_num = round(len(sequences) * (exclude_percent / 100))
    sequences = sequences[exclude_num : len(sequences) - exclude_num]

    multi_num_roll_seqs = [
        multi_num_roll(init_num, s, num_modify_funcs) for s in sequences
    ]

    custom_stats = {}
    for stat_func in stat_funcs:
        custom_stats |= stat_func(sequences, multi_num_roll_seqs)

    avg_of_seqs = [
        sum([seq[i] for seq in multi_num_roll_seqs]) / seq_count for i in range(count)
    ]
    largest_final_seq = max(multi_num_roll_seqs, key=lambda seq: seq[-1])
    smallest_final_seq = min(multi_num_roll_seqs, key=lambda seq: seq[-1])

    count_stats = {
        c
        * 5: {
            "avg": sum([seq[c * 5] for seq in multi_num_roll_seqs]) / seq_count,
            "largest": max([seq[c * 5] for seq in multi_num_roll_seqs]),
            "smallest": min([seq[c * 5] for seq in multi_num_roll_seqs]),
        }
        for c in range(count // 5)
    }
    count_stats.setdefault(
        count,
        {
            "avg": sum([seq[-1] for seq in multi_num_roll_seqs]) / seq_count,
            "largest": max([seq[-1] for seq in multi_num_roll_seqs]),
            "smallest": min([seq[-1] for seq in multi_num_roll_seqs]),
        },
    )

    return (
        {
            "avg_of_seqs": avg_of_seqs,
            "largest_final_seq": largest_final_seq,
            "smallest_final_seq": smallest_final_seq,
        },
        count_stats,
        custom_stats,
    )


def main():
    # return
    saved_data = {}
    seqs_data, count_stats, custom_stats = simulate_sequences(
        100000,
        5.0,
        15,
        seq_count=10000,
        exclude_percent=2,
        num_modify_funcs=[
            # get_add_num_func(10000),
            # get_remove_num_func(10000),
            # get_remove_num_adjusted_func(12000, 0.35, saved_data),
            # get_adjusted_removal_advnaced_func(12000,
            #                               {0: {-15: 1.0, -10: 1.0, -5: 1.0, -1: 1.0},
            #                                3: {-15: 0.5, -10: 0.5, -5: 0.2, 5: 0.0, 10: 0.0, 15: 0.4},
            #                                10: {-15: 0.3, -10: 0.2, 1: 0.0, 5: 0.0, 10: 0.4, 15: 0.6},
            #                                20: {-15: 0.2, -10: 0.1, 1: 0.2, 5: 0.4, 10: 0.6, 15: 0.8}
            #                               }, 0.0, saved_data)
            # get_adjusted_percent_removal_func(8000, {
            #                                0: {-15: 1.0, -10: 1.0, -5: 1.0, -1: 1.0},
            #                                3: {-15: 3.0, -10: 3.5, -5: 4.0, 5: 5.5, 10: 5.5, 15: 6.0},
            #                                10: {-15: 4.0, -10: 4.0, -5: 4.5, 5: 8.0, 10: 9.0, 15: 10.0},
            #                                }, 5.0, saved_data)
        ],
        stat_funcs=[
            get_sequence_averages_func(),
            # get_percent_hit_zero_func()
        ],
    )

    print("saved_data", saved_data)
    print("count_stats", count_stats[list(count_stats)[-1]])
    print("custom_stats", custom_stats)
    plot(
        [*seqs_data.values()], show_black=True, colors=["#FFD700", "#10DE94", "#FF6961"]
    )


main()
