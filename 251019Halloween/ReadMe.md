# Ghost Survival 👻

A thrilling survival game where you play as a ghost navigating through a city, following day-night rules while avoiding patrolling police officers.

## Game Description

In **Ghost Survival**, you are a ghost wandering through the city streets, trying to survive as long as possible by following the day-night cycle rules. Be careful - you can only move freely during the night, but must remain completely still during the day to avoid detection!

## Game Features

### 🎮 Core Gameplay
- **Day-Night Cycle**: 3-second days and 8-second nights that gradually speed up
- **Movement Restrictions**: Must stay still during the day, free movement at night
- **Police Patrols**: Officers spawn during nights and move across the screen
- **Treasure Collection**: Collect treasure boxes for bonus points (5 points each)

### 🏆 Survival Mechanics
- **Score System**: Earn 1 point per second survived during night time
- **Increasing Difficulty**: Police speed increases every 15 seconds
- **Time Pressure**: Treasure boxes relocate every 5 seconds if not collected
- **Game Over Conditions**:
  - Moving during daytime (BE DISCOVERED)
  - Colliding with police officers (YOU GET KILLED)

### 🎨 Visual Elements
- Animated ghost character with directional sprites
- Police officers with left/right movement animations
- Day/Night background transitions with visual effects
- Treasure boxes with countdown indicators
- Real-time score and survival time display

## Controls

- **Arrow Keys**: Move ghost (UP, DOWN, LEFT, RIGHT)
- **ESC**: Exit game
- **R**: Restart game (when game over)
- **Mouse Click**: Start game from main menu

## How to Play

1. **Start the game** from the main menu by clicking anywhere
2. **Understand the rules**:
   - Stay still during DAY (white text in top-right)
   - Move freely during NIGHT (white text in top-right)
   - Avoid police officers that patrol during nights
   - Collect treasure boxes for extra points
3. **Survive as long as possible** to achieve a high score!
4. **Watch the day-night cycle** - it gets faster over time!
5. **Collect treasure boxes quickly** - they disappear after 5 seconds

## Technical Requirements

- Python 3.x
- Pygame library
- Required asset folders:
  - `251019Halloween/image/Ghost/` - Ghost sprites
  - `251019Halloween/image/Police/` - Police sprites  
  - `251019Halloween/image/Background/` - Day/Night backgrounds
  - `251019Halloween/image/UI/` - Treasure box image

## Installation

1. Ensure you have Python installed
2. Install Pygame: `pip install pygame`
3. Download or clone this repository
4. Make sure all asset folders are in the correct location
5. Run the game: `python ghost_survival.py`

## Game Strategy Tips

- **Plan your movements** during night time to avoid police patrols
- **Use the full screen** - police enter from both sides
- **Prioritize treasure collection** but don't take unnecessary risks
- **Anticipate day transitions** - stop moving before day begins
- **The game gets harder** - police speed increases over time

## File Structure

```
ghost_survival.py    # Main game file
251019Halloween/
├── image/
│   ├── Ghost/
│   │   ├── GhostLeft/     # Left-facing ghost animations
│   │   └── GhostRight/    # Right-facing ghost animations
│   ├── Police/
│   │   ├── PoliceLeft/    # Left-facing police animations
│   │   └── PoliceRight/   # Right-facing police animations
│   ├── Background/
│   │   ├── Morning.png    # Daytime background
│   │   └── Night.png      # Nighttime background
│   └── UI/
│       └── Box.png        # Treasure box image
```

## Development

This game was built using Python and Pygame, featuring:
- Object-oriented design with separate classes for game entities
- Sprite-based animation system
- Collision detection with adjusted hitboxes
- Time-based game mechanics
- Progressive difficulty scaling

---

## Credits & Attribution

### Game Inspiration
The core gameplay mechanics are inspired by the traditional children's game **"Red Light, Green Light"** (also known as "1, 2, 3, Wooden Man" in some regions), where players must freeze when the caller turns around. This concept was adapted into a digital survival game with day-night cycle mechanics.

### Art Assets
- **Pixel Art**: Generated using [pixie.haus](https://pixie.haus) pixel art generator
- **AI-Assisted Art**: Additional artwork created with Doubao AI image generation
- **Theme Selection**: Halloween theme chosen due to development timing coinciding with the Halloween season

### Development Tools
- **Primary IDE**: Visual Studio Code
- **AI Programming Assistants**:
  - GitHub Copilot for code suggestions and completion
  - ChatGPT for algorithm design and problem-solving
  - Google AI Studio for code optimization and debugging
- **No external source code was referenced** - all code was written specifically for this project

### Technologies Used
- **Python 3.x** as the primary programming language
- **Pygame** library for game development and rendering
- **Object-Oriented Programming** principles for game architecture
