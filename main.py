import pygame
import queue
import threading

import action
import basic

X = 1200
Y = 720

pygame.init()
game_window = pygame.display.set_mode((X, Y))
pygame.display.set_caption('image')
red = pygame.Color(255, 105, 97)
black  = pygame.Color(0, 0, 0)
yellow = pygame.Color(255, 255, 0)
blue = pygame.Color(0, 0, 255)
imp = pygame.image.load("C:\\Users\\thinh\\OneDrive\\Desktop\\2913127.png").convert()
game_window.blit(imp, (0, 0))

def print_cube(x,y,amount,color):
    if amount == 1:
        pygame.draw.rect(game_window, color,(x,y,10,10))
    elif amount == 2:
        pygame.draw.rect(game_window, color,(x-7,y,10,10))
        pygame.draw.rect(game_window, color,(x+7,y,10,10))
    elif amount == 3:
        pygame.draw.rect(game_window, color,(x-7,y-7,10,10))
        pygame.draw.rect(game_window, color,(x,  y+7,10,10))
        pygame.draw.rect(game_window, color,(x+7,y-7,10,10))

def print_player(player_id):
    player_location = basic.return_player_location(player_id)
    pygame.draw.rect(game_window, red, (player_location[0],player_location[1],10,10))

quit_game = False
commands = queue.Queue()

class Input(threading.Thread):
  def run(self):
    while not quit_game:
      command = input()
      commands.put(command)
i = Input()
i.start()

while not quit_game:
    try:
        command = commands.get(False)
    except queue.Empty:
        command = None

    if command in ['1','2','3','4']:
        print(command)
        action.move_execute(1, int(command))
        game_window.blit(imp, (0, 0))
        print_player(1)
    if command == 'test':
        print(basic.return_player_location(1))

    pygame.display.flip()

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            print("pres any key to quit")
            quit_game = True

i.join()