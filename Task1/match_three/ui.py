"""
Module: ui.py
Purpose: User interface for the match-3 game (command-line interface).
"""

import sys
from typing import Tuple, Optional
from game import Game, GameState


class GameUI:
    """
    Command-line user interface for the match-3 game.
    
    Handles:
    - Displaying the game board
    - Getting player input
    - Showing game status
    - Game loop management
    """
    
    def __init__(self):
        """Initialize the UI and game."""
        self.game = Game()
    
    def clear_screen(self) -> None:
        """
        Clear the terminal screen.
        
        Works on Windows, macOS, and Linux.
        """
        try:
            import os
            os.system("clear" if sys.platform != "win32" else "cls")
        except Exception:
            # If clearing fails, just print newlines
            print("\n" * 50)
    
    def display_welcome(self) -> None:
        """Display welcome message and game instructions."""
        self.clear_screen()
        print("=" * 50)
        print("MATCH-3 PUZZLE GAME".center(50))
        print("=" * 50)
        print()
        print("OBJECTIVE:")
        print("  - Reach a score of 1000 points before running out of moves")
        print("  - You have 50 moves total")
        print()
        print("HOW TO PLAY:")
        print("  1. The board is a 6x6 grid with colored tiles (R, B, G, Y, P)")
        print("  2. Select two ADJACENT tiles (up, down, left, right)")
        print("  3. If swapping creates a match of 3+ same-colored tiles,")
        print("     they are removed and you gain points")
        print("  4. Tiles fall down to fill empty spaces (gravity)")
        print("  5. New tiles appear at the top")
        print()
        print("SCORING:")
        print("  - 10 points per removed tile")
        print("  - Cascade multiplier applies if new matches occur after refill")
        print()
        print("=" * 50)
    
    def display_board(self) -> None:
        """
        Display the current game board.
        
        Shows the board grid with row/column labels.
        """
        print("\nCurrent Board:")
        print(self.game.board.display())
        print()
    
    def display_status(self) -> None:
        """
        Display the current game status.
        
        Shows score, moves remaining, and game state.
        """
        print(self.game.get_status())
        print()
    
    def get_tile_input(self) -> Tuple[Optional[int], Optional[int]]:
        """
        Get a tile position from the player.
        
        Returns:
            Tuple[int, int]: (row, col) if valid, (None, None) if invalid.
        """
        while True:
            try:
                user_input = input("Enter row and col (e.g., '0 1'): ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("Thanks for playing!")
                    sys.exit(0)
                
                parts = user_input.split()
                if len(parts) != 2:
                    print("Invalid input. Please enter row and column separated by space.")
                    continue
                
                row = int(parts[0])
                col = int(parts[1])
                
                if not (0 <= row < 6 and 0 <= col < 6):
                    print("Positions must be between 0 and 5.")
                    continue
                
                return row, col
            
            except ValueError:
                print("Invalid input. Please enter two integers.")
            except KeyboardInterrupt:
                print("\nGame interrupted. Goodbye!")
                sys.exit(0)
    
    def run_game_loop(self) -> None:
        """
        Run the main game loop.
        
        Continues until the game reaches WON or LOST state.
        """
        while self.game.game_state == GameState.PLAYING:
            self.display_board()
            self.display_status()
            
            # Get first tile
            print("Select first tile:")
            row1, col1 = self.get_tile_input()
            
            # Get second tile
            print("Select second tile (must be adjacent):")
            row2, col2 = self.get_tile_input()
            
            # Attempt move
            success, message = self.game.make_move(row1, col1, row2, col2)
            print(f"Result: {message}")
            print()
            
            if not success:
                input("Press Enter to continue...")
            
            self.clear_screen()
        
        # Game ended
        self.display_board()
        self.display_status()
        
        if self.game.game_state == GameState.WON:
            print("🎉 YOU WON! 🎉".center(50))
        else:
            print("💔 GAME OVER 💔".center(50))
        
        print()
    
    def run(self) -> None:
        """
        Run the complete game session.
        
        Displays welcome, runs game loop, and allows replay.
        """
        self.display_welcome()
        input("Press Enter to start...")
        
        play_again = True
        while play_again:
            self.clear_screen()
            self.game.reset()
            self.run_game_loop()
            
            print("\nWould you like to play again? (yes/no)")
            response = input("Enter choice: ").strip().lower()
            play_again = response in ['yes', 'y']
            self.clear_screen()
        
        print("Thanks for playing! Goodbye!")
