"""
Module: game.py
Purpose: Main game class managing game state, moves, and win/lose conditions.
"""

from enum import Enum
from typing import Tuple, Optional
from board import Board
from match_engine import MatchEngine


class GameState(Enum):
    """
    Enumeration of possible game states.
    
    Attributes:
        PLAYING: Game is in progress.
        WON: Player reached target score before running out of moves.
        LOST: Player ran out of moves without reaching target score.
    """
    
    PLAYING = "PLAYING"
    WON = "WON"
    LOST = "LOST"


class Game:
    """
    Main game class managing the match-3 game logic.
    
    Attributes:
        board (Board): The current game board.
        score (int): Current accumulated score.
        remaining_moves (int): Number of moves remaining.
        game_state (GameState): Current state of the game.
        target_score (int): Score needed to win.
        move_limit (int): Maximum number of moves allowed.
    """
    
    TARGET_SCORE = 1000
    MOVE_LIMIT = 50
    
    def __init__(self):
        """
        Initialize a new game.
        
        Creates a new board, resets score and moves, and sets game to PLAYING.
        """
        self.board = Board()
        self.score = 0
        self.remaining_moves = self.MOVE_LIMIT
        self.game_state = GameState.PLAYING
        self.target_score = self.TARGET_SCORE
        self.move_limit = self.MOVE_LIMIT
    
    def is_valid_move(self, row1: int, col1: int, row2: int, col2: int) -> bool:
        """
        Check if a move is valid.
        
        A move is valid if:
        1. Game is in PLAYING state
        2. Both positions have valid tiles
        3. Positions are adjacent
        4. Swapping them would result in a match
        
        Args:
            row1 (int): Row of first tile.
            col1 (int): Column of first tile.
            row2 (int): Row of second tile.
            col2 (int): Column of second tile.
        
        Returns:
            bool: True if move is valid, False otherwise.
        """
        if self.game_state != GameState.PLAYING:
            return False
        
        if not self.board.are_adjacent(row1, col1, row2, col2):
            return False
        
        # Test the swap to see if it creates a match
        test_board = self.board.copy()
        
        if not test_board.swap_tiles(row1, col1, row2, col2):
            return False
        
        matches = MatchEngine.find_matches(test_board)
        return len(matches) > 0
    
    def make_move(self, row1: int, col1: int, row2: int, col2: int) -> Tuple[bool, str]:
        """
        Attempt to make a move.
        
        Args:
            row1 (int): Row of first tile.
            col1 (int): Column of first tile.
            row2 (int): Row of second tile.
            col2 (int): Column of second tile.
        
        Returns:
            Tuple[bool, str]: (success, message).
                - (True, ""): Move successful
                - (False, error_message): Move failed with reason
        """
        # Validate move
        if self.game_state != GameState.PLAYING:
            return False, "Game is not in progress."
        
        if not self.board.are_adjacent(row1, col1, row2, col2):
            return False, "Selected tiles are not adjacent. Choose adjacent tiles."
        
        # Attempt swap
        if not self.board.swap_tiles(row1, col1, row2, col2):
            return False, "Invalid position. Please select valid tile positions."
        
        # Check for matches
        matches = MatchEngine.find_matches(self.board)
        
        if not matches:
            # Revert the swap
            self.board.swap_tiles(row1, col1, row2, col2)
            return False, "No matches found. Move reverted."
        
        # Valid move! Process matches and cascades
        score_gained, cascade_depth = MatchEngine.process_move_and_matches(self.board)
        
        self.score += score_gained
        self.remaining_moves -= 1
        
        # Check win/lose conditions
        self._check_end_conditions()
        
        return True, f"Success! Gained {score_gained} points."
    
    def _check_end_conditions(self) -> None:
        """
        Check if the game has reached a win or lose condition.
        
        Updates game_state to WON or LOST if conditions are met.
        """
        if self.score >= self.target_score:
            self.game_state = GameState.WON
        elif self.remaining_moves <= 0:
            self.game_state = GameState.LOST
    
    def has_valid_moves(self) -> bool:
        """
        Check if there are any valid moves available on the board.
        
        This is an optional check that can be used to detect lose conditions
        earlier than waiting for move limit.
        
        Returns:
            bool: True if at least one valid move exists, False otherwise.
        """
        if self.game_state != GameState.PLAYING:
            return False
        
        for row1 in range(self.board.height):
            for col1 in range(self.board.width):
                for row2 in range(self.board.height):
                    for col2 in range(self.board.width):
                        if self.is_valid_move(row1, col1, row2, col2):
                            return True
        
        return False
    
    def get_status(self) -> str:
        """
        Get a human-readable status message.
        
        Returns:
            str: Status message with score, moves, and game state.
        """
        status = f"Score: {self.score}/{self.target_score} | "
        status += f"Moves: {self.remaining_moves}/{self.move_limit}\n"
        status += f"State: {self.game_state.value}"
        
        if self.game_state == GameState.WON:
            status += " - Congratulations! You won!"
        elif self.game_state == GameState.LOST:
            status += " - Game Over! You lost."
        
        return status
    
    def reset(self) -> None:
        """
        Reset the game to an initial state.
        
        Creates a new board and resets score, moves, and game state.
        """
        self.board = Board()
        self.score = 0
        self.remaining_moves = self.MOVE_LIMIT
        self.game_state = GameState.PLAYING
