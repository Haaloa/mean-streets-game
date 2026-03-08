# # Mean Streets Game - Design Patterns Implementation

**Kurs:** PA1458 Object Oriented Design  
**Grupp:** 7  
**Datum:** 2026-02-27

Location-based adventure game implementing Strategy Pattern, Singleton Pattern, and Use Case Controller Pattern.

---

## Project Overview

Mean Streets is a location-based adventure game where players interact with objects using different interaction strategies. This implementation demonstrates three key design patterns as part of our Object-Oriented Design course.

### Design Patterns Implemented:

1. **Strategy Pattern** - 8 different interaction types as separate classes
2. **Singleton Pattern** - EventManager with single instance
3. **Use Case Controller Pattern** - Separation of concerns between Game and Controllers

---

## Project Structure

```
mean-streets-game/
├── strategies/              # Strategy Pattern implementations
│   ├── interaction_strategy.py
│   ├── person1_strategies.py  (Look, Open, Move, TurnOn)
│   └── person2_strategies.py  (TurnOff, Taste, PickUp, Drop)
├── models/                  # Domain classes
│   ├── game_object.py       # Context for Strategy Pattern
│   ├── scene.py             # Manages objects in scenes
│   └── event_manager.py     # Singleton Pattern
├── controllers/             # Use Case Controllers
│   ├── game.py              # Main game controller
│   └── interaction_controller.py
├── tests/                   # Unit tests
│   ├── test_person5.py
│   ├── test_strategies.py
│   └── test_integration.py
├── main.py                  # Demo program
└── README.md
```

---

## Getting Started

### Prerequisites

- Python 3.7 or higher
- Git

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR-USERNAME/mean-streets-game.git
   cd mean-streets-game
   ```

2. **Run the demo:**
   ```bash
   python3 main.py
   ```

3. **Run tests:**
   ```bash
   python3 -m pytest tests/
   # or
   python3 tests/test_person5.py
   ```

---

## Team Members & Responsibilities

| Person | Responsibility | Files | Status |
|--------|---------------|-------|--------|
| **Person 1** | Strategy Pattern (Part 1) | LookStrategy, OpenStrategy, MoveStrategy, TurnOnStrategy | ⏳ In Progress |
| **Person 2** | Strategy Pattern (Part 2) | TurnOffStrategy, TasteStrategy, PickUpStrategy, DropStrategy | ⏳ In Progress |
| **Person 3** | Singleton Pattern | EventManager | ⏳ In Progress |
| **Person 4** | Controllers | Game, InteractionController | ⏳ In Progress |
| **Person 5** | Domain & Integration | GameObject, Scene, main.py, tests | ✅ Complete |

---

## Design Patterns

### 1. Strategy Pattern

**Problem:** Different interaction types with if-statements causing low cohesion.

**Solution:** 8 separate strategy classes implementing `InteractionStrategy` interface.

**Classes:**
- `LookAtStrategy` - View object description
- `OpenItStrategy` - Open objects
- `MoveItStrategy` - Move objects
- `TurnItOnStrategy` - Turn on objects
- `TurnItOffStrategy` - Turn off objects
- `TasteItStrategy` - Taste objects
- `PickItUpStrategy` - Pick up objects (adds to inventory)
- `DropItStrategy` - Drop objects (removes from inventory)

**Benefits:**
- High Cohesion - each class has one responsibility
- Low Coupling - GameObject depends on interface, not concrete classes
- Open/Closed Principle - easy to add new interaction types

### 2. Singleton Pattern

**Problem:** Multiple EventManager instances causing inconsistent state.

**Solution:** Singleton pattern ensuring only one instance exists.

**Implementation:**
```python
class EventManager:
    _instance = None
    
    @classmethod
    def getSharedInstance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
```

**Benefits:**
- Guaranteed single instance
- Global access point
- Consistent event state

### 3. Use Case Controller Pattern

**Problem:** Game class with 50+ methods causing low cohesion.

**Solution:** Separate controller for each use case.

**Before:**
- Game: LOW COHESION (50+ methods for all use cases)

**After:**
- Game: HIGH COHESION (5 methods - game state only)
- InteractionController: HIGH COHESION (5 methods - interact use case only)

**Benefits:**
- High Cohesion - each class has focused responsibility
- Low Coupling - controllers are independent
- Single Responsibility Principle

---

## Testing

### Run all tests:
```bash
python3 -m pytest tests/ -v
```

### Run specific test file:
```bash
python3 tests/test_person5.py
```

### Expected output:
```
============================================================
RUNNING PERSON 5 TESTS
============================================================
test_add_strategy ... ok
test_available_strategies ... ok
test_create_game_object ... ok
...

Ran 11 tests in 0.001s

OK 
```

---

## Usage Example

```python
from controllers.game import Game

# Create game
game = Game()

# Get interaction controller
ic = game.createInteractionController()

# Interact with object
ic.pickGameObject("phone")
ic.chooseInteraction("look")
result = ic.performInteraction()

print(result)  # "You look at the phone. A black rotary phone..."
```

---

## Git Workflow

### Before starting work:
```bash
git pull
```

### After completing work:
```bash
git add .
git commit -m "Person X: Description of changes"
git push
```

### Commit message format:
```
Person X: Brief description

- What was added/changed
- Why it was needed
```

---

## GRASP Patterns Applied

- **Controller** - InteractionController handles system events
- **Information Expert** - GameObject knows its available strategies
- **Polymorphism** - Strategy Pattern uses inheritance instead of if-statements
- **Pure Fabrication** - Strategies and Controllers are technical classes
- **Low Coupling** - Interface-based dependencies
- **High Cohesion** - Each class has focused responsibility
- **Protected Variations** - InteractionStrategy interface protects from changes

---

## Course Information

**Course:** PA1458 Object Oriented Design  
**Assignment:** Refactored Class Diagram + Demo Implementation  
**University:** Blekinge Institute of Technology  
**Year:** 2026

---

## License

This is a student project for educational purposes.

---

## Contributing

This is a closed group project. Only team members can contribute.

### For team members:

1. Pull latest changes: `git pull`
2. Create/edit your files
3. Test your code: `python3 your_file.py`
4. Commit: `git commit -m "Person X: Description"`
5. Push: `git push`

---

## Contact

For questions about this project, contact any team member.

---

## Current Status

**Project Completion:** 20%

- [ ] Project structure created
- [ ] GameObject implemented (Person 5)
- [ ] Scene implemented (Person 5)
- [ ] main.py with mocks (Person 5)
- [ ] Unit tests for Person 5
- [ ] Strategy Pattern Part 1 (Person 1)
- [ ] Strategy Pattern Part 2 (Person 2)
- [ ] Singleton EventManager (Person 3)
- [ ] Game & Controllers (Person 4)
- [ ] Integration (All together)
- [ ] Final testing
- [ ] Demo preparation

---

**Last Updated:** 2026-03-08

**Ready for Demo:** Not yet - Integration pending
