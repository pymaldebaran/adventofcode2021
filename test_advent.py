"""Test file for the whole Advent of Code 2021 session."""

from collections import Counter
from typing import List

from assertpy import assert_that, soft_assertions
from assertpy import add_extension as assertpy_add_extension
import numpy as np
from more_itertools import padded
import pytest

import day1
import day2
import day3
import day4
import day5
import day6

# pylint: disable=missing-function-docstring
# pylint: disable=redefined-outer-name


@pytest.fixture
def input_day1():
    """Simple input for day 1."""
    return [199, 200, 208, 210, 200, 207, 240, 269, 260, 263]


def test_day1_on_simple_exemple(input_day1):
    assert day1.day1(input_day1) == 7


def test_day1bis_on_simple_exemple(input_day1):
    assert day1.day1_bis(input_day1) == 5


@pytest.fixture
def input_day2_raw():
    return ["forward 5", "down 5", "forward 8", "up 3", "down 8", "forward 2"]


@pytest.fixture
def input_day2(input_day2_raw):
    return [day2.CommandV1(line) for line in input_day2_raw]


@pytest.fixture
def input_day2_bis(input_day2_raw):
    return [day2.CommandV2(line) for line in input_day2_raw]


def test_day2_on_simple_exemple(input_day2):
    assert day2.day2(input_day2) == day2.Position(15, 10)


def test_day2bis_on_simple_exemple(input_day2_bis):
    assert day2.day2bis(input_day2_bis) == day2.Position(15, 60)


@pytest.fixture
def input_day3():
    return [
        "00100",
        "11110",
        "10110",
        "10111",
        "10101",
        "01111",
        "00111",
        "11100",
        "10000",
        "11001",
        "00010",
        "01010",
    ]


def test_day3_on_simple_exemple(input_day3):
    diagnostic = day3.day3(input_day3)
    with soft_assertions():
        (
            assert_that(diagnostic)
            .has_gamma(22)
            .has_gamma_binary("10110")
            .has_epsilon(9)
            .has_epsilon_binary("01001")
            .has_power_consumption(198)
        )


def test_day3bis_on_simple_exemple(input_day3):
    diagnostic = day3.day3bis(input_day3)
    with soft_assertions():
        (
            assert_that(diagnostic)
            .has_oxygen_generator(23)
            .has_oxygen_generator_binary("10111")
            .has_co2_scrubber(10)
            .has_co2_scrubber_binary("01010")
            .has_life_support(230)
        )


@pytest.fixture
def input_day4():
    return """7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7
"""


def test_bingo_can_be_parsed_from_str(input_day4):
    bingo = day4.day4(input_day4)

    with soft_assertions():
        assert_that(bingo.drawn_numbers).is_length(27)
        assert_that(bingo.boards).is_length(3)


def is_array_equal_to(self, other):
    if not np.array_equal(self.val, other):
        return self.error(f"Expected {self.val} to be equal to {other}, but was not.")

    return self


# Wa had a new assertion to assertpy
assertpy_add_extension(is_array_equal_to)


def test_day4_on_simple_example(input_day4):
    bingo = day4.day4(input_day4)

    winning_board = bingo.first_winning_board()

    with soft_assertions():
        assert_that(winning_board).has_winning_number(24)
        (
            assert_that(winning_board.numbers).is_array_equal_to(
                np.array(
                    [
                        [14, 21, 17, 24, 4],
                        [10, 16, 15, 9, 19],
                        [18, 8, 23, 26, 20],
                        [22, 11, 13, 6, 5],
                        [2, 0, 12, 3, 7],
                    ]
                )
            )
        )
        (
            assert_that(winning_board.marked).is_array_equal_to(
                np.array(
                    [
                        [True, True, True, True, True],
                        [False, False, False, True, False],
                        [False, False, True, False, False],
                        [False, True, False, False, True],
                        [True, True, False, False, True],
                    ]
                )
            )
        )
        assert_that(winning_board).has_unmarked_sum(188)
        assert_that(winning_board).has_score(4512)


def test_day4bis_on_simple_example(input_day4):
    bingo = day4.day4(input_day4)

    last_board = bingo.last_winning_board()

    with soft_assertions():
        assert_that(last_board).has_winning_number(13)
        (
            assert_that(last_board.numbers).is_array_equal_to(
                np.array(
                    [
                        [3, 15, 0, 2, 22],
                        [9, 18, 13, 17, 5],
                        [19, 8, 7, 25, 23],
                        [20, 11, 10, 24, 4],
                        [14, 21, 16, 12, 6],
                    ]
                )
            )
        )
        assert_that(last_board).has_unmarked_sum(148)
        assert_that(last_board).has_score(1924)


@pytest.fixture
def input_day5():
    return """0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
"""


def test_day5_on_simple_example(input_day5):
    hydro_map = day5.day5(input_day5)

    assert_that(hydro_map).has_nb_overlaps_hv(5)


def test_day5bis_on_simple_example(input_day5):
    hydro_map = day5.day5(input_day5)

    assert_that(hydro_map).has_nb_overlaps_full(12)


@pytest.fixture
def input_day6() -> str:
    return "3,4,3,1,2"


def raw_po_to_counter(raw_pop: str) -> Counter:
    return Counter([int(val) for val in raw_pop.strip().split(",")])


@pytest.fixture
def expected_counters() -> List[Counter]:
    return [
        raw_po_to_counter(raw)
        for raw in [
            "2,3,2,0,1",
            "1,2,1,6,0,8",
            "0,1,0,5,6,7,8",
            "6,0,6,4,5,6,7,8,8",
            "5,6,5,3,4,5,6,7,7,8",
            "4,5,4,2,3,4,5,6,6,7",
            "3,4,3,1,2,3,4,5,5,6",
            "2,3,2,0,1,2,3,4,4,5",
            "1,2,1,6,0,1,2,3,3,4,8",
            "0,1,0,5,6,0,1,2,2,3,7,8",
            "6,0,6,4,5,6,0,1,1,2,6,7,8,8,8",
            "5,6,5,3,4,5,6,0,0,1,5,6,7,7,7,8,8",
            "4,5,4,2,3,4,5,6,6,0,4,5,6,6,6,7,7,8,8",
            "3,4,3,1,2,3,4,5,5,6,3,4,5,5,5,6,6,7,7,8",
            "2,3,2,0,1,2,3,4,4,5,2,3,4,4,4,5,5,6,6,7",
            "1,2,1,6,0,1,2,3,3,4,1,2,3,3,3,4,4,5,5,6,8",
            "0,1,0,5,6,0,1,2,2,3,0,1,2,2,2,3,3,4,4,5,7,8",
            "6,0,6,4,5,6,0,1,1,2,6,0,1,1,1,2,2,3,3,4,6,7,8,8,8,8",
        ]
    ]


def test_day6_on_simple_example(input_day6, expected_counters):
    population = day6.day6(input_day6)

    assert_that(population.counter).is_equal_to(raw_po_to_counter(input_day6))

    for day, expected in enumerate(padded(expected_counters, None, 80)):
        population.evolve()

        if expected:
            assert_that(population.counter).is_equal_to(expected)
        if day + 1 == 18:
            assert_that(population.counter.total()).is_equal_to(26)

    assert_that(population.counter.total()).is_equal_to(5934)
