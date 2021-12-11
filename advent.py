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
from collections import Counter

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


@dataclass
class Position:
    h: int
    d: int


class UnknownCommand(Exception):
    def __init__(self, command: str):
        self.command = command
        super().__init__(f"Unknown command: {command}")


@dataclass
class CommandV1:
    delta_h: int
    delta_d: int

    def __init__(self, raw_command: str):
        label, val = raw_command.split()
        match label:
            case "forward":
                self.delta_h = int(val)
                self.delta_d = 0
            case "down":
                self.delta_h = 0
                self.delta_d = int(val)
            case "up":
                self.delta_h = 0
                self.delta_d = -int(val)
            case _:
                raise UnknownCommand(com)


@dataclass
class CommandV2:
    label: str
    val: int

    def __init__(self, raw_command: str):
        label, val = raw_command.split()
        self.label = label
        self.val = int(val)


def day2(commands: List[CommandV1]) -> (int, int):
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
    return Position(sum(delta_h), sum(delta_d))


def day2bis(commands: List[CommandV2]) -> (int, int):
    """
    Based on your calculations, the planned course doesn't seem to make any
    sense. You find the submarine manual and discover that the process is
    actually slightly more complicated.

    In addition to horizontal position and depth, you'll also need to track a
    third value, aim, which also starts at 0. The commands also mean something
    entirely different than you first thought:

        down X increases your aim by X units.
        up X decreases your aim by X units.
        forward X does two things:
            It increases your horizontal position by X units.
            It increases your depth by your aim multiplied by X.

    Again note that since you're on a submarine, down and up do the opposite of
    what you might expect: "down" means aiming in the positive direction.

    Now, the above example does something different:

        forward 5 adds 5 to your horizontal position, a total of 5. Because your aim is 0, your depth does not change.
        down 5 adds 5 to your aim, resulting in a value of 5.
        forward 8 adds 8 to your horizontal position, a total of 13. Because your aim is 5, your depth increases by 8*5=40.
        up 3 decreases your aim by 3, resulting in a value of 2.
        down 8 adds 8 to your aim, resulting in a value of 10.
        forward 2 adds 2 to your horizontal position, a total of 15. Because your aim is 10, your depth increases by 2*10=20 to a total of 60.

    After following these new instructions, you would have a horizontal position
    of 15 and a depth of 60. (Multiplying these produces 900.)

    Using this new interpretation of the commands, calculate the horizontal
    position and depth you would have after following the planned course. What
    do you get if you multiply your final horizontal position by your final
    depth?
    """
    aim = 0
    pos = Position(0, 0)

    for com in commands:
        match com.label:
            case "down":
                aim += com.val
            case "up":
                aim -= com.val
            case "forward":
                pos.h += com.val
                pos.d += aim * com.val
            case _:
                raise UnknownCommand(com)

    return pos


@dataclass
class DiagnosticReport:
    gamma_binary: str

    @property
    def epsilon_binary(self) -> str:
        return bit_not_str(self.gamma_binary)

    @property
    def gamma(self) -> int:
        return int(self.gamma_binary, base=2)

    @property
    def epsilon(self) -> int:
        return int(self.epsilon_binary, base=2)

    def power_consumption(self) -> int:
        return self.gamma * self.epsilon


def bit_not_str(number: str) -> str:
    """
    Example:

        >>> bit_not_str('110011')
        '001100'

        >>> bit_not_str('01010101')
        '10101010'

        >>> bit_not_str('111')
        '000'
    """
    return ''.join([str(int(not int(c, base=2))) for c in number])

def bit_not(n, numbits) -> int:
    """
    See: https://stackoverflow.com/a/31151236

    Example:

        >>> bit_not(0b101, 3) == 0b010
        True

        >>> bit_not(0b10101011, 8) == 0b01010100
        True
    """
    return (1 << numbits) - 1 - n


def lines_to_cols(lines: List[str]) -> List[str]:
    """
    Transpose a matrix like list of string by returning the corresponding
    list of columns.

    Example:

        >>> lines_to_cols(['ABC', 'DEF'])
        ['AD', 'BE', 'CF']
    """
    return [''.join(col) for col in zip(*lines)]

