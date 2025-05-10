import pygame
import sys
import random
import os

# Initialize pygame
pygame.init()
pygame.mixer.init()  # Initialize the mixer for sound

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# Paddle properties
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 20
PADDLE_SPEED = 10

# Ball properties
BALL_RADIUS = 10
BALL_SPEED_X = 4
BALL_SPEED_Y = -4

# Brick properties
BRICK_WIDTH = 80
BRICK_HEIGHT = 30
BRICK_ROWS = 5
BRICK_COLS = 10
BRICK_GAP = 5
BRICK_COLORS = [RED, ORANGE, YELLOW, GREEN, BLUE]

# Game states
MENU = 0
PLAYING = 1
GAME_OVER = 2

# Sound files directory
sound_dir = "sounds"
os.makedirs(sound_dir, exist_ok=True)

# Create sound files if they don't exist yet
def create_default_sound_files():
    # Simple beep sound for paddle hit using pygame
    if not os.path.exists(os.path.join(sound_dir, "paddle_hit.wav")):
        beep_sound = pygame.mixer.Sound(pygame.sndarray.make_sound(
            pygame.sndarray.array([4096 * pygame.math.sin(x / 50.0)
                      for x in range(0, 22050)])).get_raw())
        beep_sound.set_volume(0.3)
        pygame.mixer.Sound.save(beep_sound, os.path.join(sound_dir, "paddle_hit.wav"))
    
    # Simple pop sound for brick hit
    if not os.path.exists(os.path.join(sound_dir, "brick_hit.wav")):
        pop_sound = pygame.mixer.Sound(pygame.sndarray.make_sound(
            pygame.sndarray.array([4096 * pygame.math.sin(x / 30.0) * max(0, 1 - x / 5000)
                      for x in range(0, 10000)])).get_raw())
        pop_sound.set_volume(0.4)
        pygame.mixer.Sound.save(pop_sound, os.path.join(sound_dir, "brick_hit.wav"))
    
    # Create a simple background music
    if not os.path.exists(os.path.join(sound_dir, "background.wav")):
        # Create a simple melody
        duration = 44100 * 20  # 20 seconds
        sample_rate = 44100
        
        # Generate a simple melody based on a scale
        scale = [261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88]  # C major scale
        melody = []
        
        for _ in range(500):  # Create a 20 second melody
            note = random.choice(scale)
            note_duration = random.randint(10000, 30000)  # Random note duration
            melody.extend([int(32767 * 0.2 * pygame.math.sin(2 * pygame.math.pi * note * t / sample_rate)) 
                         for t in range(note_duration)])
        
        # Make sure the melody is long enough
        while len(melody) < duration:
            melody.extend(melody[:duration - len(melody)])
        
        # Trim to exact length
        melody = melody[:duration]
        
        # Convert to NumPy array with correct data type
        import numpy as np
        melody_array = np.array(melody, dtype=np.int16)
        
        # Create pygame sound and save
        bg_music = pygame.mixer.Sound(pygame.sndarray.make_sound(melody_array).get_raw())
        bg_music.set_volume(0.2)
        pygame.mixer.Sound.save(bg_music, os.path.join(sound_dir, "background.wav"))

# Try to create default sound files
try:
    create_default_sound_files()
except:
    print("Could not create default sound files. Please add your own sound files.")

# Load sounds
try:
    PADDLE_HIT_SOUND = pygame.mixer.Sound(os.path.join(sound_dir, "paddle_hit.wav"))
    BRICK_HIT_SOUND = pygame.mixer.Sound(os.path.join(sound_dir, "brick_hit.wav"))
    # Set volume
    PADDLE_HIT_SOUND.set_volume(0.3)
    BRICK_HIT_SOUND.set_volume(0.4)
except:
    print("Could not load sound files. Playing without sound.")
    PADDLE_HIT_SOUND = None
    BRICK_HIT_SOUND = None

class Paddle:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        
    def move(self, mouse_x):
        self.rect.centerx = mouse_x
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

