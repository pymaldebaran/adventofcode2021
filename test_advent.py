from advent import day1, day1_bis

SIMPLE_DAY_1 = [
        199,
        200,
        208,
        210,
        200,
        207,
        240,
        269,
        260,
        263
    ]

def test_day1_on_simple_exemple():
    assert day1(SIMPLE_DAY_1) == 7

def test_day1bis_on_simple_exemple():
    assert day1_bis(SIMPLE_DAY_1) == 5
