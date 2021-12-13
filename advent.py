#!/usr/bin/env python3
"""
You're minding your own business on a ship at sea when the overboard alarm goes
off! You rush to see if you can help. Apparently, one of the Elves tripped and
accidentally sent the sleigh keys flying into the ocean!

Before you know it, you're inside a submarine the Elves keep ready for
situations like this. It's covered in Christmas lights (because of course it
is), and it even has an experimental antenna that should be able to track the
keys if you can boost its signal strength high enough; there's a little meter
that indicates the antenna's signal strength by displaying 0-50 stars.

Your instincts tell you that in order to save Christmas, you'll need to get all
fifty stars by December 25th.

Collect stars by solving puzzles. Two puzzles will be made available on each day
in the Advent calendar; the second puzzle is unlocked when you complete the
first. Each puzzle grants one star. Good luck!
"""

import day1
import day2
import day3


def main():
    # Day 1 #################################################################
    with open("input_day1.txt") as all_depth:
        all_depth_int = [int(depth) for depth in all_depth if depth != "\n"]

    print("Day 01    :", day1.day1(all_depth_int))
    print("Day 01 bis:", day1.day1_bis(all_depth_int))

    # Day 2 #################################################################

    with open("input_day2.txt") as commands_file:
        raw_commands = [line.strip() for line in commands_file if line != "\n"]

    commands = [day2.CommandV1(line) for line in raw_commands]

    pos = day2.day2(commands)
    print("Day 02    :", pos.h * pos.d)

    commands_bis = [day2.CommandV2(line) for line in raw_commands]

    pos_bis = day2.day2bis(commands_bis)
    print("Day 02 bis:", pos_bis.h * pos_bis.d)

    # Day 3 #################################################################

    with open("input_day3.txt") as diagnostic_file:
        raw_diagnostic = [line.strip() for line in diagnostic_file if line != "\n"]

    print("Day 03    :")
    diag = day3.day3(raw_diagnostic)
    print(f"\tgamma  : {diag.gamma_binary} -> {diag.gamma}")
    print(f"\tepsilon: {diag.epsilon_binary} -> {diag.epsilon}")
    print(f"\tpower  : {diag.power_consumption()}")

    print("Day 03bis :")
    diag_bis = day3.day3bis(raw_diagnostic)
    print(
        f"\toxygen generator rating : "
        f"{diag_bis.oxygen_generator_binary} -> {diag_bis.oxygen_generator}"
    )
    print(
        f"\tCO2 scrubber rating     : "
        f"{diag_bis.CO2_scrubber_binary} -> {diag_bis.CO2_scrubber}"
    )
    print(f"\tlife support            : {diag_bis.life_support()}")


if __name__ == "__main__":
    main()
