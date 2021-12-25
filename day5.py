"""
Day 5: Hydrothermal Venture.

You come across a field of hydrothermal vents on the ocean floor! These vents
constantly produce large, opaque clouds, so it would be best to avoid them if
possible.

They tend to form in lines; the submarine helpfully produces a list of nearby
lines of vents (your puzzle input) for you to review. For example:

0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2

Each line of vents is given as a line segment in the format x1,y1 -> x2,y2 where
x1,y1 are the coordinates of one end the line segment and x2,y2 are the
coordinates of the other end. These line segments include the points at both
ends. In other words:

    An entry like 1,1 -> 1,3 covers points 1,1, 1,2, and 1,3.
    An entry like 9,7 -> 7,7 covers points 9,7, 8,7, and 7,7.

For now, only consider horizontal and vertical lines: lines where either x1 = x2
or y1 = y2.

So, the horizontal and vertical lines from the above list would produce the
following diagram:

.......1..
..1....1..
..1....1..
.......1..
.112111211
..........
..........
..........
..........
222111....

In this diagram, the top left corner is 0,0 and the bottom right corner is 9,9.
Each position is shown as the number of lines which cover that point or . if no
line covers that point. The top-left pair of 1s, for example, comes from 2,2 ->
2,1; the very bottom row is formed by the overlapping lines 0,9 -> 5,9 and 0,9
-> 2,9.

To avoid the most dangerous areas, you need to determine the number of points
where at least two lines overlap. In the above example, this is anywhere in the
diagram with a 2 or larger - a total of 5 points.

Consider only horizontal and vertical lines. At how many points do at least two
lines overlap?

--- Part Two ---

Unfortunately, considering only horizontal and vertical lines doesn't give you
the full picture; you need to also consider diagonal lines.

Because of the limits of the hydrothermal vent mapping system, the lines in your
list will only ever be horizontal, vertical, or a diagonal line at exactly 45
degrees. In other words:

    An entry like 1,1 -> 3,3 covers points 1,1, 2,2, and 3,3.
    An entry like 9,7 -> 7,9 covers points 9,7, 8,8, and 7,9.

Considering all lines from the above example would now produce the following
diagram:

1.1....11.
.111...2..
..2.1.111.
...1.2.2..
.112313211
...1.2....
..1...1...
.1.....1..
1.......1.
222111....

You still need to determine the number of points where at least two lines
overlap. In the above example, this is still anywhere in the diagram with a 2 or
larger - now a total of 12 points.

Consider all of the lines. At how many points do at least two lines overlap?
"""

from dataclasses import dataclass
from typing import List, NamedTuple
import itertools
from collections import Counter


class Point(NamedTuple):
    """Represent a 2D point with integer coordinates."""

    x: int
    y: int

    def __repr__(self) -> str:
        """Represent the point in the most simple way."""
        return f"Point({self.x},{self.y})"

    @staticmethod
    def from_str(raw_point: str) -> "Segment":
        """
        Build a Point from it's basic string representation.

        Example:
            >>> Point.from_str('1,2')
            Point(1,2)
        """
        assert "," in raw_point
        x, y = raw_point.strip().split(",")
        return Point(int(x), int(y))


