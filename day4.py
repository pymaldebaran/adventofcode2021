"""
Day 4: Giant Squid.

You're already almost 1.5km (almost a mile) below the surface of the ocean,
already so deep that you can't see any sunlight. What you can see, however, is a
giant squid that has attached itself to the outside of your submarine.

Maybe it wants to play bingo?

Bingo is played on a set of boards each consisting of a 5x5 grid of numbers.
Numbers are chosen at random, and the chosen number is marked on all boards on
which it appears. (Numbers may not appear on all boards.) If all numbers in any
row or any column of a board are marked, that board wins. (Diagonals don't
count.)

The submarine has a bingo subsystem to help passengers (currently, you and the
giant squid) pass the time. It automatically generates a random order in which
to draw numbers and a random set of boards (your puzzle input). For example:

> 7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1
>
> 22 13 17 11  0
>  8  2 23  4 24
> 21  9 14 16  7
>  6 10  3 18  5
>  1 12 20 15 19
>
>  3 15  0  2 22
>  9 18 13 17  5
> 19  8  7 25 23
> 20 11 10 24  4
> 14 21 16 12  6
>
> 14 21 17 24  4
> 10 16 15  9 19
> 18  8 23 26 20
> 22 11 13  6  5
>  2  0 12  3  7

After the first five numbers are drawn (7, 4, 9, 5, and 11), there are no
winners, but the boards are marked as follows (shown here adjacent to each other
to save space):

>  22   13   17  *11*   0         3   15    0    2   22        14   21   17   24   *4*
>   8    2   23   *4*  24        *9*  18   13   17   *5*       10   16   15   *9*  19
>  21   *9*  14   16   *7*       19    8   *7*  25   23        18    8   23   26   20
>   6   10    3   18   *5*       20  *11*  10   24   *4*       22  *11*  13    6   *5*
>   1   12   20   15   19        14   21   16   12    6         2    0   12    3   *7*

After the next six numbers are drawn (17, 23, 2, 0, 14, and 21), there are still
no winners:

>  22   13  *17* *11*  *0*        3   15   *0*  *2*  22       *14*  21* *17*  24   *4*
>   8   *2* *23*  *4*  24        *9*  18   13  *17*  *5*       10   16   15   *9*  19
> *21*  *9* *14*  16   *7*       19    8   *7*  25  *23*       18    8  *23*  26   20
>   6   10    3   18   *5*       20  *11*  10   24   *4*       22  *11*  13    6   *5*
>   1   12   20   15   19       *14* *21*  16   12    6        *2*  *0*  12    3   *7*

Finally, 24 is drawn:

>  22   13  *17* *11*  *0*        3   15   *0*  *2*  22       *14*  21* *17* *24*  *4*
>   8   *2* *23*  *4* *24*       *9*  18   13  *17*  *5*       10   16   15   *9*  19
> *21*  *9* *14*  16   *7*       19    8   *7*  25  *23*       18    8  *23*  26   20
>   6   10    3   18   *5*       20  *11*  10  *24*  *4*       22  *11*  13    6   *5*
>   1   12   20   15   19       *14* *21*  16   12    6        *2*  *0*  12    3   *7*

At this point, the third board wins because it has at least one complete row or
column of marked numbers (in this case, the entire top row is marked: 14 21 17
24 4).

The score of the winning board can now be calculated. Start by finding the sum
of all unmarked numbers on that board; in this case, the sum is 188. Then,
multiply that sum by the number that was just called when the board won, 24, to
get the final score, 188 * 24 = 4512.

To guarantee victory against the giant squid, figure out which board will win
first. What will your final score be if you choose that board?

--- Part Two ---

On the other hand, it might be wise to try a different strategy: let the giant
squid win.

You aren't sure how many bingo boards a giant squid could play at once, so
rather than waste time counting its arms, the safe thing to do is to figure out
which board will win last and choose that one. That way, no matter which boards
it picks, it will win for sure.

In the above example, the second board is the last to win, which happens after
13 is eventually called and its middle column is completely marked. If you were
to keep playing until this point, the second board would have a sum of unmarked
numbers equal to 148 for a final score of 148 * 13 = 1924.

Figure out which board will win last. Once it wins, what would its final score
be?
"""

from dataclasses import dataclass, field
from typing import List
import numpy as np
from numpy.typing import NDArray


