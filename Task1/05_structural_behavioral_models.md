# TODO 5: Structural and Behavioral Models

## Conceptual Domain Model

### Main Entities and Attributes

```
GAME
├── board: Board
├── current_score: int
├── remaining_moves: int
├── game_state: GameState (PLAYING, WON, LOST)
├── target_score: int = 1000
└── move_limit: int = 50

BOARD
├── tiles: List[List[Tile]]  (6x6 grid)
├── width: int = 6
├── height: int = 6
└── Operations:
    ├── get_tile(row, col) -> Tile
    ├── swap_tiles(row1, col1, row2, col2) -> bool
    ├── remove_tiles(positions: List[(row, col)])
    └── apply_gravity() -> List[(row, col)]

TILE
├── color: Color (RED, BLUE, GREEN, YELLOW, PURPLE)
├── row: int
├── col: int
└── is_empty: bool = False

MATCH
├── color: Color
├── tiles: List[Tile]
├── match_type: MatchType (HORIZONTAL, VERTICAL)
└── cascade_depth: int
```

### Entity Relationships

```
GAME ──1──► BOARD
GAME ──1──► LIST[MOVE]
BOARD ──36──► TILE (6x6 grid)
MOVE ──1──► (Tile, Tile)  [two tiles swapped]
MATCH ──1──► LIST[TILE]   [tiles that matched]
```

### Attributes and Data Types

| Entity | Attribute | Type | Range | Default |
|--------|-----------|------|-------|---------|
| GAME | current_score | int | 0-∞ | 0 |
| GAME | remaining_moves | int | 0-50 | 50 |
| GAME | game_state | enum | {PLAYING, WON, LOST} | PLAYING |
| BOARD | width | int | 6 | 6 |
| BOARD | height | int | 6 | 6 |
| TILE | color | enum | {R, B, G, Y, P} | random |
| TILE | row | int | 0-5 | varies |
| TILE | col | int | 0-5 | varies |
| MATCH | cascade_depth | int | 0-∞ | 0 |

---

## Behavioral Models

### 1. Detailed Use Case: "Player Makes a Move"

**Use Case Name**: Make a Move and Check for Matches

**Actor**: Player

**Preconditions**:
- Game is in PLAYING state
- Board is initialized with tiles
- Remaining moves > 0

**Main Flow**:

1. Player sees the game board with 6x6 grid of colored tiles
2. Player selects a tile by clicking/entering row and column
3. System highlights selected tile
4. Player selects an adjacent tile (up, down, left, or right)
5. System validates adjacency
6. System swaps the two tiles on the board
7. System searches board for matches (horizontal & vertical)
8. **IF matches found**:
   - System removes all matched tiles (set to empty)
   - System increments score based on: 10 × tiles_removed × (cascade_depth + 1)
   - System applies gravity (tiles fall downward)
   - System generates new tiles at top of empty columns
   - System checks for cascading matches (Step 7 repeats)
   - System decrements remaining_moves by 1
   - Player sees updated board and score
9. **ELSE (no matches)**:
   - System swaps tiles back to original positions
   - Player is notified "Invalid move - no match!"
   - No moves decremented
   - Board remains unchanged
10. System checks win/lose conditions:
    - **IF** current_score >= 1000: Game state = WON
    - **ELSE IF** remaining_moves == 0 AND current_score < 1000: Game state = LOST
    - **ELSE**: Continue to step 1

**Postconditions**:
- Board is updated and valid
- Score may be incremented
- Move count may be decremented
- Game state is checked

**Alternative Flows**:
- **A1**: Player selects invalid tile → Error message displayed
- **A2**: Player selects non-adjacent tile → Error message "Selection must be adjacent!"
- **A3**: Match occurs but creates cascades → Loop continues until no matches remain

---

### 2. Gameplay State Machine

The following diagram represents the finite state machine for the game flow:

