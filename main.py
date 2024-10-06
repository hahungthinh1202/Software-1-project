import pygame
import queue
import threading
import action
import basic
import graphic
import infection
import player
from str_list import *
win_lose = False
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

def main_menu_print(s,string):
    if string == "up":
        s = s - 1
        if s < 1: s = 1
    elif string == "down":
        s = s + 1
        if s > 3: s = 3
    elif string == "ok":
        if s == 1:
            basic.game_init(6, 2)
            print("do 1")
        elif s == 2:
            print("do 2")
        elif s == 3:
            print("do 3")
        return False
    graphic.print_main_menu(250, 172 + s * 57)
    return s


(main_menu, action_menu, action_execute, computer, endgame) = ('main_menu','action_menu','action_execute','computer', 'endgame')

state = main_menu
my_choice = 1
main_menu_print(my_choice, "")
next_state = main_menu
current_player = 1
action_point  = 4
flag = 0
while not quit_game:
    try:
        command = commands.get(False)
    except queue.Empty:
        command = None

    if state == main_menu and command is not None:
        my_choice = main_menu_print(my_choice, command)
        if not my_choice:
            next_state = action_menu
    elif state == action_menu:
        graphic.print_action_menu(current_player, action_point)

        move_data  = action.move_check(current_player)
        action.move_detail_print(move_data)

        treat_data = action.treat_check(current_player)
        if len(treat_data)>1:
            action.treat_detail_print(treat_data)

        build_data = action.build_check(current_player)
        if build_data:
            action.build_detail_print(build_data)

        cure_data = action.cure_check(current_player)
        if cure_data:
            action.cure_print(cure_data)
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
            elif command_1 == 'cure' and not action.cure_execute(current_player,cure_data,command_2):
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
        win_lose = basic.check_win()
        if win_lose:
            next_state = endgame
        else:
            next_state = action_menu
    elif state == endgame:
        graphic.print_endgame(win_lose)


    if state != main_menu and state != endgame:
        graphic.print_map()
    state = next_state

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            print("pres any key to quit")
            quit_game = True