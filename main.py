import pygame
import queue
import threading
import color
import action
import basic
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
        pygame.draw.rect(game_window, colour,(x,y,10,10))
    elif amount == 2:
        pygame.draw.rect(game_window, colour,(x-7,y,10,10))
        pygame.draw.rect(game_window, colour,(x+7,y,10,10))
    elif amount == 3:
        pygame.draw.rect(game_window, colour,(x-7,y-7,10,10))
        pygame.draw.rect(game_window, colour,(x,  y+7,10,10))
        pygame.draw.rect(game_window, colour,(x+7,y-7,10,10))

def print_player():
    player_location = basic.return_player_location()
    if player_location[0][1] == player_location[1][1]:
        game_window.blit(p1, (player_location[0][1] -10, player_location[0][2] - 25))
        game_window.blit(p2, (player_location[1][1] , player_location[1][2] - 25))
    else:
        game_window.blit(p1, (player_location[0][1]-5,player_location[0][2]-25))
        game_window.blit(p2, (player_location[1][1]-5,player_location[1][2]-25))


def print_city():
    data = basic.get_map_data()
    for mem in data:
        if sum(mem[1:5])<4:
            l = basic.return_city_location(mem[0])
            print_cube(l[0], l[1], mem[blue], color.blue)
            print_cube(l[0], l[1], mem[violet], color.violet)
            print_cube(l[0], l[1], mem[red], color.red)
            print_cube(l[0], l[1], mem[yellow], color.orange)



pygame.init()   #init pygame
game_window = pygame.display.set_mode((1200, 720)) #create game window
imp = pygame.image.load("C:\\Users\\thinh\\OneDrive\\Desktop\\map_pandemic.png").convert() #set background img location
p1 = pygame.image.load("C:\\Users\\thinh\\OneDrive\\Desktop\\pawn_yellow.png")
p2 = pygame.image.load("C:\\Users\\thinh\\OneDrive\\Desktop\\pawn_red.png")
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
player_id = 1
action_point  = 400
last_command = ''

game_window.blit(imp, (0, 0))

while not quit_game:
    try:
        command = commands.get(False)
    except queue.Empty:
        command = None

    if state == action_menu:
        print("This is ", state," state")
        print(f'this is player {player_id} turn, you have {action_point} action left')
        print('please choose: move, treat, cure, build.')
        state = action_detail

    elif state == action_detail and command is not None:
        print("This is ", state, " state")
        last_command = command
        state = action_execute
        if command == 'move':
            data_list = action.move_info(player_id)
        elif command == 'treat':
            data_list = action.treat_info(player_id)
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
                action.move_execute(player_id, destination_id)
            elif destination_id in data_list['fly']:
                player.discard(player_id,destination_id)
                action.move_execute(player_id, destination_id)
                print("fly to", command)
            elif data_list['jet'][0]:
                action.move_execute(player_id, destination_id)
                player.discard(player_id, data_list['jet'])
                print("jet to", command)
            elif destination_id in data_list['rc']:
                print("rc")
            else:
                state = action_execute
                print("You can not go to", command,"Please choose again")

        elif last_command == 'treat':
            if command in disease_list:
                action.treat_execute(player_id,command ,data_list[disease_list.index(command)+1])
                state = check
            else:
                print("Did not recognise command")
                state = action_execute
        elif last_command == 'cure':
            print("execute cure")
        elif last_command == 'build':
            print("execute build")

    elif state == check:
        basic.check_win()
        action_point = action_point - 1
        if action_point == 0:
            player_id = 1 + player_id % 2
            action_point = 4
        state = action_menu


    game_window.blit(imp, (0, 0))
    print_player()
    print_city()


    pygame.display.flip()
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            print("pres any key to quit")
            quit_game = True