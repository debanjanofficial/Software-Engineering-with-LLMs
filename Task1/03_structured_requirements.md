# TODO 3: Structured Requirements

## User Requirements (What users need the system to do)

### UR1: Board Display
- **Description**: The player must see the game board with all tiles clearly visible
- **Rationale**: Visual feedback is essential for gameplay
- **Verification**: Board is rendered on startup and after each move

### UR2: Tile Interaction
- **Description**: The player can select a tile and swap it with an adjacent tile (left, right, up, down)
- **Rationale**: Core gameplay mechanic
- **Verification**: Clicking/selecting two adjacent tiles results in their swap

### UR3: Match Detection
- **Description**: After each move, the system automatically detects and identifies all matches (3+ tiles in a line)
- **Rationale**: Fundamental to match-3 gameplay
- **Verification**: Matching tiles are removed after move validation

### UR4: Board Refill
- **Description**: After matches are removed, empty spaces are filled with new tiles by gravity
- **Rationale**: Keeps gameplay flowing
- **Verification**: Tiles fall to fill empty spaces

### UR5: Scoring
- **Description**: The player accumulates score points for matched tiles
- **Rationale**: Provides progression feedback
- **Verification**: Score increases by correct amount after each move

### UR6: Game Status
- **Description**: The player can see current score and remaining moves
- **Rationale**: Player needs to understand game state
- **Verification**: Score and move counter displayed at all times

### UR7: Win Condition
- **Description**: Player wins when the score reaches a target value (e.g., 1000 points)
- **Rationale**: Defines success criteria
- **Verification**: Game shows win message when target reached

### UR8: Lose Condition
- **Description**: Player loses when all moves are spent or no valid moves exist
- **Rationale**: Defines failure criteria and game limits
- **Verification**: Game shows lose message when condition met

---

## System Requirements

### SR-F: Functional Requirements

#### SR-F1: Board Initialization
- **Description**: System shall initialize a 6x6 game board with random tiles from 5 colors
- **Type**: Functional
- **Verifiable**: Board contains exactly 36 tiles, each one of 5 colors randomly distributed

#### SR-F2: Move Validation
- **Description**: System shall accept only valid moves (swapping adjacent tiles that result in a match)
- **Type**: Functional
- **Verifiable**: Swap is only completed if resulting board contains at least one match

#### SR-F3: Match Detection Algorithm
- **Description**: System shall identify all horizontal and vertical matches of 3 or more consecutive tiles of the same color
- **Type**: Functional, Domain-Specific
- **Verifiable**: Algorithm correctly identifies all matches given any board state
- **Algorithm**: Scan each row and column for sequences of 3+ identical tiles

#### SR-F4: Gravity Mechanics
- **Description**: System shall apply gravity to fill empty spaces; tiles fall vertically, new tiles appear at top
- **Type**: Functional, Domain-Specific
- **Verifiable**: After tile removal, all empty spaces are filled with new tiles

#### SR-F5: Score Calculation
- **Description**: System shall calculate score as: 10 points per removed tile, multiplied by cascade depth
- **Type**: Functional
- **Verifiable**: Score increases correctly after matches

#### SR-F6: Game State Persistence
- **Description**: System shall maintain and update game state (board, score, move count)
- **Type**: Functional
- **Verifiable**: Game state accurately reflects all actions

#### SR-F7: Game End Detection
- **Description**: System shall detect winning (score >= 1000) or losing (moves == 0 OR no valid moves)
- **Type**: Functional
- **Verifiable**: Game ends at correct time with correct message

#### SR-F8: Input Processing
- **Description**: System shall accept tile selection input and process it within 100ms
- **Type**: Functional
- **Verifiable**: User action produces visible result within 100ms

---

### SR-NF: Non-Functional Requirements

#### SR-NF1: Performance - Response Time
- **Description**: Each move shall be processed and displayed within 100 milliseconds
- **Type**: Non-Functional (Product Quality)
- **Measurement**: Latency between action and visual feedback <= 100ms
- **Verification**: Measure response time during gameplay

#### SR-NF2: Performance - Memory Usage
- **Description**: Application shall use no more than 100MB of RAM during gameplay
- **Type**: Non-Functional (Product Quality)
- **Measurement**: Peak memory footprint <= 100MB
- **Verification**: Monitor memory usage during extended play

#### SR-NF3: Performance - Startup
- **Description**: Application shall start and display the game board within 2 seconds
- **Type**: Non-Functional (Product Quality)
- **Measurement**: Time from launch to playable state <= 2 seconds
- **Verification**: Measure launch time

#### SR-NF4: Usability - Intuitiveness
- **Description**: Game rules must be understandable without documentation within 1 minute of starting
- **Type**: Non-Functional (Product Quality)
- **Measurement**: Display clear board, obvious controls
- **Verification**: User testing or self-assessment

