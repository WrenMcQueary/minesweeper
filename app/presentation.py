"""
Presentation layer; serves the GUI.
"""

import tkinter as tk
from tkinter.messagebox import Message

from app.board import Board
from app.tile import Tile


class Presentation:

    def __init__(self, board: Board):
        """
        TODO
        """
        self.board = board
        self.window = tk.Tk()
        self.window.title("Minesweeper")
        self.window.geometry("300x270")  # TODO: Scale based on side length
        self.window.configure(background="gray")
        self.num_flags = 0

        # Create frames and mappings from frames to tiles
        side_length = self.board.get_side_length()
        self.frames = [[None for _ in range(side_length)] for _ in range(side_length)]
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
                self.frames[rr][cc].bind("<Button-1>", self.reveal)
                self.frames[rr][cc].bind("<Button-2>", self.toggle_flag)
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

    def get_tile_from_frame(self, frame: tk.Frame) -> Tile:
        """
        Get the Tile of the board (in the data layer) that corresponds with a
        particular Frame (in the presentation layer).

        :param frame:       Frame object
        :return:            The corresponding Tile object.
        """
        return self.frame_to_tile[frame]

    def lose(self) -> None:
        """
        Lose the game.
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

    def reveal(self, event: tk.Event) -> None:
        """
        Reveal the tile.  Update the data layer and presentation layer.

        :param event:       Event produced by mouseclick
        """
        frame = event.widget
        tile = self.get_tile_from_frame(frame)
        
        # Do nothing if tile is revealed or flagged
        if tile.get_is_revealed() or tile.get_is_flagged():
            return
        
        # If tile is a mine, lose.
        if tile.get_is_mine():
            self.lose()
            return

        # Reveal tile
        tile.reveal()
        frame.configure(
            relief=tk.FLAT,
        )
        adjacent_mine_count = tile.get_adjacent_mine_count()
        count_color = {
            0: "gray",
            1: "blue",
            2: "green",
            3: "yellow",
            4: "purple",
            5: "#c52525",
            6: "#8b0000",
            7: "orange",
            8: "brown",
        }[adjacent_mine_count]
        tk.Label(frame,
            text=str(tile.get_adjacent_mine_count()),
            relief=tk.FLAT,
            bg="gray",
            fg=count_color,
            font="Courier 18",
        ).pack()

        # If tile has an adjacent mine count of 0, reveal all contiguous tiles with adjacent mine counts of 0.
        # TODO

    def toggle_flag(self, event: tk.Event) -> None:
        """
        Toggle a flag on the tile.  Update the data layer and presentation
        layer.
        
        :param event:       Event produced by mouseclick
        """
        frame = event.widget
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
