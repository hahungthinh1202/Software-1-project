import pygame
import queue
import threading
import color
import action
import basic
import infection
import player


quit_game = False
(blue, violet, red, yellow) = (1,2,3,4)
class ParallelThread(threading.Thread):
  def run(self):
    while not quit_game:
      command = input()
      commands.put(command)

def print_cube(x,y,amount,colour):

    if amount == 1:
        game_window.blit(virus_graphic[colour], (x, y))
    elif amount == 2:
        game_window.blit(virus_graphic[colour], (x, y))
        game_window.blit(virus_graphic[colour], (x-9, y+5))
    elif amount == 3:
        game_window.blit(virus_graphic[colour], (x, y))
        game_window.blit(virus_graphic[colour], (x-9, y+5))
        game_window.blit(virus_graphic[colour], (x+9, y+5))

def print_player():
    player_location = basic.return_player_coordinate()
    if player_location[0][1] == player_location[1][1]:
        game_window.blit(p1, (player_location[0][1] -10, player_location[0][2] - 25))
        game_window.blit(p2, (player_location[1][1] , player_location[1][2] - 25))
    else:
        game_window.blit(p1, (player_location[0][1]-5,player_location[0][2]-25))
        game_window.blit(p2, (player_location[1][1]-5,player_location[1][2]-25))


def print_map():
    data = basic.return_all_city_situation()
    for mem in data:
        if sum(mem[1:5])<4:
            l = basic.return_city_coordinate(mem[0])
            print_cube(l[0], l[1], mem[blue], 'blue')
            print_cube(l[0], l[1], mem[violet], 'violet')
            print_cube(l[0], l[1], mem[red], 'red')
            print_cube(l[0], l[1], mem[yellow], 'yellow')
    data = basic.return_game_info()
    pygame.draw.circle(game_window, color.brown,(48+24*data[0],550), 9)
    pygame.draw.circle(game_window, color.orange, (48 + 24 * data[1], 480), 9)

def print_action_menu(player_id,action_point):
    print(f"Player {player_id} turn, you have {action_point} action points and this is your current knowledge:")
    player.display(player_id)
    print("Available action: move, treat, cure, build.")

pygame.init()   #init pygame
game_window = pygame.display.set_mode((1200, 720)) #create game window
imp = pygame.image.load("graphic/map pandemic.png").convert() #set background img location
p1 = pygame.image.load("graphic/pawn_yellow.png")
p2 = pygame.image.load("graphic/pawn_red.png")
virus_graphic = {
    'blue' : pygame.image.load("graphic/blue.png"),
    'violet' : pygame.image.load("graphic/violet.png"),
    'red' : pygame.image.load("graphic/red.png"),
    'yellow' : pygame.image.load("graphic/yellow.png")
}

game_window.blit(imp, (0, 0),)


commands = queue.Queue()
instance = ParallelThread()
instance.start()

basic.game_init(6,2)
command_list = ['move','treat','cure','build']
disease_list = ['blue','violet','red','yellow']

(main_menu, action_menu, action_detail, action_execute, check) = \
('main_menu','action_menu','action_detail','action_execute','check')
state = action_menu
data_list = []
city_list = []
current_player = 1
action_point  = 4
last_command = ''

game_window.blit(imp, (0, 0))

while not quit_game:
    try:
        command = commands.get(False)
    except queue.Empty:
        command = None

    if state == action_menu:
        print_action_menu(current_player, action_point)
        state = action_detail

    elif state == action_detail and command is not None:
        last_command = command
        state = action_execute
        if command == 'move':
            data_list = action.move_info(current_player)
        elif command == 'treat':
            data_list = action.treat_info(current_player)
            if not data_list:
                state = action_menu
        elif command == 'cure':
            print("cure")
        elif command == 'build':
            print("build")
        else:
            state = action_detail
            print("syntax error")
    elif state == action_execute and command is not None:
        print("This is ", state, " state")
        state = check
        if last_command == 'move':
            destination_id = basic.city_name_to_id(command)
            if not destination_id:
                print("syntax error at choosing city name")
                state = action_execute
            elif destination_id in data_list['drive']:
                print("run move_execute action")
                action.move_execute(current_player, destination_id)
            elif destination_id in data_list['fly']:
                player.discard(current_player, destination_id)
                action.move_execute(current_player, destination_id)
                print("fly to", command)
            elif data_list['jet'][0]:
                action.move_execute(current_player, destination_id)
                player.discard(current_player, data_list['jet'])
                print("jet to", command)
            elif destination_id in data_list['rc']:
                print("rc")
            else:
                state = action_execute
                print("You can not go to", command,"Please choose again")

        elif last_command == 'treat':
            if command in disease_list:
                action.treat_execute(current_player, command, data_list[disease_list.index(command) + 1])
                state = check
            else:
                print("Did not recognise command")
                state = action_execute
        elif last_command == 'cure':
            print("execute cure")
        elif last_command == 'build':
            print("execute build")

    elif state == check:
        action_point = action_point - 1
        if action_point == 0:
            player.draw(current_player)
            player.draw(current_player)
            current_player = 1 + current_player % 2
            action_point = 4
            infection.infect()

        basic.reset_outbreak_flag()
        basic.check_win()
        state = action_menu


    game_window.blit(imp, (0, 0))
    print_player()
    print_map()


    pygame.display.flip()
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            print("pres any key to quit")
            quit_game = True