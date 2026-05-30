"""
The game board.
"""

import random
from functools import reduce
import operator

from app.tile import Tile


class Board:

    def __init__(self, side_length: int, num_mines: int):
        """
        TODO
        """
        self.side_length = side_length
        self.num_mines = num_mines

        num_safe_tiles = self.side_length ** 2 - self.num_mines
        mine_assignments = [False for _ in range(num_safe_tiles)] + [True for _ in range(self.num_mines)]
        random.shuffle(mine_assignments)

        self.board = [[False for _ in range(self.side_length)] for _ in range(self.side_length)]   # Each sub-list is a row

        # Decide which tiles are mines
        for rr in range(self.side_length):
            for cc in range(self.side_length):
                self.board[rr][cc] = Tile(row=rr, column=cc, is_mine=mine_assignments.pop())
        
        # Set adjacent mine counts
        self.count_adjacent_mines()

    def get_tile(self, row: int, column: int) -> Tile:
        """
        :return:        The board represented as rows of Tiles.
        """
        return self.board[row][column]
    
    def get_side_length(self) -> int:
        """
        :return:        The side length of the board
        """
        return self.side_length

    def get_neighboring_tiles(self, row: int, column: int) -> list[Tile]:
        """
        TODO
        """
        coordinates_to_collect = [
            [rr, cc]
            for rr, cc in [
                [row-1, column-1],
                [row-1, column],
                [row-1, column+1],
                
                [row, column-1],
                [row, column+1],
                
                [row+1, column-1],
                [row+1, column],
                [row+1, column+1],
            ]
            if 0 <= rr < self.side_length and 0 <= cc < self.side_length
        ]
        return [self.board[rr][cc] for rr, cc in coordinates_to_collect]
    
    def get_random_non_mine_tile(self) -> Tile:
        """
        TODO
        """
        non_mine_tiles = []
        for rr in range(self.side_length):
            for cc in range(self.side_length):
                tile = self.get_tile(row=rr, column=cc)
                if not tile.get_is_mine():
                    non_mine_tiles.append(tile)
        return random.choice(non_mine_tiles)

    def swap_tile_mines(self, tile_0: Tile, tile_1: Tile) -> None:
        """
        TODO

        :modify:        tile_0
        :modify:        tile_1
        """
        # Get mines from both tiles
        mines = {
            "tile_0": tile_0.get_is_mine(),
            "tile_1": tile_1.get_is_mine(),
        }

        # Swap mines
        tile_0.set_is_mine(mines["tile_1"])
        tile_1.set_is_mine(mines["tile_0"])

        # Re-count adjacent mine counts.
        self.count_adjacent_mines()

    def count_adjacent_mines(self) -> None:
        """
        TODO
        """
        for rr in range(self.side_length):
            for cc in range(self.side_length):
                if not self.board[rr][cc].get_is_mine():
                    neighbors = self.get_neighboring_tiles(rr, cc)
                    adjacent_mine_count = reduce(operator.add, [neighbor.get_is_mine() for neighbor in neighbors])
                    self.board[rr][cc].set_adjacent_mine_count(adjacent_mine_count)
