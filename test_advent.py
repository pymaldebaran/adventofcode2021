from assertpy import assert_that, soft_assertions
from assertpy import add_extension as assertpy_add_extension
import numpy as np

import pytest

import day1
import day2
import day3
import day4


@pytest.fixture
def input_day1():
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
            .has_CO2_scrubber(10)
            .has_CO2_scrubber_binary("01010")
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
