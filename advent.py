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

from typing import List, Tuple
from itertools import pairwise
from dataclasses import dataclass

from more_itertools import windowed


def day1(all_depth: List[int]) -> int:
    """
    --- Day 1: Sonar Sweep ---

    As the submarine drops below the surface of the ocean, it automatically
    performs a sonar sweep of the nearby sea floor. On a small screen, the sonar
    sweep report (your puzzle input) appears: each line is a measurement of the
    sea floor depth as the sweep looks further and further away from the
    submarine.

    For example, suppose you had the following report:

    199
    200
    208
    210
    200
    207
    240
    269
    260
    263

    This report indicates that, scanning outward from the submarine, the sonar
    sweep found depths of 199, 200, 208, 210, and so on.

    The first order of business is to figure out how quickly the depth
    increases, just so you know what you're dealing with - you never know if the
    keys will get carried into deeper water by an ocean current or a fish or
    something.

    To do this, count the number of times a depth measurement increases from the
    previous measurement. (There is no measurement before the first
    measurement.) In the example above, the changes are as follows:

    199 (N/A - no previous measurement)
    200 (increased)
    208 (increased)
    210 (increased)
    200 (decreased)
    207 (increased)
    240 (increased)
    269 (increased)
    260 (decreased)
    263 (increased)

    In this example, there are 7 measurements that are larger than the previous
    measurement.

    How many measurements are larger than the previous measurement?
    """
    return len(list(filter(lambda pair: pair[0] < pair[1], pairwise(all_depth))))


def day1_bis(all_depth: List[int]) -> int:
    """
    Considering every single measurement isn't as useful as you expected:
    there's just too much noise in the data.

    Instead, consider sums of a three-measurement sliding window. Again
    considering the above example:

    199  A
    200  A B
    208  A B C
    210    B C D
    200  E   C D
    207  E F   D
    240  E F G
    269    F G H
    260      G H
    263        H

    Start by comparing the first and second three-measurement windows. The
    measurements in the first window are marked A (199, 200, 208); their sum is
    199 + 200 + 208 = 607. The second window is marked B (200, 208, 210); its
    sum is 618. The sum of measurements in the second window is larger than the
    sum of the first, so this first comparison increased.

    Your goal now is to count the number of times the sum of measurements in
    this sliding window increases from the previous sum. So, compare A with B,
    then compare B with C, then C with D, and so on. Stop when there aren't
    enough measurements left to create a new three-measurement sum.

    In the above example, the sum of each three-measurement window is as
    follows:

    A: 607 (N/A - no previous sum)
    B: 618 (increased)
    C: 618 (no change)
    D: 617 (decreased)
    E: 647 (increased)
    F: 716 (increased)
    G: 769 (increased)
    H: 792 (increased)

    In this example, there are 5 sums that are larger than the previous sum.

    Consider sums of a three-measurement sliding window. How many sums are
    larger than the previous sum?
    """
    windowed_depth = windowed(all_depth, 3)
    sum_depth = [sum(w) for w in windowed_depth]
    return day1(sum_depth)


class UnknownCommand(Exception):
    def __init__(self, command: str):
        self.command = command
        super().__init__(f"Unknown command: {command}")


@dataclass
class Command:
    delta_h: int
    delta_d: int

    def __init__(self, com: str, val: int):
        match com:
            case "forward":
                self.delta_h = val
                self.delta_d = 0
            case "down":
                self.delta_h = 0
                self.delta_d = val
            case "up":
                self.delta_h = 0
                self.delta_d = -val
            case _:
                raise UnknownCommand(com)


def day2(commands: List[Command]) -> (int, int):
    """
    --- Day 2: Dive! ---

    Now, you need to figure out how to pilot this thing.

    It seems like the submarine can take a series of commands like forward 1,
    down 2, or up 3:

        forward X increases the horizontal position by X units.
        down X increases the depth by X units.
        up X decreases the depth by X units.

    Note that since you're on a submarine, down and up affect your depth, and so
    they have the opposite result of what you might expect.

    The submarine seems to already have a planned course (your puzzle input).
    You should probably figure out where it's going. For example:

    forward 5
    down 5
    forward 8
    up 3
    down 8
    forward 2

    Your horizontal position and depth both start at 0. The steps above would
    then modify them as follows:

        forward 5 adds 5 to your horizontal position, a total of 5.
        down 5 adds 5 to your depth, resulting in a value of 5.
        forward 8 adds 8 to your horizontal position, a total of 13.
        up 3 decreases your depth by 3, resulting in a value of 2.
        down 8 adds 8 to your depth, resulting in a value of 10.
        forward 2 adds 2 to your horizontal position, a total of 15.

    After following these instructions, you would have a horizontal position of
    15 and a depth of 10. (Multiplying these together produces 150.)

    Calculate the horizontal position and depth you would have after following
    the planned course. What do you get if you multiply your final horizontal
    position by your final depth?
    """
    delta_h = [com.delta_h for com in commands]
    delta_d = [com.delta_d for com in commands]
    return sum(delta_h), sum(delta_d)


def main():
    with open("input_day1.txt") as all_depth:
        all_depth_int = [int(depth) for depth in all_depth if depth != "\n"]

    print("Day 01    :", day1(all_depth_int))
    print("Day 01 bis:", day1_bis(all_depth_int))

    with open("input_day2.txt") as instructions_file:
        instructions = [
            (Command(com, int(val)))
            for com, val in (line.split() for line in instructions_file if line != "\n")
        ]

    h_pos, d_pos = day2(instructions)
    print("Day 02    :", h_pos * d_pos)


if __name__ == "__main__":
    main()
