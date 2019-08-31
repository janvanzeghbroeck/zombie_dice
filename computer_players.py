import game_bits as gb
import game as z
import pandas as pd
import numpy as np
import sys
# threading? python import

# add colors
# Black: \u001b[30m
# Red: \u001b[31m
# Green: \u001b[32m
# Yellow: \u001b[33m
# Blue: \u001b[34m
# Magenta: \u001b[35m
# Cyan: \u001b[36m
# White: \u001b[37m
# Reset: \u001b[0m

out = pd.read_csv('roll_probability_data_n10000.csv')
out2  = pd.read_csv('roll_probability_data_n1000.csv')

out.set_index(['greens','yellows','reds'], inplace=True)
out2.set_index(['greens','yellows','reds'], inplace=True)

def simple_comp(game_state):
    return 'n' # stop rolling after first roll

def two_and_done_comp(game_state):
    if game_state[2] == 2: # if you have 2 shots
        return 'n' # stop rolling
    else: # otherwise
        return 'y' # keep rolling

def one_and_done_comp(game_state):
    if game_state[2] > 1: # if you have 1 or more shots
        return 'n' # stop rolling
    else: # otherwise
        return 'y' # keep rolling

def three_plus_brains_comp(game_state):
    if game_state[1] >= 3: # if you 3 or more brains
        return 'n' # stop rolling
    else: # otherwise
        return 'y' # keep rolling

def med1_comp(game_state):
    ''' if you have one or more brains, keep rolling
        otherwise if you have 2 shots, stop rolling
    '''
    if game_state[1] <= 1 : # if you have one or less brains
        return 'y' # keep rolling
    elif game_state[2] == 2: # otherwise if you have 2 shots
        return 'n' # stop rolling
    else: # otherwise
        return 'y' # keep rollings

def med2_comp(game_state):
    if game_state[0] + game_state[1] >= 13:
        return 'n'
    elif game_state[1] <= 1 : # if you have one or less brains
        return 'y' # keep rolling
    elif game_state[2] == 2: # otherwise if you have 2 shots
        return 'n' # stop rolling
    elif game_state[1] >= 5 and game_state[2] == 1: # otherwise if you 5 or more brains and one shot
        return 'n' # stop rolling
    elif game_state[1] >= 7: # otherwise if you 7 or more brains
            return 'n' # stop rolling
    else: # otherwise
        return 'y' # keep rollings

def fancy1_comp(game_state):
    probs = out.loc[game_state[3],game_state[4],game_state[5]]
    mean_shots = probs['mean_shots']
    mean_brains = probs['mean_brains']
    if mean_shots + game_state[2] >= 2.5:
        return 'n'
    else:
        return 'y'

def fancy2_comp(game_state):
    probs = out.loc[game_state[3],game_state[4],game_state[5]]
    mean_shots = probs['mean_shots']
    mean_brains = probs['mean_brains']
    if mean_shots + game_state[2] >= 2:
        return 'n'
    else:
        return 'y'


p1 = z.Zombie('Undead4ever')
c1 = z.Zombie('simple_comp')
c1.add_computer_player_logic(simple_comp)
c2 = z.Zombie('two_and_done')
c2.add_computer_player_logic(two_and_done_comp)
c25 = z.Zombie('one_and_done')
c25.add_computer_player_logic(one_and_done_comp)

c3 = z.Zombie('three_plus_brains')
c3.add_computer_player_logic(three_plus_brains_comp)
c4 = z.Zombie('med1')
c4.add_computer_player_logic(med1_comp)
c5 = z.Zombie('med2')
c5.add_computer_player_logic(med2_comp)
c6 = z.Zombie('fancy1')
c6.add_computer_player_logic(fancy1_comp)
c7 = z.Zombie('fancy2')
c7.add_computer_player_logic(fancy2_comp)

zombies = [c4,c4,c4,c4] #s test impact of randomness in N
zombies = [c2,c25,c5,c6,c7]

p1 = z.Zombie('Jan')
p2 = z.Zombie('Zack')
game = z.Game([p1,p2,c7,c5])
game.start_game()

sys.exit()

n = 1000
winners = []
for j in range(n):
    copy_zombies = [z.copy_zombie(zom) for zom in zombies]
    # add label
    for i,zom in enumerate(copy_zombies):
        zom.name = zom.name + '_' + str(i+1)
    # shuffel who goes first
    np.random.shuffle(copy_zombies)

    game = z.Game(copy_zombies)
    winner = game.start_game(print_log=False)
    winners.append([winner.name, winner.points])
    if j%100 == 0: print j

winners = pd.DataFrame(winners)
winners.columns = ['name','score']
win_prob = winners.name.value_counts() / len(winners)
print win_prob


# game_state example
# points, brains, shots, n_green, n_yellow, n_red
game_state = [0, 2, 2, 5, 3, 2]
