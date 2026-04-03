# TODO 4: Validation and Prioritization of Requirements

## Requirement Quality Evaluation

All requirements have been evaluated against the quality criteria from the lecture:

### Evaluation Criteria Results

| Criterion | Result | Notes |
|-----------|--------|-------|
| **Measurability** | ✅ PASS | All requirements have verifiable success criteria |
| **Completeness** | ✅ PASS | No gaps identified; all needed aspects covered |
| **Correctness** | ✅ PASS | Requirements flow logically from user needs |
| **Consistency** | ✅ PASS | No contradictions between requirements |
| **Unambiguity** | ✅ PASS | Each requirement is clearly stated with no double meanings |
| **Feasibility** | ✅ PASS | All requirements can be implemented in Python within reasonable scope |
| **Traceability** | ✅ PASS | Each requirement traces back to user needs (see traceability matrix) |

### Quality Revisions Made

The following refinements were applied during specification:

1. **Clarified "Match"** from vague "matching tiles" to "3+ consecutive tiles of identical color in horizontal or vertical lines" (SR-DS3)
2. **Specified Gravity** from unclear "tiles fall" to "gravity acts vertically only, new tiles appear at top" (SR-DS4)
3. **Defined Scoring** from ambiguous "points for matches" to explicit formula: "10 × removed tiles × (cascade depth + 1)" (SR-DS5)
4. **Concrete Thresholds**: Target score = 1000 (SR-DS6), Move limit = 50 (SR-DS7), Board size = 6x6 (SR-DS1)
5. **Explicit Response Time**: "within 100ms" instead of "responsive" (SR-NF1)

---

## MoSCoW Prioritization for First Prototype

### **MUST Have** (Non-negotiable for playable prototype)

These requirements **must** be implemented. Without them, the game is not playable.

#### Functional Requirements - MUST
- **SR-F1**: Board Initialization (6x6, 5 colors)
  - *Rationale*: Essential first step; no board = no game
  
- **SR-F2**: Move Validation (valid swaps only)
  - *Rationale*: Prevents invalid game states
  
- **SR-F3**: Match Detection (3+ in line)
  - *Rationale*: Core mechanic; cannot play without detecting matches
  
- **SR-F4**: Gravity Mechanics (tiles fall, refill)
  - *Rationale*: Game progression depends on this
  
- **SR-F5**: Score Calculation
  - *Rationale*: No win condition without scoring
  
- **SR-F6**: Game State Persistence
  - *Rationale*: Must track board, score, moves
  
- **SR-F7**: Game End Detection (win/lose)
  - *Rationale*: Game must have clear end states
  
- **SR-F8**: Input Processing
  - *Rationale*: Must accept player moves

#### Non-Functional Requirements - MUST
- **SR-NF1**: Response Time <= 100ms
  - *Rationale*: Game must feel responsive
  
- **SR-NF4**: Intuitiveness
  - *Rationale*: Game rules must be self-evident
  
- **SR-NF5**: Python 3.8+ support
  - *Rationale*: Requirement from problem statement
  
- **SR-NF10**: Error Handling
  - *Rationale*: App must not crash on invalid input

#### Domain-Specific Requirements - MUST
- **SR-DS1**: 6x6 Board
- **SR-DS2**: 5 Tile Colors
- **SR-DS3**: Match Definition (3+ in line)
- **SR-DS4**: Gravity Direction (vertical only)
- **SR-DS5**: Scoring Formula
- **SR-DS6**: Win Threshold (1000 points)
- **SR-DS7**: Move Limit (50 moves)

**MUST Count**: 23 requirements

---

### **SHOULD Have** (Important for quality, but not blocking)

These requirements enhance quality and usability but are not strictly necessary for core functionality.

#### Non-Functional Requirements - SHOULD
- **SR-NF2**: Memory Usage <= 100MB
  - *Rationale*: Important for smooth operation; nice-to-have constraint
  
- **SR-NF3**: Startup Time <= 2 seconds
  - *Rationale*: Affects user experience; can be optimized later
  
- **SR-NF6**: Minimal Dependencies
  - *Rationale*: Good practice; ensures portability
  
- **SR-NF7**: PEP-8 Code Style
  - *Rationale*: Maintainability and team standards
  
- **SR-NF8**: Documentation Strings
  - *Rationale*: Future maintenance; should be done properly
  
- **SR-NF9**: Modular Structure
  - *Rationale*: Good engineering; supports future changes

**SHOULD Count**: 6 requirements

---

### **COULD Have** (Nice-to-have, lower priority)

These would enhance the game but can be deferred to later versions if time is limited.

- Cascade animations or visual effects
- Sound effects or background music
- Different difficulty levels
- Move hints or suggestions
- Statistics tracking (best score, games played)
- Color themes or customization

**Note**: Since these are not explicitly in the requirements, they are not formally prioritized here. If implemented, they would be COULD-haves.

**COULD Count**: 0 formal requirements (all are out of scope for prototype)

---

### **WON'T Have** (Explicitly out of scope)

These requirements are explicitly deferred from the first prototype.

- **Cascading chains**: Multiple sequential matches after one move
- **Multiple levels**: Only one playable level for prototype
- **Power-ups**: Special tiles with bonus effects
- **Persistent saves**: No game state save/load
- **Multiplayer**: Single-player only
- **Advanced graphics**: Minimalist UI acceptable
- **Mobile support**: Desktop only
- **Complex animations**: Simple state changes acceptable

---

## Scope Definition for First Playable Prototype: "Must Requirements Only"

The **minimum scope** (MVP) is defined by the **23 MUST requirements**:

### In Scope
✅ 6x6 game board  
✅ 5 tile colors  
✅ Match detection (3+ in lines)  
✅ Simple gravity/refill  
✅ Score tracking (formula-based)  
✅ 50-move limit  
✅ 1000-point win target  
✅ Win/lose detection  
✅ Input handling  
✅ Game state management  
✅ Responsive (< 100ms)  
✅ Non-crashing error handling  
✅ Basic UI (CLI or simple GUI)  

### Out of Scope
❌ Cascading matches  
❌ Multiple levels  
❌ Power-ups  
❌ Animations  
❌ Sound  
❌ Persistent saves  
❌ Multiplayer  
❌ Advanced graphics  

---

## Prioritization Summary

| Priority | Count | Effort (Est.) | Risk |
|----------|-------|---------------|------|
| MUST | 23 | 40-50 hours | Critical path |
| SHOULD | 6 | 10-15 hours | Medium |
| COULD | 0 | - | - |
| WON'T | 7+ | Deferred | Low |

**For the first prototype, focus on MUST requirements.** If time permits, add SHOULD items for better quality.

---

## Consistency Check & Conflict Resolution

### Identified Potential Conflicts
1. **Performance vs. Visual Feedback**: Response time requirement (100ms) might conflict with complex graphics. *Resolution*: Use simple UI (text or basic graphics).
2. **Code Quality vs. Speed**: PEP-8 compliance adds time. *Resolution*: Plan for code review/refactoring in SHOULD phase.

### Cross-Requirement Dependencies
- All functional requirements depend on SR-F6 (Game State)
- Scoring depends on Match Detection (SR-F3)
- Win/Lose depends on Score and Move tracking
- *All dependencies are manageable*

### No Critical Issues Found
All MUST requirements are compatible and feasible.

---

## Next Steps

Proceed with TODO 5 using **MUST requirements as the foundation**. 
SHOULD and COULD features can be added iteratively if time permits.
