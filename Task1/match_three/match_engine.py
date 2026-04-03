"""
Module: match_engine.py
Purpose: Implements match detection, scoring, and board refill logic.
"""

from typing import List, Tuple, Set
import random
from board import Board, Color, Tile


class Match:
    """
    Represents a match found on the board.
    
    Attributes:
        color (Color): The color of the matched tiles.
        positions (List[Tuple[int, int]]): List of (row, col) positions in match.
        match_type (str): Type of match ("HORIZONTAL" or "VERTICAL").
        cascade_depth (int): How deep in the cascade this match occurred.
    """
    
    def __init__(
        self,
        color: Color,
        positions: List[Tuple[int, int]],
        match_type: str = "HORIZONTAL",
        cascade_depth: int = 0
    ):
        """
        Initialize a match.
        
        Args:
            color (Color): The color of tiles in the match.
            positions (List[Tuple]): List of (row, col) tuples.
            match_type (str): "HORIZONTAL" or "VERTICAL".
            cascade_depth (int): Cascade depth for scoring. Defaults to 0.
        """
        self.color = color
        self.positions = positions
        self.match_type = match_type
        self.cascade_depth = cascade_depth
    
    def count(self) -> int:
        """
        Get the number of tiles in this match.
        
        Returns:
            int: The number of positions in the match.
        """
        return len(self.positions)
    
    def __repr__(self) -> str:
        """String representation of the match."""
        return f"Match({self.color.value}, {self.match_type}, {self.count()} tiles)"


class MatchEngine:
    """
    Engine for detecting matches and managing the match-3 game logic.
    
    This class handles:
    - Match detection (horizontal and vertical)
    - Score calculation with cascade multipliers
    - Board refilling with gravity
    - Cascading match detection
    """
    
    @staticmethod
    def find_matches(board: Board) -> List[Match]:
        """
        Find all matches on the current board.
        
        Scans all rows for horizontal matches and all columns for vertical matches.
        A match is 3 or more consecutive tiles of the same color.
        
        Args:
            board (Board): The game board to scan.
        
        Returns:
            List[Match]: List of all matches found.
        """
        matches = []
        
        # Find horizontal matches
        for row in range(board.height):
            col = 0
            while col < board.width:
                tile = board.get_tile(row, col)
                
                if tile is None or tile.is_empty():
                    col += 1
                    continue
                
                # Count consecutive tiles of the same color
                color = tile.color
                streak_start = col
                streak_length = 1
                
                while col + streak_length < board.width:
                    next_tile = board.get_tile(row, col + streak_length)
                    if next_tile is not None and next_tile.color == color:
                        streak_length += 1
                    else:
                        break
                
                # If we have 3+ in a row, record the match
                if streak_length >= 3:
                    positions = [(row, c) for c in range(streak_start, streak_start + streak_length)]
                    match = Match(
                        color=color,
                        positions=positions,
                        match_type="HORIZONTAL"
                    )
                    matches.append(match)
                    col += streak_length
                else:
                    col += 1
        
        # Find vertical matches
        for col in range(board.width):
            row = 0
            while row < board.height:
                tile = board.get_tile(row, col)
                
                if tile is None or tile.is_empty():
                    row += 1
                    continue
                
                # Count consecutive tiles of the same color
                color = tile.color
                streak_start = row
                streak_length = 1
                
                while row + streak_length < board.height:
                    next_tile = board.get_tile(row + streak_length, col)
                    if next_tile is not None and next_tile.color == color:
                        streak_length += 1
                    else:
                        break
                
                # If we have 3+ in a column, record the match
                if streak_length >= 3:
                    positions = [(r, col) for r in range(streak_start, streak_start + streak_length)]
                    match = Match(
                        color=color,
                        positions=positions,
                        match_type="VERTICAL"
                    )
                    matches.append(match)
                    row += streak_length
                else:
                    row += 1
        
        return matches
    
    @staticmethod
    def calculate_score(matches: List[Match], cascade_depth: int = 0) -> int:
        """
        Calculate score from matches.
        
        Formula: score = sum(tiles_removed) * 10 * (cascade_depth + 1)
        
        Args:
            matches (List[Match]): List of matches found.
            cascade_depth (int): Current cascade depth. Defaults to 0.
        
        Returns:
            int: Total score for these matches.
        """
        if not matches:
            return 0
        
        tiles_removed = sum(match.count() for match in matches)
        multiplier = cascade_depth + 1
        
        return tiles_removed * 10 * multiplier
    
    @staticmethod
    def apply_gravity(board: Board) -> int:
        """
        Apply gravity to the board: tiles fall down, fill from top.
        
        Args:
            board (Board): The board to modify.
        
        Returns:
            int: The number of new tiles added.
        """
        new_tiles_count = 0
        
        # Process each column
        for col in range(board.width):
            # Collect non-empty tiles in this column
            non_empty = []
            for row in range(board.height):
                tile = board.get_tile(row, col)
                if tile is not None and not tile.is_empty():
                    non_empty.append(tile)
            
            # Clear the column
            for row in range(board.height):
                board.set_tile(row, col, Tile(color=None, row=row, col=col))
            
            # Place non-empty tiles at the bottom
            start_row = board.height - len(non_empty)
            for i, tile in enumerate(non_empty):
                board.set_tile(start_row + i, col, tile)
            
            # Fill the top with new tiles
            for row in range(start_row):
                new_color = random.choice(list(Color))
                new_tile = Tile(color=new_color, row=row, col=col)
                board.set_tile(row, col, new_tile)
                new_tiles_count += 1
        
        return new_tiles_count
    
    @staticmethod
    def process_move_and_matches(
        board: Board,
        cascade_depth: int = 0
    ) -> Tuple[int, int]:
        """
        Process all matches and cascades from the current board state.
        
        This function:
        1. Finds all matches on the board
        2. Removes matched tiles
        3. Applies gravity
        4. Recursively checks for cascading matches
        
        Args:
            board (Board): The board to process.
            cascade_depth (int): Current cascade depth. Defaults to 0.
        
        Returns:
            Tuple[int, int]: (total_score, cascade_depth).
        """
        matches = MatchEngine.find_matches(board)
        
        if not matches:
            return 0, cascade_depth
        
        # Calculate score for this cascade level
        score = MatchEngine.calculate_score(matches, cascade_depth)
        
        # Get all positions to remove (avoid duplicates)
        positions_to_remove: Set[Tuple[int, int]] = set()
        for match in matches:
            positions_to_remove.update(match.positions)
        
        # Remove tiles
        board.remove_tiles(list(positions_to_remove))
        
        # Apply gravity
        MatchEngine.apply_gravity(board)
        
        # Check for cascading matches
        next_cascade_depth = cascade_depth + 1
        cascade_score, final_depth = MatchEngine.process_move_and_matches(
            board,
            next_cascade_depth
        )
        
        return score + cascade_score, final_depth
