"""
Presentation layer.
"""

import tkinter as tk
from tkinter.messagebox import Message

from app.board import Board
from app.tile import Tile


class Presentation:
    """
    Serves the GUI of the minesweeper game, updates the data layer based on the
    player's inputs, and adjudicates wins and losses.
    """

    def __init__(self, board: Board):
        """
        :param board:           Data layer object representing the game board.
        """
        self.board = board
        self.window = tk.Tk()
        self.window.title("Minesweeper")
        window_width = 30 * self.board.side_length + 30
        window_height = 30 * self.board.side_length
        self.window.geometry(f"{window_width}x{window_height}")  # TODO: Scale based on side length
        self.window.configure(background="gray")
        self.num_flags = 0
        self.is_next_click_safe = True

        # Create frames and mappings from frames to tiles
        side_length = self.board.get_side_length()
        self.frames = [[None for _ in range(side_length)] for _ in range(side_length)]
        self.tile_to_frame = dict()
        self.frame_to_tile = dict()
        for rr in range(side_length):
            for cc in range(side_length):
                self.frames[rr][cc] = tk.Frame(
                    self.window,
                    width=30,
                    height=30,
                    bg="gray",
                    bd=3,
                    relief=tk.RAISED,
                )
                self.frames[rr][cc].grid(row=rr, column=cc)
                self.frames[rr][cc].bind("<Button-1>", self.handle_left_click)
                self.frames[rr][cc].bind("<Button-2>", self.handle_right_click)
                self.tile_to_frame[self.board.get_tile(rr, cc)] = self.frames[rr][cc]
                self.frame_to_tile[self.frames[rr][cc]] = self.board.get_tile(rr, cc)

        # Create outstanding mine counter
        self.outstanding_mine_counter = tk.Label(
            self.window,
            text=str(self.board.num_mines),
            width=2,
            height=1,
            bg="yellow",
            fg="black",
            font="Courier 18",
        )
        self.outstanding_mine_counter.grid(row=0, column=side_length)

        # Serve GUI
        self.window.mainloop()

    def get_frame_from_tile(self, tile: Tile) -> tk.Frame:
        """
        Get the Frame (in the presentation layer) that corresponds to a
        particular Tile of the board (in the data layer).

        :param tile:        Tile object.
        :return:            The corresponding Frame object.
        """
        return self.tile_to_frame[tile]
    
    def get_tile_from_frame(self, frame: tk.Frame) -> Tile:
        """
        Get the Tile of the board (in the data layer) that corresponds to a
        particular Frame (in the presentation layer).

        :param frame:       Frame object
        :return:            The corresponding Tile object.
        """
        return self.frame_to_tile[frame]

    def lose(self) -> None:
        """
        Show a loss message and exit the game once the message is closed.
        """
        message = Message(
            self.window,
            type="ok",
            title="Kaboom",
            icon="error",
            message="💣💥☹️",
        )
        message.show()
        self.window.quit()

    def win(self) -> None:
        """
        Show a win message and exit the game once the message is closed.
        """
        message = Message(
            self.window,
            type="ok",
            title="Victory!",
            icon="info",
            message="You won!",
        )
        message.show()
        self.window.quit()

    def check_if_game_won(self) -> bool:
        """
        Check whether the game has been won (ie, whether all non-mine tiles have
        been revealed).

        :return:        True if the game has been won, else False.
        """
        for rr in range(self.board.side_length):
            for cc in range(self.board.side_length):
                tile = self.board.get_tile(row=rr, column=cc)
                if (not tile.get_is_mine()) and (not tile.get_is_revealed()):
                    return False
        return True

    def reveal(self, frame: tk.Frame) -> None:
        """
        Reveal a space of the board.  Update the Tile in the data layer and the
        Frame in the presentation layer.

        :param frame:       Frame to reveal
        """
        tile = self.get_tile_from_frame(frame)
        
        # Do nothing if tile is revealed or flagged
        if tile.get_is_revealed() or tile.get_is_flagged():
            return
        
        # Reveal tile
        tile.reveal()
        frame.configure(
            relief=tk.FLAT,
        )
        
        is_mine = tile.get_is_mine()
        if is_mine:
            if self.is_next_click_safe:
                # Find a random tile that isn't a mine
                non_mine_tile = self.board.get_random_non_mine_tile()

                # Swap the tiles
                self.board.swap_tile_mines(tile, non_mine_tile)

                # Set label parameters like normal
                label_text = str(tile.get_adjacent_mine_count())
                label_color = {
                    "0": "gray",
                    "1": "blue",
                    "2": "green",
                    "3": "yellow",
                    "4": "purple",
                    "5": "#c52525",
                    "6": "#8b0000",
                    "7": "orange",
                    "8": "brown",
                }[label_text]
                label_font = "Courier 18"

                # Avoid mine-clicking consequences
                is_mine = False
            else:
                label_text = "💣"
                label_color = "black"
                label_font = "Courier 12"
        else:
            label_text = str(tile.get_adjacent_mine_count())
            label_color = {
                "0": "gray",
                "1": "blue",
                "2": "green",
                "3": "yellow",
                "4": "purple",
                "5": "#c52525",
                "6": "#8b0000",
                "7": "orange",
                "8": "brown",
            }[label_text]
            label_font = "Courier 18"
        
        tk.Label(frame,
            text=label_text,
            relief=tk.FLAT,
            bg="gray",
            fg=label_color,
            font=label_font,
        ).pack()
        self.is_next_click_safe = False


        # If tile has an adjacent mine count of 0, reveal all contiguous tiles with adjacent mine counts of 0.
        if label_text == "0":
            row, column = tile.get_coordinates()
            neighbors = self.board.get_neighboring_tiles(row=row, column=column)
            for neighbor in neighbors:
                self.reveal(self.get_frame_from_tile(neighbor))

        # If tile is a mine, lose.
        if is_mine:
            self.window.after(1, self.lose)
            return
        
        # If all non-mine tiles have been revealed, win
        is_game_won = self.check_if_game_won()
        if is_game_won:
            self.window.after(1, self.win)
            return

    def toggle_flag(self, frame: tk.Frame) -> None:
        """
        Toggle a flag on a space of the board.  Update the Tile in the data
        layer and the Frame in the presentation layer.
        
        :param frame:       Frame to toggle
        """
        tile = self.get_tile_from_frame(frame)
        
        # Do nothing if tile is revealed
        if tile.get_is_revealed():
            return
        
        # Toggle
        tile.toggle_flag()
        if tile.get_is_flagged():
            frame.configure(bg="red")
            self.num_flags += 1
        else:
            frame.configure(bg="gray")
            self.num_flags -= 1
        
        # Update counter
        self.outstanding_mine_counter.configure(text=str(self.board.num_mines - self.num_flags))

    def handle_left_click(self, event: tk.Event) -> None:
        """
        Handle a left-click event.

        :param event:       Input event created by Tkinter.
        """
        self.reveal(frame=event.widget)

    def handle_right_click(self, event: tk.Event) -> None:
        """
        Handle a right-click event.

        :param event:       Input event created by Tkinter.
        """
        self.toggle_flag(frame=event.widget)