@dataclass
class Board:
    """A bingo board with numbers marked or not."""

    numbers: NDArray[int]
    marked: NDArray[bool] = field(init=False)
    winning_number: int | None = field(init=False, default=None, repr=False)

    def __post_init__(self):
        """Fill the marked array to represent a non mrked board."""
        self.marked = np.zeros_like(self.numbers, dtype=bool)

    def __repr__(self) -> str:
        """Represent the board in the most simple way."""
        content = " | ".join(
            [
                " ".join(
                    [
                        f'{"*" if check else ""}{num}'
                        for num, check in zip(num_line, check_line)
                    ]
                )
                for num_line, check_line in zip(self.numbers, self.marked)
            ]
        )
        return f"Board({content})"

    @staticmethod
    def from_str(raw_board: str) -> "Board":
        """
        Build a Board from a classic string representation of it.

        Example:
            >>> conf = '''1 2
            ... 3 4
            ... '''
            >>> Board.from_str(conf)
            Board(1 2 | 3 4)
        """
        return Board(
            numbers=np.array(
                [
                    [int(v) for v in line.split()]
                    for line in raw_board.strip().split("\n")
                ]
            )
        )

    def unmarked_sum(self) -> int:
        """Sum of the value of all the unmarked numbers of the board."""
        return self.numbers[~self.marked].sum()

    def do_we_have_a_winner(self) -> bool:
        """
        Determine if we have a winning board.

        If any line or column if fully marked the board is a won.

        Example:
            >>> brd = Board.from_str('''1 2
            ... 3 4''')
            >>> brd.marked = np.array([[0, 0], [0, 0]], bool)
            >>> brd.do_we_have_a_winner()
            False
            >>> brd.marked = np.array([[1, 0], [0, 1]], bool)
            >>> brd.do_we_have_a_winner()
            False
            >>> brd.marked = np.array([[1, 1], [0, 0]], bool)
            >>> brd.do_we_have_a_winner()
            True
            >>> brd.marked = np.array([[0, 0], [1, 1]], bool)
            >>> brd.do_we_have_a_winner()
            True
            >>> brd.marked = np.array([[1, 0], [1, 0]], bool)
            >>> brd.do_we_have_a_winner()
            True
            >>> brd.marked = np.array([[0, 1], [0, 1]], bool)
            >>> brd.do_we_have_a_winner()
            True
        """
        for line in self.marked:
            if line.all():
                return True

        for col in self.marked.T:
            if col.all():
                return True

        return False

    def try_to_mark_number(self, number: int) -> bool:
        """
        Mark a number if it is present in the board.

        Example:
            >>> brd = Board.from_str('''1 2
            ... 3 4''')
            >>> brd
            Board(1 2 | 3 4)
            >>> brd.try_to_mark_number(2)
            True
            >>> brd
            Board(1 *2 | 3 4)
            >>> brd.try_to_mark_number(5)
            False
            >>> brd
            Board(1 *2 | 3 4)
            >>> brd.try_to_mark_number(3)
            True
            >>> brd
            Board(1 *2 | *3 4)
        """
        try:
            # BLACKMAGIC see https://stackoverflow.com/a/43821453
            found_idx = next(
                (idx for idx, val in np.ndenumerate(self.numbers) if val == number)
            )
            self.marked[found_idx] = True
            return True
        except StopIteration:
            return False

    def score(self) -> int:
        """Compute the score of a winning board."""
        assert self.winning_number, "Score can only be computed for a winning board"
        return self.unmarked_sum() * self.winning_number


@dataclass
class Bingo:
    """Represent a whole bingo game with boards and drawn numbers."""

    drawn_numbers: List[int]
    boards: List[Board]
    winning_board_idx: List[int] = field(init=False, default_factory=list, repr=False)

    def __post_init__(self):
        """Simulate the drawing of all the numbers until all boards are won."""
        for num in self.drawn_numbers:
            for idx, board in enumerate(self.boards):
                # We update only the not yet won boards
                if idx not in self.winning_board_idx:
                    board.try_to_mark_number(num)

            for idx, board in enumerate(self.boards):
                if idx not in self.winning_board_idx and board.do_we_have_a_winner():
                    board.winning_number = num
                    self.winning_board_idx.append(idx)

            # We must stop as soon as all boards are won
            if len(self.winning_board_idx) == len(self.boards):
                return

    @staticmethod
    def from_str(config: str) -> "Bingo":
        """
        Build a Bingo game from a classic string representation of it.

        Example:
            >>> conf = '''1,2,3
            ...
            ...  1  1
            ...  1  1
            ...
            ... 20 20
            ...  2 20
            ... '''
            >>> Bingo.from_str(conf)
            Bingo(drawn_numbers=[1, 2, 3],
            boards=[Board(*1 1 | 1 1), Board(20 20 | *2 20)])
        """
        raw_num, *raw_boards = config.strip().split("\n\n")

        num = [int(vn) for vn in raw_num.split(",")]
        boards = [Board.from_str(raw_b) for raw_b in raw_boards]

        return Bingo(drawn_numbers=num, boards=boards)

    def first_winning_board(self) -> Board | None:
        """Get the firts board to win according to the orders of drawn numbers."""
        if self.winning_board_idx:
            return self.boards[self.winning_board_idx[0]]

        return None

    def last_winning_board(self) -> Board | None:
        """Get the last board to win according to the orders of drawn numbers."""
        if self.winning_board_idx:
            return self.boards[self.winning_board_idx[-1]]

        return None


def day4(config: str) -> Bingo:
    """Solve day 4 puzzle (part 1 and 2) for any valid input."""
    bingo = Bingo.from_str(config)

    return bingo
