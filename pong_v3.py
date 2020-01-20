# Pong version 3
# Implements a game window that contains a circle and two rectangles.
# The circle starts in the centre of the screen and moves around the screen,
# bouncing off the sides of the screen. The ball also bounces off the front
# of the rectangles, but not the back of them.
# Both paddles respond to the player pressing a key that corresponds with
# upwards or downwards movement of the paddle (Q/A keys and P/L keys)

import pygame


# User-defined functions

def main():
   # initialize all pygame modules (some need initialization)
   pygame.init()
   # create a pygame display window
   pygame.display.set_mode((500, 400))
   # set the title of the display window
   pygame.display.set_caption('Pong Version 3')   
   # get the display surface
   w_surface = pygame.display.get_surface() 
   # create a game object
   game = Game(w_surface)
   # start the main game loop by calling the play method on the game object
   game.play() 
   # quit pygame and clean up the pygame window
   pygame.quit() 
   
# User-defined classes

class Game:
   # An object in this class represents a complete game.
   
   def __init__(self, surface):
      # Initialize a Game.
      # - self is the Game to initialize
      # - surface is the display window surface object

      # === objects that are part of every game that we will discuss
      self.surface = surface
      self.bg_color = pygame.Color('black')
      
      self.FPS = 60
      self.game_Clock = pygame.time.Clock()
      self.close_clicked = False
      self.continue_game = True
      
      # === game specific objects
      self.x_offset = 75
      self.paddle1 = Paddle('white', [self.x_offset, (self.surface.get_height()//2)-20, 10, 40], self.surface)
      self.paddle2 = Paddle('white', [self.surface.get_width()-10 - self.x_offset, (self.surface.get_height()//2)-20, 10, 40], self.surface)
      self.ball = Ball('white', 8, [self.surface.get_width()//2, self.surface.get_height()//2], [7, 3], self.paddle1, self.paddle2, self.surface)
      self.p1score = 0
      self.p2score = 0
      
   def play(self):
      
      # Play the game until the player presses the close box.
      # - self is the Game that should be continued or not.

      while not self.close_clicked:  # until player clicks close box
         # play frame
         self.handle_events()
         self.draw()
         if self.continue_game:
            self.update()
            self.decide_continue()
         self.game_Clock.tick(self.FPS) # run at most with FPS Frames Per Second 
         
   def handle_events(self):
      # Handle each user event by changing the game state appropriately.
      # - self is the Game whose events will be handled

      events = pygame.event.get()
      for event in events:
         if event.type == pygame.QUIT:
            self.close_clicked = True
   
   def draw_score(self):
      # Draw the score for both players on the top corners of the window
      font_color = pygame.Color('white')
      font_bg = pygame.Color('black')
      font = pygame.font.SysFont('arial', 50)
      text_p1_score = font.render(str(self.p1score), True, font_color, font_bg)
      text_p2_score = font.render(str(self.p2score), True, font_color, font_bg)
      self.surface.blit(text_p1_score, (0,0))
      self.surface.blit(text_p2_score, (self.surface.get_width() - 50, 0))
      
   def draw(self):
      # Draw all game objects.
      # - self is the Game to draw
      self.surface.fill(self.bg_color) # clear the display surface first
      self.ball.draw()
      self.paddle1.draw()
      self.paddle2.draw()
      self.draw_score()
      pygame.display.update() # make the updated surface appear on the display

   def get_key(self):
      # Determine what key the user pressed, and call the move_paddle method
      # with the according key
      keys = pygame.key.get_pressed()
      if keys[pygame.K_q] and self.paddle1.get_top() > 0:
         self.paddle1.move_paddle('q')
      if keys[pygame.K_a] and self.paddle1.get_top() < (self.surface.get_height() - self.paddle1.get_height()):
         self.paddle1.move_paddle('a')
      if keys[pygame.K_p] and self.paddle2.get_top() > 0:
         self.paddle2.move_paddle('p')
      if keys[pygame.K_l] and self.paddle2.get_top() < (self.surface.get_height() - self.paddle2.get_height()):
         self.paddle2.move_paddle('l')

   def update(self):
      # Update the game objects for the next frame.
      # - self is the Game to update
      self.ball.check_collision()
      hit = self.ball.move()
      if hit == 1:
         self.p1score += 1
      elif hit == 2:
         self.p2score += 1
      self.get_key()

   def decide_continue(self):
      # Check and remember if the game should continue
      # - self is the Game to check
      if self.p1score > 10 or self.p2score > 10:
         self.continue_game = False
         

class Paddle:
   # objects of this class represent a paddle the users can control
   
   def __init__(self, paddle_color, paddle_dimensions, surface):
      # Initialize a padde
      # - self is the paddle to initialize
      # - color is the color of the paddle
      # - dimensions is a list of dimensions for the rectangular paddle
      # - surface is the window surface
      
      self.color = pygame.Color(paddle_color)
      self.surface = surface
      self.x_offset = paddle_dimensions[0]      
      self.top = paddle_dimensions[1]
      self.width = paddle_dimensions[2]
      self.height = paddle_dimensions[3]        
      
   def move_paddle(self, key):
      #moves the paddle depending on the key pressed
         if key == 'q' or key == 'p':
            self.top -= 10
         elif key == 'a' or key == 'l':
            self.top += 10

   def get_height(self):
      #returns the current height of the paddle
      return self.height

   def get_top(self):
      #returns the top coordinate of the paddle
      return self.top

   def draw(self):
      # draw the paddle as a rectangle on the screen
      self.rectangle = pygame.Rect(self.x_offset, self.top, self.width, self.height)
      pygame.draw.rect(self.surface, self.color, self.rectangle)


class Ball:
   # An object in this class represents a Ball that moves 
   
   def __init__(self, ball_color, ball_radius, ball_center, ball_velocity, paddle1, paddle2, surface):
      # Initialize a Ball.
      # - self is the Ball to initialize
      # - color is the pygame.Color of the ball
      # - center is a list containing the x and y int
      #   coords of the center of the ball
      # - radius is the int pixel radius of the ball
      # - velocity is a list containing the x and y components
      # - surface is the window's pygame.Surface object
      # - paddle1 is the left paddle
      # - paddle2 is the right paddle

      self.color = pygame.Color(ball_color)
      self.radius = ball_radius
      self.center = ball_center
      self.velocity = ball_velocity
      self.surface = surface
      self.paddle1 = paddle1
      self.paddle2 = paddle2
   
   def move(self):
      # Change the location of the Ball by adding the corresponding 
      # speed values to the x and y coordinate of its center
      # - self is the Ball
      window_size = self.surface.get_size()
      
      for i in range(len(self.center)):
         
         self.center[i] += self.velocity[i]
         # if the centre position is less than the radius, it will be off screen
         if self.center[i] < self.radius:
            self.velocity[i] = -self.velocity[i]
            # if the ball bounces off the left side of the screen, give a point to p2
            if i == 0:
               return 2
         # if the centre + radius is greater than height/width, it will be off screen
         elif (self.center[i] + self.radius) > window_size[i]:
            self.velocity[i] = -self.velocity[i]
            # if the ball bounces off the right side of the screen, give a point to p1
            if i == 0:
               return 1
               
   def check_collision(self):
      # check if the ball is heading towards the front or back of the paddles
      if (self.center[0] < 250 and self.velocity[0] < 0) or (self.center[0] > 250 and self.velocity[0] > 0):
         # if the ball collides with either paddle, reverse the velocity of the ball
         if self.paddle1.rectangle.collidepoint(self.center[0], self.center[1]):
            self.velocity[0] = -self.velocity[0]
         if self.paddle2.rectangle.collidepoint(self.center[0], self.center[1]):
            self.velocity[0] = -self.velocity[0]
   
   def draw(self):
      # Draw the ball on the surface
      # - self is the Ball
      pygame.draw.circle(self.surface, self.color, self.center, self.radius)
      


main()
