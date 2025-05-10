// Breakout Game JavaScript version
// Based on the Python implementation

// Game constants
const SCREEN_WIDTH = 800;
const SCREEN_HEIGHT = 600;

// Colors
const WHITE = "#FFFFFF";
const BLACK = "#000000";
const BLUE = "#0000FF";
const RED = "#FF0000";
const GREEN = "#00FF00";
const YELLOW = "#FFFF00";
const ORANGE = "#FFA500";

// Paddle properties
const PADDLE_WIDTH = 100;
const PADDLE_HEIGHT = 20;
const PADDLE_SPEED = 10;

// Ball properties
const BALL_RADIUS = 10;
const BALL_SPEED_X = 4;
const BALL_SPEED_Y = -4;

// Brick properties
const BRICK_WIDTH = 80;
const BRICK_HEIGHT = 30;
const BRICK_ROWS = 5;
const BRICK_COLS = 10;
const BRICK_GAP = 5;
const BRICK_COLORS = [RED, ORANGE, YELLOW, GREEN, BLUE];

// Game states
const MENU = 0;
const PLAYING = 1;
const GAME_OVER = 2;

// Sound effects (to be loaded)
let paddleHitSound = null;
let brickHitSound = null;
let backgroundMusic = null;

// Game class
class Game {
    constructor() {
        this.canvas = document.getElementById('gameCanvas');
        this.ctx = this.canvas.getContext('2d');
        this.canvas.width = SCREEN_WIDTH;
        this.canvas.height = SCREEN_HEIGHT;
        
        this.state = MENU;
        this.score = 0;
        this.lives = 3;
        
        this.paddle = new Paddle(
            SCREEN_WIDTH / 2 - PADDLE_WIDTH / 2,
            SCREEN_HEIGHT - 50,
            PADDLE_WIDTH,
            PADDLE_HEIGHT,
            WHITE
        );
        
        this.ball = new Ball(
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT - 70,
            BALL_RADIUS,
            WHITE,
            BALL_SPEED_X,
            BALL_SPEED_Y
        );
        
        this.bricks = this.createBricks();
        
        // Set up event listeners
        this.canvas.addEventListener('mousemove', (event) => {
            const rect = this.canvas.getBoundingClientRect();
            const mouseX = event.clientX - rect.left;
            this.paddle.move(mouseX);
        });
        
        this.canvas.addEventListener('click', () => {
            if (this.state === MENU) {
                this.state = PLAYING;
            } else if (this.state === GAME_OVER) {
                this.resetGame();
            }
        });
        
        // Load sounds
        this.loadSounds();
        
        // Start game loop
        this.lastTime = 0;
        window.requestAnimationFrame(this.gameLoop.bind(this));
    }
    
    loadSounds() {
        try {
            // Create AudioContext
            const AudioContext = window.AudioContext || window.webkitAudioContext;
            const audioCtx = new AudioContext();
            
            // Simple paddle hit sound
            paddleHitSound = audioCtx.createOscillator();
            paddleHitSound.type = 'sine';
            paddleHitSound.frequency.setValueAtTime(440, audioCtx.currentTime);
            
            // Simple brick hit sound  
            brickHitSound = audioCtx.createOscillator();
            brickHitSound.type = 'sine';
            brickHitSound.frequency.setValueAtTime(880, audioCtx.currentTime);
            
            // For simplicity, we're not implementing full sound in this version
            // In a complete version, you'd load actual audio files
        } catch (error) {
            console.log("Sound system not available");
        }
    }
    
    createBricks() {
        const bricks = [];
        for (let row = 0; row < BRICK_ROWS; row++) {
            const brickRow = [];
            for (let col = 0; col < BRICK_COLS; col++) {
                const x = col * (BRICK_WIDTH + BRICK_GAP) + BRICK_GAP;
                const y = row * (BRICK_HEIGHT + BRICK_GAP) + BRICK_GAP + 50;
                const brick = {
                    x: x,
                    y: y,
                    color: BRICK_COLORS[row % BRICK_COLORS.length],
                    active: true
                };
                brickRow.push(brick);
            }
            bricks.push(brickRow);
        }
        return bricks;
    }
    