class Ball:
    def __init__(self, x, y, radius, color, speed_x, speed_y):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.in_play = True
        
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        
    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y
        
        # Wall collision
        if self.x <= self.radius or self.x >= SCREEN_WIDTH - self.radius:
            self.speed_x = -self.speed_x
        if self.y <= self.radius:
            self.speed_y = -self.speed_y
            
        # Bottom wall (game over)
        if self.y >= SCREEN_HEIGHT - self.radius:
            self.in_play = False
            
    def reset(self, paddle):
        self.in_play = True
        self.x = paddle.rect.centerx
        self.y = paddle.rect.top - self.radius
        self.speed_x = BALL_SPEED_X * random.choice([-1, 1])
        self.speed_y = BALL_SPEED_Y
        
    def check_collision(self, paddle, bricks):
        # Paddle collision
        if self.y + self.radius >= paddle.rect.top and self.x >= paddle.rect.left and self.x <= paddle.rect.right:
            if self.y <= paddle.rect.top + PADDLE_HEIGHT:
                self.speed_y = -abs(self.speed_y)  # Always bounce up
                # Change x direction based on where the ball hits the paddle
                relative_x = (self.x - paddle.rect.centerx) / (PADDLE_WIDTH / 2)
                self.speed_x = relative_x * 5  # Adjust the multiplier for desired effect
                
                # Play paddle hit sound
                if PADDLE_HIT_SOUND:
                    PADDLE_HIT_SOUND.play()
                
        # Brick collision
        for row in bricks:
            for brick in row:
                if brick and self.check_brick_collision(brick):
                    brick["active"] = False
                    return True
        return False
                    
    def check_brick_collision(self, brick):
        if not brick["active"]:
            return False
            
        brick_rect = pygame.Rect(brick["x"], brick["y"], BRICK_WIDTH, BRICK_HEIGHT)
        
        # Calculate the closest point on the rectangle to the center of the circle
        closest_x = max(brick_rect.left, min(self.x, brick_rect.right))
        closest_y = max(brick_rect.top, min(self.y, brick_rect.bottom))
        
        # Calculate the distance between the circle's center and this closest point
        distance_x = self.x - closest_x
        distance_y = self.y - closest_y
        distance = (distance_x ** 2 + distance_y ** 2) ** 0.5
        
        # If the distance is less than the circle's radius, an intersection occurs
        if distance <= self.radius:
            # Determine which side of the brick was hit
            if abs(self.x - brick_rect.left) <= self.radius or abs(self.x - brick_rect.right) <= self.radius:
                self.speed_x = -self.speed_x
            else:
                self.speed_y = -self.speed_y
                
            # Play brick hit sound
            if BRICK_HIT_SOUND:
                BRICK_HIT_SOUND.play()
                
            return True
        return False

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Breakout Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)
        self.state = MENU
        self.score = 0
        self.lives = 3
        
        # Create paddle
        self.paddle = Paddle(SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2, 
                            SCREEN_HEIGHT - 50, 
                            PADDLE_WIDTH, 
                            PADDLE_HEIGHT, 
                            WHITE)
        
        # Create ball
        self.ball = Ball(SCREEN_WIDTH // 2, 
                        SCREEN_HEIGHT - 70, 
                        BALL_RADIUS, 
                        WHITE, 
                        BALL_SPEED_X, 
                        BALL_SPEED_Y)
        
        # Create bricks
        self.bricks = self.create_bricks()
        
        # Start background music
        self.start_background_music()
        
    def start_background_music(self):
        try:
            pygame.mixer.music.load(os.path.join(sound_dir, "background.wav"))
            pygame.mixer.music.set_volume(0.2)  # Set lower volume for background music
            pygame.mixer.music.play(-1)  # -1 means loop indefinitely
        except:
            print("Could not play background music")
        
    def create_bricks(self):
        bricks = []
        for row in range(BRICK_ROWS):
            brick_row = []
            for col in range(BRICK_COLS):
                x = col * (BRICK_WIDTH + BRICK_GAP) + BRICK_GAP
                y = row * (BRICK_HEIGHT + BRICK_GAP) + BRICK_GAP + 50
                brick = {
                    "x": x,
                    "y": y,
                    "color": BRICK_COLORS[row % len(BRICK_COLORS)],
                    "active": True
                }
                brick_row.append(brick)
            bricks.append(brick_row)
        return bricks
        
    def draw_bricks(self):
        for row in self.bricks:
            for brick in row:
                if brick["active"]:
                    pygame.draw.rect(self.screen, 
                                    brick["color"], 
                                    [brick["x"], brick["y"], BRICK_WIDTH, BRICK_HEIGHT])
                    pygame.draw.rect(self.screen, 
                                    WHITE, 
                                    [brick["x"], brick["y"], BRICK_WIDTH, BRICK_HEIGHT], 
                                    1)
    
    def draw_text(self, text, x, y, color=WHITE):
        text_surface = self.font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))
    
    def draw_game(self):
        self.screen.fill(BLACK)
        
        # Draw game elements
        self.paddle.draw(self.screen)
        self.ball.draw(self.screen)
        self.draw_bricks()
        
        # Draw score and lives
        self.draw_text(f"Score: {self.score}", 10, 10)
        self.draw_text(f"Lives: {self.lives}", SCREEN_WIDTH - 100, 10)
    
    def draw_menu(self):
        self.screen.fill(BLACK)
        self.draw_text("BREAKOUT", SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 - 50)
        self.draw_text("Click to start", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2)
    
    def draw_game_over(self):
        self.screen.fill(BLACK)
        self.draw_text("GAME OVER", SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 - 50)
        self.draw_text(f"Final Score: {self.score}", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2)
        self.draw_text("Click to play again", SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 50)
    
    def check_game_over(self):
        # Check if all bricks are destroyed
        all_destroyed = True
        for row in self.bricks:
            for brick in row:
                if brick["active"]:
                    all_destroyed = False
                    break
        
        if all_destroyed:
            self.reset_game()
            self.score += 100  # Bonus for clearing the level
        
        # Check if ball is out of play
        if not self.ball.in_play:
            self.lives -= 1
            if self.lives <= 0:
                self.state = GAME_OVER
            else:
                self.ball.reset(self.paddle)
    
    def reset_game(self):
        self.bricks = self.create_bricks()
        self.ball.reset(self.paddle)
        if self.state == GAME_OVER:
            self.score = 0
            self.lives = 3
            self.state = PLAYING
    
    def run(self):
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.state == MENU:
                        self.state = PLAYING
                    elif self.state == GAME_OVER:
                        self.reset_game()
            
            # Get mouse position for paddle
            mouse_x, _ = pygame.mouse.get_pos()
            self.paddle.move(mouse_x)
            
            # Main game logic
            if self.state == PLAYING:
                self.ball.move()
                if self.ball.check_collision(self.paddle, self.bricks):
                    self.score += 10
                self.check_game_over()
                self.draw_game()
            elif self.state == MENU:
                self.draw_menu()
            elif self.state == GAME_OVER:
                self.draw_game_over()
            
            pygame.display.flip()
            self.clock.tick(60)
        
        # Stop the music when exiting
        pygame.mixer.music.stop()
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run() 