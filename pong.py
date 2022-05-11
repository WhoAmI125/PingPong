# This is ping pong game using pygame
# The three different class sets up the game
# Bring the modules I need to use
from pygame.locals import*
import pygame
import random

# Where the game call would happen
def main():
    # Initialize all pygame modules (some need initialization)
    pygame.init()
    # Create a pygame display window
    pygame.display.set_mode((500, 400))
    # Set the title of the display window
    pygame.display.set_caption("Pong")  # Title of the game
    game_screen = pygame.display.get_surface()
    game = Game(game_screen)
    game.play() 
    pygame.quit() # Quit the game

# This is where it sets up the condition of the game 
class Game:
    # An object in this class represents a complete game.
    # Set up the basic game condition, the size of the screen and aspects object
    def __init__(self, screen):  
        # self is basic, and screen is to set up the background
        # initialize a game
        self.screen = screen
        self.bg_color = pygame.Color('black')  # Set the background
        
        # FPS Clocking and game conditions
        self.FPS = 60
        self.game_Clock = pygame.time.Clock()
        self.close_clicked = False
        self.continue_game = True        
        
        # Set the ball
        self.pp_ball = PP_Ball("white", 8, [200, 200], [6, 2], self.screen)
        
        # Set the count
        self.score_1 = 0
        self.score_2 = 0
        
        # Set up the paddle
        self.paddle_1 = Paddle(30, 150, 10, 60, self.screen)  
        self.paddle_2 = Paddle(450, 150, 10, 60, self.screen)
   
    # Play the game until the player presses the close box.    
    def play(self):
        # self is the Game that should be continued or not.
        while not self.close_clicked:  # until player clicks close box
            # play frame
            self.handle_events()  # set up how to end the game
            self.draw()  # draw up the object
            if self.continue_game == True:
                self.update()  # call the update of position
                self.decide_continue()  # call when the game is stopped
            self.game_Clock.tick(self.FPS) # Shows the Frame per Second  
    
    # Handle each user event by changing the game state appropriately.     
    def handle_events(self):
        # self is the Game whose events will be handled
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.close_clicked = True  # Change the game condition to end the game          
    
    # Draw all game objects.            
    def draw(self):
        # self is the Game to draw     
        self.screen.fill(self.bg_color) # clean up the display
        self.pp_ball.draw()
        self.draw_score_1()
        self.draw_score_2()
        self.update_score()
        pygame.draw.rect(self.screen, pygame.Color("white"), self.paddle_1)
        pygame.draw.rect(self.screen, pygame.Color("white"), self.paddle_2)
        pygame.display.update()
        
    # Update all game objects    
    def update(self):
        # self is the game to update
        self.pp_ball.move()
        self.pp_ball.collide_detection(self.paddle_1, self.paddle_2)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            self.paddle_1.moveUp(5)
        if keys[pygame.K_a]:
            self.paddle_1.moveDown(5)
        if keys[pygame.K_UP]:
            self.paddle_2.moveUp(5)
        if keys[pygame.K_DOWN]:
            self.paddle_2.moveDown(5)        
    
    # Check and remember if the game should continue            
    def decide_continue(self):
        # self is the Game to check
        if self.score_1 == 11 or self.score_2 == 11: 
            self.continue_game = False 
            
    # Draw the score for the left side
    def draw_score_1(self):
        # self is to draw up the score and set the position
        text_string_1 = str(self.score_1)  # rendering text need to be string
        text_color = pygame.Color("white")        
        text_font = pygame.font.SysFont("Times New Roman", 72, 60)
        text_image = text_font.render(text_string_1, True, text_color)
        text_pos = (0, -10)
        self.screen.blit(text_image, text_pos)
    
    # Draw the score for the right side    
    def draw_score_2(self):
        # self is to draw up the score and set the position
        text_string_2 = str(self.score_2)  # rendering text need to be string
        text_color = pygame.Color("white")        
        text_font = pygame.font.SysFont("Times New Roman", 72, 60)
        text_image = text_font.render(text_string_2, True, text_color)
        text_pos = (455, -10)
        if self.score_2 > 9:  # this is needed since the position goes outside
            text_pos = (440, -10)
        self.screen.blit(text_image, text_pos)    
    
    # Update the score as hit the border
    def update_score(self):
        # self is update the score when the ball hits left or right side
        if self.pp_ball.center[0] < self.pp_ball.radius:
            self.score_2 += 1
        if self.pp_ball.center[0] + self.pp_ball.radius > self.screen.get_width():
            self.score_1 += 1

# This is where it sets up the ball   
class PP_Ball:
    # Initialize a Ball
    def __init__(self, pp_ball_color, pp_ball_radius, pp_ball_center, pp_ball_velocity, screen):
        # - self is the Ball to initialize
        # - color is the pygame.Color of the dot
        # - center is a list containing the x and y int
        #   coords of the center of the dot
        # - radius is the int pixel radius of the dot
        # - velocity is a list containing the x and y components
        # - screen is the window's pygame.Surface object
    
        self.color = pygame.Color(pp_ball_color)
        self.radius = pp_ball_radius
        self.center = pp_ball_center
        self.velocity = pp_ball_velocity
        self.screen = screen
    
    # Allow to move    
    def move(self):
        # Change the location of the Ball by adding the corresponding 
        # speed values to the x and y coordinate of its center
        # - self is the Ball
        size = self.screen.get_size()
        for i in range(0,2):
            self.center[i] = (self.center[i] + self.velocity[i])
            if self.center[i] < self.radius or self.center[i] + self.radius > size[i]:
                self.velocity[i] = -self.velocity[i]
    
                # Bounce the ball when it hits the paddle            
    def collide_detection(self, paddle_1, paddle_2):
        # self is the ball
        # paddle_1 and paddle_2 are the paddles in each side
        if paddle_1.rect.collidepoint(self.center) and self.velocity[0] < 0:  # When the ball goes inside the paddle
            self.velocity[0] = - self.velocity[0]
        if paddle_2.rect.collidepoint(self.center) and self.velocity[0] > 0:
            self.velocity[0] = - self.velocity[0]
    
    # Draw the pp_ball on the screen            
    def draw(self):
        # Dself is the ball
        pygame.draw.circle(self.screen, self.color, self.center, self.radius)    

# Define and set up the class for paddle         
class Paddle:
    # Initialize the paddle
    def __init__(self, x, y, width, height, screen):
        # self is the paddle to initialize
        # x and y is the position of the paddle
        # width and height is the size of the paddle
        # - screen is the window's pygame.Surface object
        self.rect = pygame.Rect(x, y, width, height)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen = screen
    
    # Let the paddle move up    
    def moveUp(self, square):
        # self is the paddle and pixels square of the paddle that moves up
        self.rect.y -= square
        if self.rect.y < 0:
            self.rect.y = 0
            
    # Let the paddle move up
    def moveDown(self, square):
        # self is the paddle and pixels square of the paddle that moves down
        self.rect.y += square
        if self.rect.y > 400:
            self.rect.y = 400
        pos = 680 - self.rect.y  # This is to set limit of y when the paddle moves down
        if self.rect.y > pos:
            self.rect.y = pos

# Call main fuction            
main()