    drawBricks() {
        for (let row = 0; row < this.bricks.length; row++) {
            for (let col = 0; col < this.bricks[row].length; col++) {
                const brick = this.bricks[row][col];
                if (brick.active) {
                    this.ctx.fillStyle = brick.color;
                    this.ctx.fillRect(brick.x, brick.y, BRICK_WIDTH, BRICK_HEIGHT);
                    this.ctx.strokeStyle = WHITE;
                    this.ctx.strokeRect(brick.x, brick.y, BRICK_WIDTH, BRICK_HEIGHT);
                }
            }
        }
    }
    
    drawText(text, x, y, color = WHITE) {
        this.ctx.fillStyle = color;
        this.ctx.font = '36px Arial';
        this.ctx.fillText(text, x, y);
    }
    
    drawGame() {
        this.ctx.fillStyle = BLACK;
        this.ctx.fillRect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT);
        
        // Draw game elements
        this.paddle.draw(this.ctx);
        this.ball.draw(this.ctx);
        this.drawBricks();
        
        // Draw score and lives
        this.drawText(`Score: ${this.score}`, 10, 30);
        this.drawText(`Lives: ${this.lives}`, SCREEN_WIDTH - 150, 30);
    }
    
    drawMenu() {
        this.ctx.fillStyle = BLACK;
        this.ctx.fillRect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT);
        this.drawText("BREAKOUT", SCREEN_WIDTH / 2 - 90, SCREEN_HEIGHT / 2 - 30);
        this.drawText("Click to start", SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 2 + 30);
    }
    
    drawGameOver() {
        this.ctx.fillStyle = BLACK;
        this.ctx.fillRect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT);
        this.drawText("GAME OVER", SCREEN_WIDTH / 2 - 90, SCREEN_HEIGHT / 2 - 30);
        this.drawText(`Final Score: ${this.score}`, SCREEN_WIDTH / 2 - 110, SCREEN_HEIGHT / 2 + 30);
        this.drawText("Click to play again", SCREEN_WIDTH / 2 - 150, SCREEN_HEIGHT / 2 + 90);
    }
    
    checkGameOver() {
        // Check if all bricks are destroyed
        let allDestroyed = true;
        for (let row = 0; row < this.bricks.length; row++) {
            for (let col = 0; col < this.bricks[row].length; col++) {
                if (this.bricks[row][col].active) {
                    allDestroyed = false;
                    break;
                }
            }
        }
        
        if (allDestroyed) {
            this.resetGame();
            this.score += 100; // Bonus for clearing the level
        }
        
        // Check if ball is out of play
        if (!this.ball.inPlay) {
            this.lives--;
            if (this.lives <= 0) {
                this.state = GAME_OVER;
            } else {
                this.ball.reset(this.paddle);
            }
        }
    }
    
    resetGame() {
        this.bricks = this.createBricks();
        this.ball.reset(this.paddle);
        
        if (this.state === GAME_OVER) {
            this.score = 0;
            this.lives = 3;
            this.state = PLAYING;
        }
    }
    
    gameLoop(timestamp) {
        // Calculate delta time
        const deltaTime = timestamp - this.lastTime;
        this.lastTime = timestamp;
        
        // Main game logic
        if (this.state === PLAYING) {
            this.ball.move();
            this.ball.checkCollision(this.paddle, this.bricks, () => { this.score += 10; });
            this.checkGameOver();
            this.drawGame();
        } else if (this.state === MENU) {
            this.drawMenu();
        } else if (this.state === GAME_OVER) {
            this.drawGameOver();
        }
        
        // Continue the game loop
        window.requestAnimationFrame(this.gameLoop.bind(this));
    }
}

class Paddle {
    constructor(x, y, width, height, color) {
        this.x = x;
        this.y = y;
        this.width = width;
        this.height = height;
        this.color = color;
    }
    
