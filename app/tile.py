"""
One tile of the board.
"""


class Tile:

    def __init__(self, is_mine: bool):
        """
        :param is_mine:     Whether the tile is a mine.
        """
        self.is_mine = is_mine
        self.is_revealed = False

    def get_is_mine(self) -> bool:
        """
        :return:            Whether the tile is a mine.
        """
        return self.is_mine

    def set_adjacent_mine_count(self, adjacent_mine_count: int):
        """
        Set the tile's adjacent mine count.

        :param adjacent_mine_count:     The value to set.
        """
        self.adjacent_mine_count = adjacent_mine_count
    
    def reveal(self) -> None:
        """
        Reveal the tile.
        """
        self.is_revealed = True