```
                   START
                     │
                     ▼
        ┌─────────────────────────┐
        │  INITIALIZE_BOARD       │
        │  • Create 6x6 grid      │
        │  • Fill with tiles      │
        │  • score = 0            │
        │  • moves = 50           │
        └──────────┬──────────────┘
                   │
                   ▼
        ┌─────────────────────────┐
        │  PLAYING                │◄──────────────────────┐
        │  • Board displayed      │                       │
        │  • Awaiting player move │                       │
        └──────────┬──────────────┘                       │
                   │                                       │
                   ▼                                       │
        ┌─────────────────────────┐                       │
        │  PROCESS_MOVE           │                       │
        │  • Validate swap        │                       │
        │  • Swap tiles           │                       │
        │  • Find matches         │                       │
        └──────────┬──────────────┘                       │
                   │                                       │
         ┌─────────┴─────────┐                            │
         │                   │                            │
    YES  ▼               NO  ▼                            │
   ┌──────────┐       ┌──────────────┐                   │
   │ MATCHES  │       │ NO_MATCHES   │                   │
   │ FOUND?   │       │ • Revert     │───────────────────┘
   └────┬─────┘       │   swap       │
        │             │ • Deduct 0   │
        │             │   moves      │
        │             └──────────────┘
        ▼
   ┌──────────────────────┐
   │ REMOVE_TILES         │
   │ • Mark tiles empty   │
   │ • Add score points   │
   │ • Deduct 1 move      │
   └──────────┬───────────┘
              │
              ▼
   ┌──────────────────────┐
   │ APPLY_GRAVITY        │
   │ • Drop tiles down    │
   │ • Fill new tiles top │
   └──────────┬───────────┘
              │
              ▼
   ┌──────────────────────┐   YES
   │ CASCADING_MATCH?     ├────────┐
   │ • Check for matches  │        │
   └──────────┬───────────┘        │
              │ NO                 │
              │              (loop to REMOVE_TILES)
              ▼
   ┌──────────────────────┐
   │ CHECK_END_CONDITIONS │
   └──────────┬───────────┘
        ┌─────┴──────────────┐
        │                    │
    YES ▼                    ▼ NO
   ┌──────────┐      ┌──────────────┐
   │ SCORE >=1000?    │ MOVES == 0?  │
   │ WON = YES  │      │ LOST = YES   │
   │ (or MOVES=0│      │ (moves out)  │
   │  LOST)     │      └──────────────┘
   └──────────┘
        │
        │ NO (both False)
        └──────────────────────────┐
                                   │
                          (back to PLAYING)
```

---

### 3. Match Detection Algorithm

**Algorithm**: Horizontal and Vertical Match Finder

**Input**: Board with 6x6 grid of tiles

**Process**:

```
matches = []

# Horizontal matches
FOR each row in board:
    current_color = None
    streak_start = 0
    streak_length = 0
    
    FOR each col in row:
        tile = board[row][col]
        IF tile.color == current_color:
            streak_length += 1
        ELSE:
            IF streak_length >= 3:
                matches.append(MATCH(
                    color=current_color,
                    positions=[(row, c) for c in range(streak_start, streak_start + streak_length)],
                    type=HORIZONTAL
                ))
            current_color = tile.color
            streak_start = col
            streak_length = 1
    
    IF streak_length >= 3:
        matches.append(MATCH(...))  # Final check

# Vertical matches (same logic, swapping row/col)
FOR each col in board[0]:
    current_color = None
    streak_start = 0
    streak_length = 0
    
    FOR each row in col:
        tile = board[row][col]
        IF tile.color == current_color:
            streak_length += 1
        ELSE:
            IF streak_length >= 3:
                matches.append(MATCH(
                    color=current_color,
                    positions=[(r, col) for r in range(streak_start, streak_start + streak_length)],
                    type=VERTICAL
                ))
            current_color = tile.color
            streak_start = row
            streak_length = 1
    
    IF streak_length >= 3:
        matches.append(MATCH(...))

RETURN matches
```

**Complexity**: O(height × width) = O(36) for 6x6 board  
**Output**: List of MATCH objects

---

### 4. Tile Removal and Refill Process

**Step 1: Identify Tiles to Remove**
```
tiles_to_remove = UNION of all tiles in all matches
FOR each tile in tiles_to_remove:
    board[tile.row][tile.col] = EMPTY
    score += 10 (score calculated at end with cascade multiplier)
```

**Step 2: Apply Gravity**
```
FOR each column (left to right):
    non_empty_tiles = [t for t in column if t is not EMPTY]  (ordered bottom-to-top)
    
    FOR each position in column (bottom to top):
        IF position_index < len(non_empty_tiles):
            board[position] = non_empty_tiles[position_index]
        ELSE:
            board[position] = EMPTY  (top positions now empty)
```

**Step 3: Refill Empty Positions**
```
FOR each column (left to right):
    empty_count = count of EMPTY tiles in column
    
    FOR i in range(empty_count):
        new_tile = generate_random_tile(one_of_5_colors)
        board[i][column] = new_tile  (add at top)
```

**Step 4: Cascade Check**
```
new_matches = find_matches(board)
IF new_matches is not empty:
    cascade_depth += 1
    score_multiplier = cascade_depth + 1
    REMOVE_TILES_AND_REFILL()  (recursive)
```

---

### 5. Conceptual State Transitions

```
┌──────────────────────────────────────────────────────────┐
│                   GAME STATE MACHINE                      │
├──────────────────────────────────────────────────────────┤
│                                                            │
│  Initial State: PLAYING (after board init)                │
│                                                            │
│  Transitions:                                              │
│  • PLAYING → WON  (if score >= 1000)                      │
│  • PLAYING → LOST (if moves == 0 AND score < 1000)       │
│  • PLAYING stays (move processed, continue)               │
│                                                            │
└──────────────────────────────────────────────────────────┘
```

---

## Summary of Models

- **Structural**: Board (6x6), Tiles (5 colors), Match, Game state
- **Behavioral**: 
  - State Machine with 5 states (Init, Playing, *Process Move, Remove, Apply Gravity, Check Cascade, Check End)
  - Use Case for "Make a Move"
  - Match Detection Algorithm (O(36))
  - Tile Removal and Refill with cascading logic
  
All models support the MUST requirements and are ready for implementation.
