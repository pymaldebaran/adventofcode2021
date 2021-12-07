from advent import day1, day1_bis, CommandV1, CommandV2, day2, day2bis, Position

SIMPLE_DAY_1 = [199, 200, 208, 210, 200, 207, 240, 269, 260, 263]


def test_day1_on_simple_exemple():
    assert day1(SIMPLE_DAY_1) == 7


def test_day1bis_on_simple_exemple():
    assert day1_bis(SIMPLE_DAY_1) == 5


SIMPLE_DAY_2_RAW = ["forward 5", "down 5", "forward 8", "up 3", "down 8", "forward 2"]

SIMPLE_DAY_2 = [CommandV1(line) for line in SIMPLE_DAY_2_RAW]
SIMPLE_DAY_2_BIS = [CommandV2(line) for line in SIMPLE_DAY_2_RAW]


def test_day2_on_simple_exemple():
    print(SIMPLE_DAY_2)
    assert day2(SIMPLE_DAY_2) == Position(15, 10)


def test_day2bis_on_simple_exemple():
    assert day2bis(SIMPLE_DAY_2_BIS) == Position(15, 60)
