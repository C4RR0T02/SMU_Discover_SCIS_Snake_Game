from tkinter import *
import random

# These are the configurations for our application
GAME_SPEED = 150
APP_WIDTH = 480
APP_HEIGHT = 480
BACKGROUND_COLOR = "#000000"
FOOD_COLOR = "#FF0000"
SNAKE_COLOR = "#00FF00"

# This is a given Class
# This class will be used to represent each cell of the game grid
# DO NOT edit this class
class Coordinate:
  def __init__(self, x, y):
    self.x = x
    self.y = y
    
  def is_within_board(self):
    return -1 < self.x < 15 and -1 < self.y < 15
    
  def __eq__(self, other):
    return self.x == other.x and self.y == other.y


class Snake:
  def __init__(self):
    self.direction = 'RIGHT'
    self.body = [Coordinate(7, 7),
                 Coordinate(6, 7),
                 Coordinate(5, 7)]
    
  def move(self):
    '''
    EXERCISE 1:
    For each step of the game, the Snake will move forward by 1 cell
    in the direction it is facing.
    Fill in the code below
    '''
    current_head = self.body[0]
    if self.direction == 'UP':
      new_head = Coordinate(current_head.x, current_head.y - 1)
    elif self.direction == 'DOWN':
      new_head = Coordinate(current_head.x, current_head.y + 1)
    elif self.direction == 'LEFT':
      new_head = Coordinate(current_head.x - 1, current_head.y)
    elif self.direction == 'RIGHT':
      new_head = Coordinate(current_head.x + 1, current_head.y)
    self.body.pop(-1)
    self.body.insert(0, new_head)
    pass

  def is_alive(self):
    '''
    EXERCISE 2:
    In each step, after moving, we need to determine if the Snake is
    still alive, or if it has eaten itself.
    Fill in the code below
    '''
    current_head = self.body[0]
    if not current_head.is_within_board():
      return False
    if self.body[0] in self.body[1:]:
      return False
    return True

  def has_eaten(self, food):
    '''
    EXERCISE 3:
    In each step, after moving, we need to determine if the Snake has
    eaten the randomly generated Food.
    Increase the length of the snake body by 1 if food is eaten.
    Fill in the code below
    '''
    if self.body[0] == food.pos:
      self.body.append(self.body[-1])
      return True
    return False
    
  def render(self, game):
    for coord in self.body:
      game.canvas.create_rectangle(coord.x*32, coord.y*32, coord.x*32+32, coord.y*32+32, fill=SNAKE_COLOR)

class Food:
  def __init__(self, snake):
    self.pos = None
    self.generate_food(snake)
    
  def generate_food(self, snake):
    '''
    Exercise 4:
    Randomly generate the position of the food
    Assign the attribute pos to the newly generated position
    '''
    valid_food_position = False
    while valid_food_position == False:
      random_x = random.randint(0, 14)
      random_y = random.randint(0, 14)
      if Coordinate(random_x, random_y) not in snake.body:
        valid_food_position = True
    self.pos = Coordinate(random_x, random_y)

  def render(self, game):
    game.canvas.create_oval(self.pos.x*32, self.pos.y*32, self.pos.x*32+32, self.pos.y*32+32, fill=FOOD_COLOR)


'''
This class is used to start and render the game
DO NOT edit this class
'''
class Game:
  def __init__(self):
    # This segment will be used to run the actual app
    self.window = Tk()
    self.window.title("Snake SCIS")
    self.window.resizable(False, False)

    # Create the score board
    self.game_over = False
    self.score = 0
    self.score_label = Label(self.window, text=f"Score: {self.score}", font=('courier new', 40))
    self.score_label.pack()

    # Create the main canvas in which the game will be rendered
    self.canvas = Canvas(self.window, bg=BACKGROUND_COLOR, height=APP_HEIGHT, width=APP_WIDTH)
    self.canvas.pack()
    
    # Initialise Food and Snake
    self.snake = Snake()
    self.food = Food(self.snake)
    
    # Bind keyboard events to canvas
    self.window.bind('<KeyPress>', self.on_key_press)
    
    # Start the game loop
    self.start_game_loop()
    self.window.mainloop()
    
  def on_key_press(self, event):
    '''
    Bonus Exercise:
    Edit this such that you cannot turn back
    180 degrees and eat yourself
    '''
    if event.keysym == 'w' and self.snake.direction != 'DOWN':
      self.snake.direction = 'UP'
    elif event.keysym == 's'and self.snake.direction != 'UP':
      self.snake.direction = 'DOWN'
    elif event.keysym == 'a' and self.snake.direction != 'RIGHT':
      self.snake.direction = 'LEFT'
    elif event.keysym == 'd' and self.snake.direction != 'LEFT':
      self.snake.direction = 'RIGHT'
    elif event.keysym == 'q':
      exit(0)
    elif self.game_over and event.keysym == 'space':
      self.game_over = False
      self.score = 0
      self.snake = Snake()
      self.food = Food()

  def start_game_loop(self):
    # Render the frame
    self.render()
    
    # Move the snake
    self.snake.move()

    # Check if snake has eaten the food
    if self.snake.has_eaten(self.food):
      self.food.generate_food(self.snake)
      self.score += 1

    # Check if snake is still alive
    if not self.snake.is_alive():
      self.game_over = True
    
    # Continue game loop
    self.window.after(GAME_SPEED, self.start_game_loop)

  def render(self):
    self.canvas.delete('all')
    if self.game_over:
      self.canvas.create_text(
        self.canvas.winfo_width()/2,
        self.canvas.winfo_height()/2,
        font=('courier new', 50),
        text="Game Over",
        fill='red'
      )
      self.canvas.create_text(
        self.canvas.winfo_width()/2,
        self.canvas.winfo_height()/2 + 50,
        font=('courier new', 10),
        text="Press <SPACE> to play again",
        fill='white'
      )
      self.canvas.create_text(
        self.canvas.winfo_width()/2,
        self.canvas.winfo_height()/2 + 70,
        font=('courier new', 10),
        text="Press <Q> to quit",
        fill='white'
      )
    else:
      self.snake.render(self)
      self.food.render(self)
      self.score_label.config(text=f"Score: {self.score}")

game = Game()