def most_common_chars_in_cols(cols: List[str]) -> str:
    """
    Return the most common char of each columns.

    Args:
        cols: a list of strings representing the columns

    Returns:
        a string with each char being the most common one of the corresponding
        column.

    Example:
        >>> most_common_chars_in_cols(['AAAB', 'BBBA', 'ABBB', 'BAAA', 'BABB'])
        'ABBAB'
    """
    return ''.join([Counter(col).most_common(1)[0][0] for col in cols])

def day3(diagnostics: List[str]) -> DiagnosticReport:
    """
    --- Day 3: Binary Diagnostic ---

    The submarine has been making some odd creaking noises, so you ask it to
    produce a diagnostic report just in case.

    The diagnostic report (your puzzle input) consists of a list of binary
    numbers which, when decoded properly, can tell you many useful things about
    the conditions of the submarine. The first parameter to check is the power
    consumption.

    You need to use the binary numbers in the diagnostic report to generate two
    new binary numbers (called the gamma rate and the epsilon rate). The power
    consumption can then be found by multiplying the gamma rate by the epsilon
    rate.

    Each bit in the gamma rate can be determined by finding the most common bit
    in the corresponding position of all numbers in the diagnostic report. For
    example, given the following diagnostic report:

    00100
    11110
    10110
    10111
    10101
    01111
    00111
    11100
    10000
    11001
    00010
    01010

    Considering only the first bit of each number, there are five 0 bits and
    seven 1 bits. Since the most common bit is 1, the first bit of the gamma
    rate is 1.

    The most common second bit of the numbers in the diagnostic report is 0, so
    the second bit of the gamma rate is 0.

    The most common value of the third, fourth, and fifth bits are 1, 1, and 0,
    respectively, and so the final three bits of the gamma rate are 110.

    So, the gamma rate is the binary number 10110, or 22 in decimal.

    The epsilon rate is calculated in a similar way; rather than use the most
    common bit, the least common bit from each position is used. So, the epsilon
    rate is 01001, or 9 in decimal. Multiplying the gamma rate (22) by the
    epsilon rate (9) produces the power consumption, 198.

    Use the binary numbers in your diagnostic report to calculate the gamma rate
    and epsilon rate, then multiply them together. What is the power consumption
    of the submarine? (Be sure to represent your answer in decimal, not binary.)
    """
    diagnostic_cols = lines_to_cols(diagnostics)

    most_commons = most_common_chars_in_cols(diagnostic_cols)

    return DiagnosticReport(gamma_binary=most_commons)


def main():
    # Day 1 #################################################################
    with open("input_day1.txt") as all_depth:
        all_depth_int = [int(depth) for depth in all_depth if depth != "\n"]

    print("Day 01    :", day1(all_depth_int))
    print("Day 01 bis:", day1_bis(all_depth_int))

    # Day 2 #################################################################

    with open("input_day2.txt") as commands_file:
        raw_commands = [line.strip() for line in commands_file if line != "\n"]

    commands = [CommandV1(line) for line in raw_commands]

    pos = day2(commands)
    print("Day 02    :", pos.h * pos.d)

    commands_bis = [CommandV2(line) for line in raw_commands]

    pos_bis = day2bis(commands_bis)
    print("Day 02 bis:", pos_bis.h * pos_bis.d)

    # Day 3 #################################################################

    with open("input_day3.txt") as diagnostic_file:
        raw_diagnostic = [line.strip() for line in diagnostic_file if line != "\n"]

    print("Day 03    :")
    diagnostic = day3(raw_diagnostic)
    print(f"\tgamma  : {diagnostic.gamma_binary} -> {diagnostic.gamma}")
    print(f"\tepsilon: {diagnostic.epsilon_binary} -> {diagnostic.epsilon}")
    print(f"\tpower  : {diagnostic.power_consumption()}")


if __name__ == "__main__":
    main()
