import pygame
from str_list import cube_xy
import basic
import player

# This module is used to graphically display the game. Basically, get information from database and display.
# Those functions are created temporary for fast checking the working of the game.
# Instead of checking the database table, I can check the map instead.
# Therefore, functions are very limited in used and serve in a very specific way.

# init pygame and create game window size of 1200x720. This game window will be use to display image on.
pygame.init()
game_window = pygame.display.set_mode((1200, 720))

# Loading a lot of image
default_background  = pygame.image.load("graphic/map pandemic.png").convert()
player_1_pawn       = pygame.image.load("graphic/pawn_yellow.png")
player_2_pawn       = pygame.image.load("graphic/pawn_red.png")
research_center     = pygame.image.load("graphic/rc.png")
vaccine_mark        = pygame.image.load("graphic/vaccine.png")
infection_mark      = pygame.image.load("graphic/infection_track_mark.png")
outbreak_mark       = pygame.image.load("graphic/blood.png")
menu_background     = pygame.image.load("graphic/main_menu.png")
win_background      = pygame.image.load("graphic/win.png")
lose_background     = pygame.image.load("graphic/lose.png")
cube_blue           = pygame.image.load("graphic/blue.png")
cube_violet         = pygame.image.load("graphic/violet.png")
cube_red            = pygame.image.load("graphic/red.png")
cube_yellow         = pygame.image.load("graphic/yellow.png")

# Sometimes the image is bigger or smaller than needed, I simply resize it
player_1_pawn = pygame.transform.scale(player_1_pawn, (12,20))
player_2_pawn = pygame.transform.scale(player_2_pawn, (12,20))

# Accept the cube dictionary and first blit all the cube.
# Exactly co-ordinate is calculate base on the city location and pre-determined deviation cube_xy list in str_list module
def print_cube(x,y,cube):
    l_i = 0
    for i in range(cube[0]):
        game_window.blit(cube_blue,(x+cube_xy[l_i][0],y+cube_xy[l_i][1]))
        l_i+=1
    for i in range(cube[1]):
        game_window.blit(cube_violet, (x + cube_xy[l_i][0], y + cube_xy[l_i][1]))
        l_i += 1
    for i in range(cube[2]):
        game_window.blit(cube_red,(x+cube_xy[l_i][0],y+cube_xy[l_i][1]))
        l_i+=1
    for i in range(cube[3]):
        game_window.blit(cube_yellow, (x + cube_xy[l_i][0], y + cube_xy[l_i][1]))
        l_i += 1

# Print the player pawn in the map, if both players are in the same location, adjust the x co-ordinate so
# the two pawns sit next to each other.
def print_player():
    player_location = basic.return_player_coordinate()
    if player_location[0][1] == player_location[1][1]:
        game_window.blit(player_1_pawn, (player_location[0][1] -10, player_location[0][2] - 18))
        game_window.blit(player_2_pawn, (player_location[1][1] , player_location[1][2] - 18))
    else:
        game_window.blit(player_1_pawn, (player_location[0][1],player_location[0][2]-18))
        game_window.blit(player_2_pawn, (player_location[1][1],player_location[1][2]-18))

# Print everything in the map:
# 1. Blit the background
# 2. Get information of all the city that have something to print and blit their virus cube and research center.
# 3. Get information about game track (virus, outbreak, infection) and also blit the the mark in suitable location.
# 4. Blit the player pawn.
# 5. Finally display all blit image into the game window.
def print_map():
    game_window.blit(default_background, (0, 0))
    data = basic.return_all_city_situation()
    for mem in data:
        l = basic.return_city_coordinate(mem[0])
        if mem[5] == 1:
            game_window.blit(research_center, (l[0]-8, l[1]-27))
        print_cube(l[0], l[1],mem[1:5])
    data = basic.return_game_info()
    game_window.blit(infection_mark, (48+24*data[0]-14,538))
    for i in range(data[1]):
        game_window.blit(outbreak_mark,(48 + 23 * i-14, 468))
    for i in range(2,6):
        if data[i] == 1:
            game_window.blit(vaccine_mark,(45+(i-2)*40, 660))
    print_player()
    pygame.display.flip()



def print_action_menu(player_id,action_point):
    print(f"Player {player_id} turn, you have {action_point} action points and this is your current card:")
    player.display(player_id)

def print_main_menu(x,y):
    game_window.blit(menu_background, (0,0))
    game_window.blit(outbreak_mark, (x-15,y-21))
    pygame.display.flip()

def print_endgame(wl):
    if wl == 'lose':
        game_window.blit(lose_background, (0,0))
    elif wl == 'win':
        game_window.blit(win_background, (0,0))
    pygame.display.flip()
