# Breakout Game

A classic Breakout arcade game implemented in Python using Pygame, with a JavaScript version for web deployment.

## Features

- Control the paddle with mouse movement
- Colored brick blocks
- Score tracking
- Lives system
- Menu and game over screens
- Sound effects when the ball hits blocks and paddle
- Soft background music
- Web playable version

## Online Demo

Play the game online: [Breakout Game on Vercel](https://breakout-game-mallocode300.vercel.app/)

## Versions

### Python Version (Main Implementation)
- Full featured implementation using Pygame
- Local gameplay with sound effects
- Source for the JavaScript web version

### JavaScript Version (Web Deployment)
- Pure JavaScript/HTML5 Canvas implementation
- Fully playable in any modern browser
- No plugins required
- Deployed on Vercel

## Requirements

### For the Python version:
- Python 3.6+
- Pygame
- Numpy (for sound generation)
- Pygbag (for web deployment)

### For the JavaScript version:
- Any modern web browser

## Installation

1. Clone this repository
2. Install the required packages:

```
pip install -r requirements.txt
```

## How to Play

### Local Python Version:

```
python main.py
```

### Web Version:
Visit [https://breakout-game-mallocode300.vercel.app/](https://breakout-game-mallocode300.vercel.app/) or open `/public/index.html` in your browser.

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

The game is deployed on Vercel using a JavaScript implementation that mimics the Python version's functionality.

### To deploy your own version:

1. Fork this repository
2. Connect it to your Vercel account
3. Deploy using the static site configuration in vercel.json

For local web preview, you can simply open the `/public/index.html` file in your browser.

## Development

- Python code is in `main.py`
- JavaScript web version is in `/public/breakout.js`
- HTML for web version is in `/public/index.html`

## Author

- [Mallory Antomarchi](https://github.com/mallocode300)

## License

This project is open source and available under the [MIT License](LICENSE).

Enjoy playing! 