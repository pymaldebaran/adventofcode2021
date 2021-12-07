from advent import day1, day1_bis, Command, day2

SIMPLE_DAY_1 = [199, 200, 208, 210, 200, 207, 240, 269, 260, 263]


def test_day1_on_simple_exemple():
    assert day1(SIMPLE_DAY_1) == 7


def test_day1bis_on_simple_exemple():
    assert day1_bis(SIMPLE_DAY_1) == 5


SIMPLE_DAY_2 = [
    Command("forward", 5),
    Command("down", 5),
    Command("forward", 8),
    Command("up", 3),
    Command("down", 8),
    Command("forward", 2),
]


def test_day2_on_simple_exemple():
    assert day2(SIMPLE_DAY_2) == (15, 10)
