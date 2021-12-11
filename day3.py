from typing import List, Tuple
from dataclasses import dataclass
from collections import Counter


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
    return "".join([str(int(not int(c, base=2))) for c in number])


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
    return ["".join(col) for col in zip(*lines)]


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
    return "".join([Counter(col).most_common(1)[0][0] for col in cols])


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
