"""
Day 3: Binary Diagnostic.

The submarine has been making some odd creaking noises, so you ask it to produce
a diagnostic report just in case.

The diagnostic report (your puzzle input) consists of a list of binary numbers
which, when decoded properly, can tell you many useful things about the
conditions of the submarine. The first parameter to check is the power
consumption.

You need to use the binary numbers in the diagnostic report to generate two new
binary numbers (called the gamma rate and the epsilon rate). The power
consumption can then be found by multiplying the gamma rate by the epsilon rate.

Each bit in the gamma rate can be determined by finding the most common bit in
the corresponding position of all numbers in the diagnostic report. For example,
given the following diagnostic report:

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

Considering only the first bit of each number, there are five 0 bits and seven 1
bits. Since the most common bit is 1, the first bit of the gamma rate is 1.

The most common second bit of the numbers in the diagnostic report is 0, so the
second bit of the gamma rate is 0.

The most common value of the third, fourth, and fifth bits are 1, 1, and 0,
respectively, and so the final three bits of the gamma rate are 110.

So, the gamma rate is the binary number 10110, or 22 in decimal.

The epsilon rate is calculated in a similar way; rather than use the most common
bit, the least common bit from each position is used. So, the epsilon rate is
01001, or 9 in decimal. Multiplying the gamma rate (22) by the epsilon rate (9)
produces the power consumption, 198.

Use the binary numbers in your diagnostic report to calculate the gamma rate and
epsilon rate, then multiply them together. What is the power consumption of the
submarine? (Be sure to represent your answer in decimal, not binary.)

--- Part Two ---

Next, you should verify the life support rating, which can be determined by
multiplying the oxygen generator rating by the CO2 scrubber rating.

Both the oxygen generator rating and the CO2 scrubber rating are values that can
be found in your diagnostic report - finding them is the tricky part. Both
values are located using a similar process that involves filtering out values
until only one remains. Before searching for either rating value, start with the
full list of binary numbers from your diagnostic report and consider just the
first bit of those numbers. Then:

-   Keep only numbers selected by the bit criteria for the type of rating value
    for which you are searching. Discard numbers which do not match the bit
    criteria.
-   If you only have one number left, stop; this is the rating value for which
    you are searching.
-   Otherwise, repeat the process, considering the next bit to the right.

The bit criteria depends on which type of rating value you want to find:

-   To find oxygen generator rating, determine the most common value (0 or
    1) in the current bit position, and keep only numbers with that bit in that
    position. If 0 and 1 are equally common, keep values with a 1 in the
    position being considered.
-   To find CO2 scrubber rating, determine the least common value (0 or 1) in
    the current bit position, and keep only numbers with that bit in that
    position. If 0 and 1 are equally common, keep values with a 0 in the
    position being considered.

For example, to determine the oxygen generator rating value using the same
example diagnostic report from above:

-   Start with all 12 numbers and consider only the first bit of each number.
    There are more 1 bits (7) than 0 bits (5), so keep only the 7 numbers with a
    1 in the first position: 11110, 10110, 10111, 10101, 11100, 10000, and
    11001.
-   Then, consider the second bit of the 7 remaining numbers: there are more 0
    bits (4) than 1 bits (3), so keep only the 4 numbers with a 0 in the second
    position: 10110, 10111, 10101, and 10000.
-   In the third position, three of the four numbers have a 1, so keep those
    three: 10110, 10111, and 10101.
-   In the fourth position, two of the three numbers have a 1, so keep those
    two: 10110 and 10111.
-   In the fifth position, there are an equal number of 0 bits and 1 bits (one
    each). So, to find the oxygen generator rating, keep the number with a 1 in
    that position: 10111.
-   As there is only one number left, stop; the oxygen generator rating is
    10111, or 23 in decimal.

Then, to determine the CO2 scrubber rating value from the same example above:

-   Start again with all 12 numbers and consider only the first bit of each
    number. There are fewer 0 bits (5) than 1 bits (7), so keep only the 5
    numbers with a 0 in the first position: 00100, 01111, 00111, 00010, and
    01010.
-   Then, consider the second bit of the 5 remaining numbers: there are fewer 1
    bits (2) than 0 bits (3), so keep only the 2 numbers with a 1 in the second
    position: 01111 and 01010.
-   In the third position, there are an equal number of 0 bits and 1 bits (one
    each). So, to find the CO2 scrubber rating, keep the number with a 0 in that
    position: 01010.
-   As there is only one number left, stop; the CO2 scrubber rating is 01010, or
    10 in decimal.

Finally, to find the life support rating, multiply the oxygen generator rating
(23) by the CO2 scrubber rating (10) to get 230.

Use the binary numbers in your diagnostic report to calculate the oxygen
generator rating and CO2 scrubber rating, then multiply them together. What is
the life support rating of the submarine? (Be sure to represent your answer in
decimal, not binary.)
"""

from typing import List
from dataclasses import dataclass
from collections import Counter


@dataclass
class DiagnosticReport:
    """Represent a health diagnostic report of the submarine."""

    gamma_binary: str

    @property
    def epsilon_binary(self) -> str:
        """Get the binary representation of epsilon."""
        return bit_not_str(self.gamma_binary)

    @property
    def gamma(self) -> int:
        """Get the decimal value of gamma."""
        return int(self.gamma_binary, base=2)

    @property
    def epsilon(self) -> int:
        """Get the decimal value of epsilon."""
        return int(self.epsilon_binary, base=2)

    def power_consumption(self) -> int:
        """Compute the power consumption of the submarine."""
        return self.gamma * self.epsilon


