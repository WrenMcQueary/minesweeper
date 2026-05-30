"""
One tile of the board.
"""


class Tile:

    def __init__(self, row: int, column: int, is_mine: bool):
        """
        :param row:         Row coordinate of the tile on the board.
        :param column:      Column coordinate of the tile on the board.
        :param is_mine:     Whether the tile is a mine.
        """
        self.row = row
        self.column = column
        self.is_mine = is_mine
        self.is_revealed = False
        self.is_flagged = False
        self.adjacent_mine_count = None

    def get_coordinates(self) -> tuple[int]:
        """
        :return:            The (row, column) coordinates of this tile on the
                            board.
        """
        return (self.row, self.column)
    
    def get_is_mine(self) -> bool:
        """
        :return:            Whether the tile is a mine.
        """
        return self.is_mine
    
    def get_is_revealed(self) -> bool:
        """
        :return:            Whether the tile is revealed.
        """
        return self.is_revealed
    
    def get_is_flagged(self) -> bool:
        """
        :return:            Whether the tile is flagged.
        """
        return self.is_flagged

    def get_adjacent_mine_count(self) -> int:
        """
        Get the tile's adjacent mine count.

        :return:            The adjacent mine count.
        """
        if self.adjacent_mine_count is None:
            raise RuntimeError("adjacent mine count has not yet been set")
        return self.adjacent_mine_count
    
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
    
    def toggle_flag(self) -> None:
        """
        Toggle flag attribute.
        """
        self.is_flagged = not self.is_flagged
