"""
Presentation layer; serves the GUI.
"""

import tkinter as tk

from app.board import Board


def reveal() -> None:
    """
    TODO
    """
    raise NotImplementedError() # TODO


def flag() -> None:
    """
    TODO
    """
    raise NotImplementedError() # TODO


# TODO: Use relief=tk.RIDGE or SUNKEN once a button has been revealed
def present(board: Board) -> None:
    """
    TODO
    """
    window = tk.Tk()
    window.title("Minesweeper")
    window.geometry("270x270")  # TODO: Scale based on side length

    # Create frames
    side_length = board.get_side_length()
    frames = [[None for _ in range(side_length)] for _ in range(side_length)]
    for rr in range(side_length):
        for cc in range(side_length):
            frames[rr][cc] = tk.Frame(
                window,
                width=30,
                height=30,
                bg="gray",
                bd=3,
                relief=tk.RAISED,
            )
            frames[rr][cc].grid(row=rr, column=cc)
            frames[rr][cc].bind("<Button-1>", reveal)
            frames[rr][cc].bind("<Button-2>", flag)
    
    # Serve GUI
    window.mainloop()