    draw(ctx) {
        ctx.fillStyle = this.color;
        ctx.fillRect(this.x, this.y, this.width, this.height);
    }
    
    move(mouseX) {
        this.x = mouseX - this.width / 2;
        if (this.x < 0) {
            this.x = 0;
        }
        if (this.x + this.width > SCREEN_WIDTH) {
            this.x = SCREEN_WIDTH - this.width;
        }
    }
}

class Ball {
    constructor(x, y, radius, color, speedX, speedY) {
        this.x = x;
        this.y = y;
        this.radius = radius;
        this.color = color;
        this.speedX = speedX;
        this.speedY = speedY;
        this.inPlay = true;
    }
    
    draw(ctx) {
        ctx.fillStyle = this.color;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
        ctx.fill();
    }
    
    move() {
        this.x += this.speedX;
        this.y += this.speedY;
        
        // Wall collision
        if (this.x <= this.radius || this.x >= SCREEN_WIDTH - this.radius) {
            this.speedX = -this.speedX;
        }
        if (this.y <= this.radius) {
            this.speedY = -this.speedY;
        }
        
        // Bottom wall (game over)
        if (this.y >= SCREEN_HEIGHT - this.radius) {
            this.inPlay = false;
        }
    }
    
    reset(paddle) {
        this.inPlay = true;
        this.x = paddle.x + paddle.width / 2;
        this.y = paddle.y - this.radius;
        this.speedX = BALL_SPEED_X * (Math.random() > 0.5 ? 1 : -1);
        this.speedY = BALL_SPEED_Y;
    }
    
    checkCollision(paddle, bricks, onBrickHit) {
        // Paddle collision
        if (this.y + this.radius >= paddle.y && 
            this.x >= paddle.x && 
            this.x <= paddle.x + paddle.width &&
            this.y <= paddle.y + PADDLE_HEIGHT) {
            
            this.speedY = -Math.abs(this.speedY); // Always bounce up
            
            // Change x direction based on where the ball hits the paddle
            const relativeX = (this.x - (paddle.x + paddle.width / 2)) / (paddle.width / 2);
            this.speedX = relativeX * 5; // Adjust the multiplier for desired effect
            
            // Play paddle hit sound (not implemented in this version)
        }
        
        // Brick collision
        for (let row = 0; row < bricks.length; row++) {
            for (let col = 0; col < bricks[row].length; col++) {
                const brick = bricks[row][col];
                if (brick.active && this.checkBrickCollision(brick)) {
                    brick.active = false;
                    if (onBrickHit) onBrickHit();
                    return true;
                }
            }
        }
        return false;
    }
    
    checkBrickCollision(brick) {
        // Create a rectangle for the brick
        const brickRect = {
            left: brick.x,
            right: brick.x + BRICK_WIDTH,
            top: brick.y,
            bottom: brick.y + BRICK_HEIGHT
        };
        
        // Calculate the closest point on the rectangle to the center of the circle
        const closestX = Math.max(brickRect.left, Math.min(this.x, brickRect.right));
        const closestY = Math.max(brickRect.top, Math.min(this.y, brickRect.bottom));
        
        // Calculate the distance between the circle's center and this closest point
        const distanceX = this.x - closestX;
        const distanceY = this.y - closestY;
        const distance = Math.sqrt(distanceX * distanceX + distanceY * distanceY);
        
        // If the distance is less than the circle's radius, an intersection occurs
        if (distance <= this.radius) {
            // Determine which side of the brick was hit
            if (Math.abs(this.x - brickRect.left) <= this.radius || 
                Math.abs(this.x - brickRect.right) <= this.radius) {
                this.speedX = -this.speedX;
            } else {
                this.speedY = -this.speedY;
            }
            
            // Play brick hit sound (not implemented in this version)
            return true;
        }
        return false;
    }
}

// Start the game when the window loads
window.onload = function() {
    new Game();
}; 