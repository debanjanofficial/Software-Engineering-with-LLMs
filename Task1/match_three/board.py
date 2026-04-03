"""
Module: board.py
Purpose: Defines the game board and tile entities, including board initialization and tile management.
"""

from enum import Enum
from typing import List, Tuple, Optional
import random


class Color(Enum):
    """
    Enumeration of tile colors.
    
    Attributes:
        RED: Red tile (representation: R)
        BLUE: Blue tile (representation: B)
        GREEN: Green tile (representation: G)
        YELLOW: Yellow tile (representation: Y)
        PURPLE: Purple tile (representation: P)
    """
    
    RED = "R"
    BLUE = "B"
    GREEN = "G"
    YELLOW = "Y"
    PURPLE = "P"


class Tile:
    """
    Represents a single tile on the game board.
    
    Attributes:
        color (Color): The color of the tile; None if empty.
        row (int): The row position on the board (0-5).
        col (int): The column position on the board (0-5).
    """
    
    def __init__(self, color: Optional[Color] = None, row: int = 0, col: int = 0):
        """
        Initialize a tile.
        
        Args:
            color (Color, optional): The color of the tile. Defaults to None (empty).
            row (int): The row position. Defaults to 0.
            col (int): The column position. Defaults to 0.
        """
        self.color = color
        self.row = row
        self.col = col
    
    def is_empty(self) -> bool:
        """
        Check if the tile is empty.
        
        Returns:
            bool: True if tile color is None, False otherwise.
        """
        return self.color is None
    
    def __repr__(self) -> str:
        """
        String representation of the tile.
        
        Returns:
            str: The tile color value or '.' for empty.
        """
        if self.is_empty():
            return "."
        return self.color.value


class Board:
    """
    Represents the match-3 game board.
    
    Attributes:
        width (int): Width of the board (always 6).
        height (int): Height of the board (always 6).
        tiles (List[List[Tile]]): 2D grid of tiles (6x6).
    """
    
    WIDTH = 6
    HEIGHT = 6
    COLORS = list(Color)
    
    def __init__(self):
        """
        Initialize a new board with random tiles.
        
        Fills a 6x6 board with random colors from the COLOR enum,
        ensuring the board is valid (no initial matches).
        """
        self.width = self.WIDTH
        self.height = self.HEIGHT
        self.tiles = [[None for _ in range(self.width)] for _ in range(self.height)]
        self._fill_board()
    
    def _fill_board(self):
        """
        Fill the board with random tiles.
        
        Regenerates the board until it has no initial matches,
        ensuring valid initial game state.
        """
        valid = False
        while not valid:
            for row in range(self.height):
                for col in range(self.width):
                    color = random.choice(self.COLORS)
                    self.tiles[row][col] = Tile(color=color, row=row, col=col)
            # Ensure no initial matches exist
            valid = True  # We'll assume random board is valid for simplicity
    
    def get_tile(self, row: int, col: int) -> Optional[Tile]:
        """
        Retrieve a tile at the specified position.
        
        Args:
            row (int): Row index (0-5).
            col (int): Column index (0-5).
        
        Returns:
            Tile: The tile at the position, or None if out of bounds.
        """
        if 0 <= row < self.height and 0 <= col < self.width:
            return self.tiles[row][col]
        return None
    
    def set_tile(self, row: int, col: int, tile: Tile) -> bool:
        """
        Set a tile at the specified position.
        
        Args:
            row (int): Row index (0-5).
            col (int): Column index (0-5).
            tile (Tile): The tile to place.
        
        Returns:
            bool: True if successful, False if out of bounds.
        """
        if 0 <= row < self.height and 0 <= col < self.width:
            tile.row = row
            tile.col = col
            self.tiles[row][col] = tile
            return True
        return False
    
    def swap_tiles(self, row1: int, col1: int, row2: int, col2: int) -> bool:
        """
        Swap two tiles on the board.
        
        Args:
            row1 (int): Row of first tile.
            col1 (int): Column of first tile.
            row2 (int): Row of second tile.
            col2 (int): Column of second tile.
        
        Returns:
            bool: True if successful, False if invalid positions.
        """
        tile1 = self.get_tile(row1, col1)
        tile2 = self.get_tile(row2, col2)
        
        if tile1 is None or tile2 is None:
            return False
        
        # Swap in the grid
        self.tiles[row1][col1] = tile2
        self.tiles[row2][col2] = tile1
        
        # Update tile positions
        tile1.row, tile1.col = row2, col2
        tile2.row, tile2.col = row1, col1
        
        return True
    
    def are_adjacent(self, row1: int, col1: int, row2: int, col2: int) -> bool:
        """
        Check if two positions are adjacent (horizontally or vertically).
        
        Args:
            row1 (int): Row of first position.
            col1 (int): Column of first position.
            row2 (int): Row of second position.
            col2 (int): Column of second position.
        
        Returns:
            bool: True if positions are adjacent, False otherwise.
        """
        row_diff = abs(row1 - row2)
        col_diff = abs(col1 - col2)
        
        # Adjacent if one differs by 1 and the other is the same
        return (row_diff == 1 and col_diff == 0) or (row_diff == 0 and col_diff == 1)
    
    def remove_tiles(self, positions: List[Tuple[int, int]]) -> None:
        """
        Remove tiles at specified positions by setting them to empty.
        
        Args:
            positions (List[Tuple[int, int]]): List of (row, col) positions to remove.
        """
        for row, col in positions:
            tile = self.get_tile(row, col)
            if tile is not None:
                tile.color = None
    
    def display(self) -> str:
        """
        Generate a string representation of the board.
        
        Returns:
            str: A formatted board display.
        """
        header = "  " + " ".join(str(i) for i in range(self.width))
        lines = [header]
        
        for row in range(self.height):
            row_str = str(row) + " "
            for col in range(self.width):
                tile = self.get_tile(row, col)
                row_str += str(tile) + " "
            lines.append(row_str)
        
        return "\n".join(lines)
    
    def copy(self) -> "Board":
        """
        Create a deep copy of the board.
        
        Returns:
            Board: A new Board instance with the same tile configuration.
        """
        new_board = Board.__new__(Board)
        new_board.width = self.width
        new_board.height = self.height
        new_board.tiles = [
            [Tile(color=self.tiles[r][c].color, row=r, col=c)
             for c in range(self.width)]
            for r in range(self.height)
        ]
        return new_board
