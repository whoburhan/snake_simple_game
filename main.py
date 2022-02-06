import pygame
from pygame.locals import *
import time
import random

SIZE = 40


class Apple:
    def __init__(self, parent_screen):
        self.image = pygame.image.load('Resources/apple.jpg').convert()
        self.parent_screen = parent_screen
        self.x = SIZE * 3
        self.y = SIZE * 3

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(1, 24) * SIZE
        self.y = random.randint(1, 19) * SIZE


class Snake:
    def __init__(self, parent_screen, length):

        self.parent_screen = parent_screen
        # This is how you load an image in pygame
        self.block = pygame.image.load("Resources/block.jpg").convert()
        self.direction = 'down'

        self.length = length
        self.x = [SIZE] * length  # postion of the image on x axis
        self.y = [SIZE] * length  # postion of the image on y axis

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def draw(self):
        for i in range(self.length):
            # Blit function allows you to draw on the screen
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()

    def walk(self):
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]
        if self.direction == "left":
            self.x[0] -= SIZE
        if self.direction == "right":
            self.x[0] += SIZE
        if self.direction == "up":
            self.y[0] -= SIZE
        if self.direction == "down":
            self.y[0] += SIZE

        self.draw()


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.play_background_music()
        # this is how you make a display in pygame
        self.surface = pygame.display.set_mode((1000, 800))
        self.surface.fill((92, 25, 84))
        self.snake = Snake(self.surface, 1)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False

    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()
        # logic of snake colliding with apple
        if self.is_collision( self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y ):
            sound = pygame.mixer.Sound('Resources/ding.mp3')
            pygame.mixer.Sound.play(sound)
            self.snake.increase_length()
            self.apple.move()

        # snake collides with itself
        for i in range( 3, self.snake.length ):
            if self.is_collision( self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i] ):
                sound = pygame.mixer.Sound( 'Resources/crash.mp3' )
                pygame.mixer.Sound.play( sound )
                raise "Game over"

    def show_game_over(self):
        self.render_background()
        font = pygame.font.SysFont( 'arial', 30 )
        line1 = font.render( f"Game is over! Your score is {self.snake.length}", True, (200, 200, 200) )
        self.surface.blit( line1, (200, 300) )
        line2 = font.render( "To play the game again press enter. To exit press escape!", True, (200, 200, 200) )
        self.surface.blit( line2, (200, 350) )
        pygame.display.flip()

        pygame.mixer.music.pause()

    def display_score(self):
        font = pygame.font.SysFont( "arial", 30 )
        score = font.render( f"Score: {self.snake.length}", True, (200, 200, 200) )
        self.surface.blit( score, (800, 10) )
    def reset(self):
        self.snake = Snake( self.surface, 1 )
        self.apple = Apple( self.surface )
    def play_background_music(self):
        pygame.mixer.music.load('Resources/bg_music_1.mp3')
        pygame.mixer.music.play()
    def render_background(self):
        bg = pygame.image.load("Resources/background.jpg")
        self.surface.blit(bg, (0,0))

    def run(self):
        running = True
        pause = False
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False
                    if not pause:
                        if event.key == K_UP:
                            self.snake.move_up()
                        if event.key == K_DOWN:
                            self.snake.move_down()
                        if event.key == K_LEFT:
                            self.snake.move_left()
                        if event.key == K_RIGHT:
                            self.snake.move_right()
                elif event.type == QUIT:
                    running = False
            try:
                if not pause:
                    self.play()
            except Exception:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep( 0.3 )


if __name__ == "__main__":
    game = Game()
    game.run()