def bit_not_str(number: str) -> str:
    """
    Compute a binary not on a serie on bit represented as a string.

    Example:
        >>> bit_not_str('110011')
        '001100'

        >>> bit_not_str('01010101')
        '10101010'

        >>> bit_not_str('111')
        '000'
    """
    return "".join([str(int(not int(c, base=2))) for c in number])


def bit_not(bits, numbits) -> int:
    """
    Compute et binary not.

    See: https://stackoverflow.com/a/31151236

    Example:
        >>> bit_not(0b101, 3) == 0b010
        True

        >>> bit_not(0b10101011, 8) == 0b01010100
        True
    """
    return (1 << numbits) - 1 - bits


def lines_to_cols(lines: List[str]) -> List[str]:
    """
    Transpose a matrix-like list of string.

    It does so by returning the corresponding list of columns.

    Example:
        >>> lines_to_cols(['ABC', 'DEF'])
        ['AD', 'BE', 'CF']
    """
    return ["".join(col) for col in zip(*lines)]


def least_common_char(chars: str, default_to: str | None = None):
    """
    Return the least common char of the provided string.

    Args:
    - chars: the string to search the char in
    - default_to: the char to return if ever there is a tie for the first place

    Returns:
        the least common char

    Examples:
        >>> least_common_char('AAABB')
        'B'
        >>> least_common_char('AABBB')
        'A'
        >>> least_common_char('AABB', 'B')
        'B'
        >>> least_common_char('AABB', 'A')
        'A'
    """
    counter = Counter(chars)
    if default_to is None:
        return counter.most_common(2)[1][0]

    _most_common_c, most_common_v = counter.most_common(2)[0]
    least_common_c, least_common_v = counter.most_common(2)[1]

    if most_common_v == least_common_v:
        return default_to

    return least_common_c


def most_common_char(chars: str, default_to: str | None = None):
    """
    Return the most common char of the provided string.

    Args:
    - chars: the string to search the char in
    - default_to: the char to return if ever there is a tie for the first place

    Returns:
        the most common char

    Examples:
        >>> most_common_char('AAABB')
        'A'
        >>> most_common_char('AABBB')
        'B'
        >>> most_common_char('AABB', 'B')
        'B'
        >>> most_common_char('AABB', 'A')
        'A'
    """
    counter = Counter(chars)
    if default_to is None:
        return counter.most_common(1)[0][0]

    most_common_c, most_common_v = counter.most_common(2)[0]
    _least_common_c, least_common_v = counter.most_common(2)[1]

    if most_common_v == least_common_v:
        return default_to

    return most_common_c


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
    return "".join([most_common_char(col) for col in cols])


def day3(diagnostics: List[str]) -> DiagnosticReport:
    """Solve day 3 puzzle part 1."""
    diagnostic_cols = lines_to_cols(diagnostics)

    most_commons = most_common_chars_in_cols(diagnostic_cols)

    return DiagnosticReport(gamma_binary=most_commons)


@dataclass
class AdvancedDiagnosticReport(DiagnosticReport):
    """Represent a improved health diagnostic report of the submarine."""

    oxygen_generator_binary: str
    co2_scrubber_binary: str

    @property
    def oxygen_generator(self) -> int:
        """Get the oxygen generator value in decimal."""
        return int(self.oxygen_generator_binary, base=2)

    @property
    def co2_scrubber(self) -> int:
        """Get the C02 scrubber value in decimal."""
        return int(self.co2_scrubber_binary, base=2)

    def life_support(self) -> int:
        """Get the global life support for the submarine."""
        return self.oxygen_generator * self.co2_scrubber


def day3bis(diagnostics: List[str]) -> AdvancedDiagnosticReport:
    """Solve day 3 puzzle part 2."""
    limited_report = day3(diagnostics)

    cols = lines_to_cols(diagnostics)

    possible_oxy_gen = diagnostics[:]
    for idx, _ in enumerate(cols):
        diagnostic_cols = lines_to_cols(possible_oxy_gen)
        col = diagnostic_cols[idx]

        possible_oxy_gen = [
            bits
            for bits in possible_oxy_gen
            if bits[idx] == most_common_char(col, default_to="1")
        ]

        if len(possible_oxy_gen) == 1:
            break
    else:
        assert False, "No oxygen generator rating found"

    oxygen_generator_binary = possible_oxy_gen[0]

    possible_co2_scr = diagnostics[:]
    for idx, _ in enumerate(cols):
        diagnostic_cols = lines_to_cols(possible_co2_scr)
        col = diagnostic_cols[idx]
        possible_co2_scr = [
            bits
            for bits in possible_co2_scr
            if bits[idx] == least_common_char(col, default_to="0")
        ]

        if len(possible_co2_scr) == 1:
            break
    else:
        assert False, "No oxygen generator rating found"

    co2_scrubber_binary = possible_co2_scr[0]

    return AdvancedDiagnosticReport(
        gamma_binary=limited_report.gamma_binary,
        oxygen_generator_binary=oxygen_generator_binary,
        co2_scrubber_binary=co2_scrubber_binary,
    )