#### SR-NF5: Compatibility - Platform
- **Description**: Application shall run on Python 3.8+ on Windows, macOS, and Linux
- **Type**: Non-Functional (External Requirement)
- **Measurement**: Compatible with 3 major OS families
- **Verification**: Test on all target platforms

#### SR-NF6: Compatibility - Dependencies
- **Description**: Shall use only standard Python libraries or widely-available packages (e.g., pygame, tkinter)
- **Type**: Non-Functional (External Requirement)
- **Measurement**: pip install should succeed without compilation
- **Verification**: Check dependency availability

#### SR-NF7: Code Quality - Style
- **Description**: Code shall conform to PEP-8 Python style guide
- **Type**: Non-Functional (Organizational Requirement)
- **Measurement**: pylint/flake8 compliance
- **Verification**: Run linter on codebase

#### SR-NF8: Code Quality - Documentation
- **Description**: All public functions shall have docstrings explaining purpose, parameters, and return values
- **Type**: Non-Functional (Organizational Requirement)
- **Measurement**: 100% of functions have docstrings
- **Verification**: Inspect code manually or use documentation tools

#### SR-NF9: Code Quality - Maintainability
- **Description**: Code shall be organized into logical modules with clear separation of concerns
- **Type**: Non-Functional (Organizational Requirement)
- **Measurement**: Modules exist for: board, logic, UI, game state
- **Verification**: Code review

#### SR-NF10: Reliability - Error Handling
- **Description**: Application shall handle invalid input gracefully and not crash
- **Type**: Non-Functional (Product Quality)
- **Measurement**: Try various invalid inputs, app should not crash
- **Verification**: Test with edge cases

---

### SR-DS: Domain-Specific Requirements

#### SR-DS1: Board Configuration
- **Description**: Game board dimensions shall be exactly 6x6 (36 tiles total)
- **Type**: Domain-Specific (Constraint)
- **Rationale**: Balances playability and performance

#### SR-DS2: Tile Colors
- **Description**: Each tile shall be one of 5 distinct colors, assigned randomly at initialization
- **Type**: Domain-Specific (Constraint)
- **Rationale**: Provides variety while keeping matches possible

#### SR-DS3: Match Definition
- **Description**: A match is defined as 3 or more consecutive tiles of the identical color in a single row or column
- **Type**: Domain-Specific (Constraint)
- **Rationale**: Canonical match-3 rule

#### SR-DS4: Gravity Direction
- **Description**: Gravity shall act downward only; tiles fall vertically but not diagonally
- **Type**: Domain-Specific (Constraint)
- **Rationale**: Simplifies mechanics for first prototype

#### SR-DS5: Scoring Formula
- **Description**: Score = (number of tiles removed) × 10 × (cascade depth + 1)
- **Type**: Domain-Specific (Constraint)
- **Rationale**: Incentivizes larger matches and cascades

#### SR-DS6: Win Threshold
- **Description**: Player wins when accumulated score reaches 1000 points
- **Type**: Domain-Specific (Constraint)
- **Rationale**: Provides clear goal; adjustable if needed

#### SR-DS7: Move Limit
- **Description**: Player has a maximum of 50 moves to reach the target score
- **Type**: Domain-Specific (Constraint)
- **Rationale**: Creates challenge and time pressure

---

## Requirement Relationships & Dependencies

### Dependencies:
- SR-F3 (Match Detection) must be implemented before SR-F2 (Move Validation)
- SR-F4 (Gravity) depends on SR-F3 (tiles only fall after matches)
- SR-F5 (Scoring) depends on SR-F3 (must know which tiles matched)
- SR-F7 (Game End) depends on SR-F5 and SR-F4 (checking win/lose conditions)

### Conflicts:
- **None identified** at this level. All requirements are complementary.

### Overlaps:
- SR-F6 (Game State) and SR-F1 to SR-F7 are interconnected; game state is updated by functional requirements.

---

## Traceability Matrix

| User Need | System Requirement | Verification Method |
|-----------|-------------------|---------------------|
| UR2 (Tile Interaction) | SR-F2 (Move Validation) | Test valid/invalid swaps |
| UR3 (Match Detection) | SR-F3 (Match Detection) | Algorithm test suite |
| UR4 (Board Refill) | SR-F4 (Gravity Mechanics) | Visual verification |
| UR5 (Scoring) | SR-F5 (Score Calculation) | Calculate scores manually |
| UR6 (Game Status) | SR-F6 (Game State Persistence) | Display verification |
| UR7 (Win Condition) | SR-F7 (Game End Detection) | Reach 1000 points |
| UR8 (Lose Condition) | SR-F7 (Game End Detection) | Exhaust moves |
| All | SR-NF7-9 (Code Quality) | Code review |

---

## Summary

**Total Functional Requirements**: 8  
**Total Non-Functional Requirements**: 10  
**Total Domain-Specific Requirements**: 7  
**Total System Requirements**: 25

All requirements are mapped to user needs and are verifiable and feasible for a first prototype.
