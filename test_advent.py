from assertpy import assert_that, soft_assertions

import day1
import day2
import day3

SIMPLE_DAY_1 = [199, 200, 208, 210, 200, 207, 240, 269, 260, 263]


def test_day1_on_simple_exemple():
    assert day1.day1(SIMPLE_DAY_1) == 7


def test_day1bis_on_simple_exemple():
    assert day1.day1_bis(SIMPLE_DAY_1) == 5


SIMPLE_DAY_2_RAW = ["forward 5", "down 5", "forward 8", "up 3", "down 8", "forward 2"]

SIMPLE_DAY_2 = [day2.CommandV1(line) for line in SIMPLE_DAY_2_RAW]
SIMPLE_DAY_2_BIS = [day2.CommandV2(line) for line in SIMPLE_DAY_2_RAW]


def test_day2_on_simple_exemple():
    print(SIMPLE_DAY_2)
    assert day2.day2(SIMPLE_DAY_2) == day2.Position(15, 10)


def test_day2bis_on_simple_exemple():
    assert day2.day2bis(SIMPLE_DAY_2_BIS) == day2.Position(15, 60)


SIMPLE_DAY_3 = [
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


def test_day3_on_simple_exemple():
    diagnostic = day3.day3(SIMPLE_DAY_3)
    with soft_assertions():
        (
            assert_that(diagnostic)
            .has_gamma(22)
            .has_gamma_binary("10110")
            .has_epsilon(9)
            .has_epsilon_binary("01001")
            .has_power_consumption(198)
        )


def test_day3bis_on_simple_exemple():
    diagnostic = day3.day3bis(SIMPLE_DAY_3)
    with soft_assertions():
        (
            assert_that(diagnostic)
            .has_oxygen_generator(23)
            .has_oxygen_generator_binary("10111")
            .has_CO2_scrubber(10)
            .has_CO2_scrubber_binary("01010")
            .has_life_support(230)
        )
