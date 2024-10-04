import pygame
from str_list import cube_xy
import basic
import player
pygame.init()   #init pygame
game_window = pygame.display.set_mode((1200, 720)) #create game window
imp = pygame.image.load("graphic/map pandemic.png").convert() #set background img location
p1 = pygame.image.load("graphic/pawn_yellow.png")
p1 = pygame.transform.scale(p1, (12,20))
p2 = pygame.image.load("graphic/pawn_red.png")
p2 = pygame.transform.scale(p2, (12,20))
rc = pygame.image.load("graphic/rc.png")
vaccine = pygame.image.load("graphic/vaccine.png")
infection_track_mark  = pygame.image.load("graphic/infection_track_mark.png")
outbreak_track_mark = pygame.image.load("graphic/blood.png")

cube_blue =  pygame.image.load("graphic/blue.png")
cube_violet = pygame.image.load("graphic/violet.png")
cube_red = pygame.image.load("graphic/red.png")
cube_yellow =pygame.image.load("graphic/yellow.png")

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

def print_player():
    player_location = basic.return_player_coordinate()
    if player_location[0][1] == player_location[1][1]:
        game_window.blit(p1, (player_location[0][1] -10, player_location[0][2] - 18))
        game_window.blit(p2, (player_location[1][1] , player_location[1][2] - 18))
    else:
        game_window.blit(p1, (player_location[0][1],player_location[0][2]-18))
        game_window.blit(p2, (player_location[1][1],player_location[1][2]-18))


def print_map():
    game_window.blit(imp, (0, 0))
    data = basic.return_all_city_situation()
    for mem in data:
        l = basic.return_city_coordinate(mem[0])
        if mem[5] == 1:
            game_window.blit(rc, (l[0]-8, l[1]-27))
        print_cube(l[0], l[1],mem[1:5])
    data = basic.return_game_info()
    game_window.blit(infection_track_mark, (48+24*data[0]-14,538))
    for i in range(data[1]+1):
        game_window.blit(outbreak_track_mark,(48 + 23 * i-14, 468))
    for i in range(2,6):
        if data[i] == 1:
            game_window.blit(vaccine,(45+(i-2)*40, 660))

    print_player()
    pygame.display.flip()


def print_action_menu(player_id,action_point):
    print(f"Player {player_id} turn, you have {action_point} action points and this is your current card:")
    player.display(player_id)