import action
import basic
import infection
import player
import SQL


# Set up a new game, include map and player hand.
def game_init(difficulty,num_player):
    basic.setUpMap()
    basic.setUpPlayerDeck(difficulty, num_player)

def gameLogic(command_1, command_2):
    gameStory = []
    if command_1 == "gameInit":
        game_init(3,2)
        gameStory.append(basic.checkWinLoseCondition())
        gameStory.append({
            'eventType' : 'story',
                'story': f"welcome to the game"
        })
        gameStory.append({
            'eventType': 'story',
            'story': f"several virulent diseases have broken<n>"
                     f"out simultaneously all over the world!<n>"
                     f"You and your teammates will travel <n>"
                     f"across the globe treating infections <n>"
                     f"while finding resources for cures<n>"
                     f"Can you find all four cures in time?<n>"
                     f"The fate of humanity is in your hands!"
        })
        return gameData(gameStory)
    elif command_1 == "gameInitTutorial":
        game_init(1, 2)
        gameStory.append(basic.checkWinLoseCondition())
        gameStory.append({
            'eventType': 'story',
            'story': f"welcome to Pandemic game"
        })
        gameStory.append({
            'eventType': 'story',
            'story': f"several virulent diseases have broken<n>"
                     f"out simultaneously all over the world!<n>"
                     f"You and your teammates will travel <n>"
                     f"across the globe treating infections <n>"
                     f"while finding resources for cures<n>"
                     f"Can you find all four cures in time?<n>"
                     f"The fate of humanity is in your hands!"
        })
        SQL.update(f"update game_current set violet = 1, red = 1, yellow = 1;")
        SQL.update(f"update city set blue = 3 where id = 9")
        SQL.update(f"insert player_own values(1,1)")
        SQL.update(f"insert player_own values(1,2)")
        SQL.update(f"insert player_own values(1,3)")
        SQL.update(f"insert player_own values(1,4)")
        SQL.update(f"update city set research_center = 1 where id = 20")
        SQL.update(f"update city set research_center = 1 where id = 4")
        SQL.update(f"update city set research_center = 1 where id = 13")

        print("update")
        return gameData(gameStory)
    else:
        current_player, action_point = basic.getPlayerInfo()
        move_data  = action.moveCheck(current_player)
        treat_data = action.treat_check(current_player)
        cure_data = action.cure_check(current_player)
        if command_1 == 'move':
            destination_id = command_2
            action.move_execute(current_player, destination_id, move_data)
        elif command_1 == 'treat':
            action.treat_execute(current_player, int(command_2), treat_data)
        elif command_1 == 'build':
            action.build_execute(current_player)
        elif command_1 == 'cure':
            action.cure_execute(current_player, cure_data, command_2)
        if action_point == 1:
            gameStory.append(player.drawCard(current_player))
            gameStory.append(player.drawCard(current_player))
            gameStory += infection.infect()
        basic.updatePlayerTurn(current_player)
        gameStory.append(basic.checkWinLoseCondition())
    return gameData(gameStory)


def gameData(gameStory):
    current_player, action_point = basic.getPlayerInfo()
    return_data = {
        'action': {
            'move': action.move_check_info(current_player),
            'treat': action.treat_check(current_player),
            'build': action.build_check(current_player),
            'cure': action.cure_check(current_player)
                },
        'player': basic.return_player_coordinate(),
        'city'  : basic.returnAllCitySituation(),
        'game'  : basic.returnGameInfo(),
        'own'   : action.player_own_info(current_player),
        'computerInfo': gameStory
    }
    return return_data

