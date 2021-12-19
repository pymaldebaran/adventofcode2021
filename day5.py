from dataclasses import dataclass
from typing import List, NamedTuple
import itertools
from collections import Counter


class Point(NamedTuple):
    x: int
    y: int

    def __repr__(self) -> str:
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
        >>> Segment(Point(1,2), Point(3,4))
        Segment(Point(1,2) -> Point(3,4))
    """

    _from: Point
    _to: Point

    def __repr__(self) -> str:
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
            from_x, to_x = self._from.x, self._to.x
            start, stop = (from_x, to_x) if from_x < to_x else (to_x, from_x)
            return [Point(x, self._from.y) for x in range(start, stop + 1)]
        elif self.is_vertical():
            from_y, to_y = self._from.y, self._to.y
            start, stop = (from_y, to_y) if from_y < to_y else (to_y, from_y)
            return [Point(self._from.x, y) for y in range(start, stop + 1)]
        else:
            raise NotImplementedError(
                f"You try to apply all_points() to {self!r} that is neither vertical nor horizontal."
            )


@dataclass
class HydrothermalVentsMap:
    segments: List[Segment]

    @staticmethod
    def from_str(raw_segments: str) -> "HydrothermalVentsMap":
        """
        Build an HydrothermalVentsMap from it's basic string representation.
        """
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
            [Segment(Point(1,1) -> Point(1,3)), Segment(Point(2,1) -> Point(2,3)), Segment(Point(3,3) -> Point(7,3))]
        """
        return [
            seg for seg in self.segments if seg.is_vertical() or seg.is_horizontal()
        ]

    def all_points(self) -> List[Point]:
        """
        Get all the points that belong to all the segments.

        WARNING: take accounts only of horizontal or vertical segments.

        Examples:
            >>> hvm = HydrothermalVentsMap.from_str('''1,1 -> 1,3
            ... 2,1 -> 2,3
            ... 1,1 -> 2,2''')
            >>> hvm.all_points()
            [Point(1,1), Point(1,2), Point(1,3), Point(2,1), Point(2,2), Point(2,3)]
        """
        return list(
            itertools.chain.from_iterable(
                (seg.all_points() for seg in self.h_or_v_segments())
            )
        )

    def nb_overlaps(self) -> int:
        """
        Count the number of overlaps in the segments.
        """
        counter = Counter(self.all_points())
        return len(list(filter(lambda pair: pair[1] >= 2, counter.most_common())))

    def map(self) -> str:
        """
        Display the HydrothermalVentsMap the same way as in the puzzle directives.
        """
        all_points = self.all_points()
        max_x = max(x for x, _ in all_points)
        max_y = max(y for _, y in all_points)

        map_elems = [["." for _ in range(max_x + 1)] for _ in range(max_y + 1)]

        counter = Counter(self.all_points())
        for (x, y), count in counter.most_common():
            map_elems[y][x] = "." if count == 0 else str(count)

        return "\n".join("".join([e for e in line]) for line in map_elems)


def day5(raw_points: str) -> HydrothermalVentsMap:
    """
    --- Day 5: Hydrothermal Venture ---

    You come across a field of hydrothermal vents on the ocean floor! These
    vents constantly produce large, opaque clouds, so it would be best to avoid
    them if possible.

    They tend to form in lines; the submarine helpfully produces a list of
    nearby lines of vents (your puzzle input) for you to review. For example:

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

    Each line of vents is given as a line segment in the format x1,y1 -> x2,y2
    where x1,y1 are the coordinates of one end the line segment and x2,y2 are
    the coordinates of the other end. These line segments include the points at
    both ends. In other words:

        An entry like 1,1 -> 1,3 covers points 1,1, 1,2, and 1,3.
        An entry like 9,7 -> 7,7 covers points 9,7, 8,7, and 7,7.

    For now, only consider horizontal and vertical lines: lines where either x1
    = x2 or y1 = y2.

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

    In this diagram, the top left corner is 0,0 and the bottom right corner is
    9,9. Each position is shown as the number of lines which cover that point or
    . if no line covers that point. The top-left pair of 1s, for example, comes
    from 2,2 -> 2,1; the very bottom row is formed by the overlapping lines 0,9
    -> 5,9 and 0,9 -> 2,9.

    To avoid the most dangerous areas, you need to determine the number of
    points where at least two lines overlap. In the above example, this is
    anywhere in the diagram with a 2 or larger - a total of 5 points.

    Consider only horizontal and vertical lines. At how many points do at least
    two lines overlap?
    """
    return HydrothermalVentsMap.from_str(raw_points)