@dataclass
class Segment:
    """
    Represent a segment from a point to another.

    Example:
        >>> Segment(Point(0,0), Point(3,3))
        Segment(Point(0,0) -> Point(3,3))
    """

    _from: Point
    _to: Point

    def __post_init__(self):
        r"""
        Normalise the segment.

        - all vertical segments must be pointing down
        - all horizontal segments must be pointing right
        - all diagonal like a / segments must be pointing up-right
        - all diagonal like a \ segments must be pointing down-right
        """
        if self.is_horizontal() and self._from.x > self._to.x:
            self._from, self._to = self._to, self._from
        elif self.is_vertical() and self._from.y > self._to.y:
            self._from, self._to = self._to, self._from
        elif self.is_diagonal_anti_slash() and self._from.x > self._to.x:
            self._from, self._to = self._to, self._from
        elif self.is_diagonal_slash() and self._from.x > self._to.x:
            self._from, self._to = self._to, self._from

    def __repr__(self) -> str:
        """Represent the segment in the most simple way."""
        return f"Segment({self._from} -> {self._to})"

    @staticmethod
    def from_str(raw_segment):
        """
        Build a Segment from it's basic string representation.

        Example:
            >>> Segment.from_str('4,5 -> 8,9')
            Segment(Point(4,5) -> Point(8,9))
        """
        assert " -> " in raw_segment
        raw_points = raw_segment.strip().split(" -> ")
        return Segment(Point.from_str(raw_points[0]), Point.from_str(raw_points[1]))

    def is_vertical(self) -> bool:
        """
        Tell if the segment is vertical.

        Examples:
            >>> v = Segment.from_str('1,2 -> 1,6')
            >>> v.is_vertical()
            True
            >>> nv = Segment.from_str('2,2 -> 1,6')
            >>> nv.is_vertical()
            False
        """
        return self._from.x == self._to.x

    def is_horizontal(self) -> bool:
        """
        Tell if the segment is horizontal.

        Examples:
            >>> v = Segment.from_str('1,2 -> 7,2')
            >>> v.is_horizontal()
            True
            >>> nv = Segment.from_str('2,2 -> 1,6')
            >>> nv.is_horizontal()
            False
        """
        return self._from.y == self._to.y

    def is_diagonal_anti_slash(self) -> bool:
        r"""
        Tell if the segment is diagonal like a \.

        Examples:
            >>> v = Segment.from_str('0,0 -> 5,5')
            >>> v.is_diagonal_anti_slash()
            True
            >>> v = Segment.from_str('5,5 -> 0,0')
            >>> v.is_diagonal_anti_slash()
            True
            >>> nv = Segment.from_str('0,0 -> 0,6')
            >>> nv.is_diagonal_anti_slash()
            False
            >>> nv = Segment.from_str('0,0 -> 6,0')
            >>> nv.is_diagonal_anti_slash()
            False
        """
        # We use the fact that we only have horizontal, vertical and diagonal segments
        return (self._from.x < self._to.x and self._from.y < self._to.y) or (
            self._from.x > self._to.x and self._from.y > self._to.y
        )

    def is_diagonal_slash(self) -> bool:
        """
        Tell if the segment is diagonal like a /.

        Examples:
            >>> v = Segment.from_str('0,5 -> 5,0')
            >>> v.is_diagonal_slash()
            True
            >>> v = Segment.from_str('5,0 -> 0,5')
            >>> v.is_diagonal_slash()
            True
            >>> nv = Segment.from_str('0,0 -> 0,6')
            >>> nv.is_diagonal_slash()
            False
            >>> nv = Segment.from_str('0,0 -> 6,0')
            >>> nv.is_diagonal_slash()
            False
        """
        # We use the fact that we only have horizontal, vertical and diagonal segments
        return (self._from.x < self._to.x and self._from.y > self._to.y) or (
            self._from.x > self._to.x and self._from.y < self._to.y
        )

    def all_points(self) -> List[Point]:
        """
        Get all the points that belong to the segment.

        WARNING: works only for horizontal or vertical segments.

        Examples:
            Downward column:

            >>> s = Segment.from_str('1,1 -> 1,3')
            >>> s.all_points()
            [Point(1,1), Point(1,2), Point(1,3)]

            Upward column:
            >>> s = Segment.from_str('1,3 -> 1,1')
            >>> s.all_points()
            [Point(1,1), Point(1,2), Point(1,3)]
        """
        if self.is_horizontal():
            # Segments are normalized so no from/to order problem
            return [Point(x, self._from.y) for x in range(self._from.x, self._to.x + 1)]

        if self.is_vertical():
            # Segments are normalized so no from/to order problem
            return [Point(self._from.x, y) for y in range(self._from.y, self._to.y + 1)]

        if self.is_diagonal_anti_slash():
            # Segments are normalized so no from/to order problem
            return [
                Point(x, y)
                for (x, y) in zip(
                    range(self._from.x, self._to.x + 1),
                    range(self._from.y, self._to.y + 1),
                )
            ]

        if self.is_diagonal_slash():
            # Segments are normalized so no from/to order problem
            return [
                Point(x, y)
                for (x, y) in zip(
                    range(self._from.x, self._to.x + 1),
                    range(self._from.y, self._to.y - 1, -1),
                )
            ]

        raise ValueError(
            f"{self!r} is neither vertical nor horizontal nor diagonal."
        )


