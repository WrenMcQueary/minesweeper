import argparse

from app.board import Board
from app.presentation import present


def main():
    """
    Run the game.
    """

    # Set up the board
    board = Board(
        side_length = 9,
        num_mines = 10,
    )

    # Create a GUI with the board
    present(board)


if __name__ == "__main__":

    # TODO: Set up argparse

    main()
