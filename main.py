import argparse

from app.board import Board
from app.presentation import Presentation


def main(side_length: int, num_mines: int):
    """
    Run a game of minesweeper.

    :param side_length:     Length of each side of the board, in tiles.
    :param num_mines:       Number of mines to distribute across the board.
    """

    # Error handling
    if side_length < 2:
        raise ValueError("side_length must be at least 2")
    if num_mines < 1:
        raise ValueError("num_mines must be at least 1")
    if num_mines >= side_length ** 2:
        raise ValueError("number of mines must be less than number of spaces on board")

    # Set up the board
    board = Board(
        side_length = side_length,
        num_mines = num_mines,
    )

    # Create a GUI with the board
    Presentation(board)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Run a game of minesweeper."
    )
    parser.add_argument(
        "--side_length",
        "-s",
        action="store",
        nargs=1,
        type=int,
        required=True,
        help="Length of each side of the board, in tiles.",
        dest="side_length",
    )
    parser.add_argument(
        "--num_mines",
        "-m",
        action="store",
        nargs=1,
        type=int,
        required=True,
        help="Number of mines to distribute across the board.",
        dest="num_mines",
    )
    args = parser.parse_args()
    side_length = args.side_length[0]
    num_mines = args.num_mines[0]

    main(side_length=side_length, num_mines=num_mines)