@dataclass
class HydrothermalVentsMap:
    """Represent a maap of the hydrothermal vents."""

    segments: List[Segment]

    @staticmethod
    def from_str(raw_segments: str) -> "HydrothermalVentsMap":
        """Build an HydrothermalVentsMap from it's basic string representation."""
        return HydrothermalVentsMap(
            [Segment.from_str(line) for line in raw_segments.strip().splitlines()]
        )

    def h_or_v_segments(self) -> List[Segment]:
        """
        Get a list of all the vertical or horizontal segments only.

        Examples:
            >>> hvm = HydrothermalVentsMap.from_str('''1,1 -> 1,3
            ... 2,1 -> 2,3
            ... 1,1 -> 2,2
            ... 3,3 -> 7,3''')
            >>> hvm.h_or_v_segments()
            [Segment(Point(1,1) -> Point(1,3)),
            Segment(Point(2,1) -> Point(2,3)),
            Segment(Point(3,3) -> Point(7,3))]
        """
        return [
            seg for seg in self.segments if seg.is_vertical() or seg.is_horizontal()
        ]

    def all_points_hv(self) -> List[Point]:
        """
        Get all the points that belong to all the horizontal or vertical segments.

        Examples:
            >>> hvm = HydrothermalVentsMap.from_str('''1,1 -> 1,3
            ... 2,1 -> 2,3
            ... 1,1 -> 2,2''')
            >>> hvm.all_points_hv()
            [Point(1,1), Point(1,2), Point(1,3), Point(2,1), Point(2,2), Point(2,3)]
        """
        return list(
            itertools.chain.from_iterable(
                (seg.all_points() for seg in self.h_or_v_segments())
            )
        )

    def all_points(self) -> List[Point]:
        """
        Get all the points that belong to all the segments.

        Examples:
            >>> hvm = HydrothermalVentsMap.from_str('''1,1 -> 1,3
            ... 2,1 -> 2,3
            ... 1,1 -> 2,2''')
            >>> hvm.all_points()
            [Point(1,1), Point(1,2), Point(1,3), Point(2,1),
            Point(2,2), Point(2,3), Point(1,1), Point(2,2)]
        """
        return list(
            itertools.chain.from_iterable((seg.all_points() for seg in self.segments))
        )

    def nb_overlaps_hv(self) -> int:
        """Count the number of overlaps in the horizontal and vertical segments."""
        counter = Counter(self.all_points_hv())
        return len(list(filter(lambda pair: pair[1] >= 2, counter.most_common())))

    def nb_overlaps_full(self) -> int:
        """Count the number of overlaps in the horiz., vertic. and diag. segments."""
        counter = Counter(self.all_points())
        return len(list(filter(lambda pair: pair[1] >= 2, counter.most_common())))

    def map(self, hv_only=False) -> str:
        """
        Display the HydrothermalVentsMap the same way as in the puzzle directives.

        This is for visual debug purpose only.
        """
        all_points = self.all_points_hv() if hv_only else self.all_points()
        max_x = max(x for x, _ in all_points)
        max_y = max(y for _, y in all_points)

        map_elems = [["." for _ in range(max_x + 1)] for _ in range(max_y + 1)]

        counter = Counter(all_points)
        for (x, y), count in counter.most_common():
            map_elems[y][x] = "." if count == 0 else str(count)

        return "\n".join("".join(list(line)) for line in map_elems)


def day5(raw_points: str) -> HydrothermalVentsMap:
    """Solve day 5 puzzle (part 1 and 2) for any valid input."""
    return HydrothermalVentsMap.from_str(raw_points)
