import pygame
import queue
import threading
import action
import basic
import graphic
import infection
import player
from str_list import *

quit_game = False


class ParallelThread(threading.Thread):
  def run(self):
    while not quit_game:
      command = input()
      commands.put(command)
commands = queue.Queue()
instance = ParallelThread()
instance.start()

def get_command(data):
    c1 = None
    c2 = None
    print(data)
    print(city_list + virus_list)
    for i in city_list + virus_list:
        if data.lower().find(i) != -1:
            c2 = i
            break
    for i in command_list:
        if data.lower().find(i) != -1:
            c1 = i
            break
    if c1 is None:
        print("Not recognize action")
        return False
    elif c1 == "move" and c2 is None:
        print("Not recognize city name  cc")
        return False
    elif (c1 == "treat" or c1 == "cure") and c2 not in virus_list:
        print("Not recognize virus color")
        return False
    else:
        return [c1, c2]

def next_player(player_id):

    return 1 + player_id % 2 , 4
#basic.game_init(6,2)

(main_menu, action_menu, action_execute, computer) = ('main_menu','action_menu','action_execute','computer')

state = action_menu
next_state = 0
current_player = 1
action_point  = 40
flag = 0

while not quit_game:
    try:
        command = commands.get(False)
    except queue.Empty:
        command = None

    if state == action_menu:
        graphic.print_action_menu(current_player, action_point)
        move_data = action.move_check(current_player)
        action.move_detail_print(move_data)
        treat_data = action.treat_check(current_player)
        if len(treat_data)>1:
            action.treat_detail_print(treat_data)
        build_data = action.build_check(current_player)
        if build_data:
            action.build_detail_print(build_data)
        next_state = action_execute
    elif state == action_execute:
        if command is not None and get_command(command):
            [command_1, command_2] = get_command(command)
            if command_1 == 'move':
                destination_id = basic.cityName_to_cityId(command_2)
                if not action.move_execute(current_player, destination_id, move_data):
                    flag = 1
            elif command_1 == 'treat' and not action.treat_execute(current_player, command_2, treat_data):
                flag = 1
            elif command_1 == 'build' and not action.build_execute(current_player):
                flag = 1
            if flag == 1:
                flag = 0
                print("Please retype the action again!")
            else:
                next_state = computer
    elif state == computer:
        action_point = action_point - 1
        if action_point == 0:
            player.draw(current_player)
            player.draw(current_player)
            current_player , action_point = next_player(current_player)
            infection.infect()

        basic.check_win()

        next_state = action_menu


    graphic.print_map()
    state = next_state

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            print("pres any key to quit")
            quit_game = True