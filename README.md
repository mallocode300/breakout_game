# Breakout Game

A classic Breakout arcade game implemented in Python using Pygame.

## Features

- Control the paddle with mouse movement
- Colored brick blocks
- Score tracking
- Lives system
- Menu and game over screens
- Sound effects when the ball hits blocks and paddle
- Soft background music

## Requirements

- Python 3.6+
- Pygame
- Numpy (for sound generation)
- Pygbag (for web deployment)

## Installation

1. Clone this repository
2. Install the required packages:

```
pip install -r requirements.txt
```

## How to Play

Run the game locally:

```
python main.py
```

### Controls

- Move your mouse to control the paddle
- Click to start the game or restart after game over

## Sound Features

The game includes:
- Sound effects when the ball hits bricks
- Sound effects when the ball hits the paddle
- Background music that plays during the game

If no sound files are found, the game will automatically generate simple sound effects and background music.

## Web Deployment

To deploy the game on the web using Pygbag:

1. Install Pygbag if you haven't already:
```
pip install pygbag
```

2. Run the following command:
```
pygbag main.py
```

3. Open your web browser and go to http://localhost:8000

4. For online deployment, you can host the generated files on any web hosting service like GitHub Pages, Netlify, or Vercel.

## Demo

The game includes:

- A main menu screen
- Gameplay with mouse-controlled paddle
- Colored bricks
- Score tracking
- Game over screen with final score

Enjoy playing! 