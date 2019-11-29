import game_bits as gb
import game as z
import pandas as pd
import numpy as np
import sys

out = pd.read_csv('roll_probability_data_n10000.csv')
out2  = pd.read_csv('roll_probability_data_n1000.csv')



# sys.exit()

# prob to get X or more points during a turn
# onetscore = (s.value_counts()/len(s)).sort_index(ascending=False).cumsum()


# idea of a game state
# [brains, shots, n_green_dice, n_yellow_dice, n_red_dice]
# [advanced n_other_zombies,other_payers_points]

# build out all the different dice combos
red_dice_options = [0,1,2,3]
yellow_dice_options = [0,1,2,3,4]
green_dice_options = [0,1,2,3,4,5,6]

options = pd.DataFrame([[r,y,g] for r in red_dice_options for y in yellow_dice_options for g in green_dice_options])

options.columns = ['r','y','g']

out = []
n = 10000
zombie = z.Zombie()
for r in red_dice_options:
    for y in yellow_dice_options:
        for g in green_dice_options:
            if g+y+r > 0: # do not calculate for zero dice
                jar = gb.Jar(g,y,r)
                print jar
                shots = []
                brains = []
                for i in range(n):
                    turn = z.Turn(zombie,jar)
                    turn.roll_dice()
                    brains.append(turn.zombie.brains)
                    shots.append(turn.zombie.shots)
                shots = np.array(shots)
                brains = np.array(brains)
                out.append([g,y,r,brains,shots])

out = pd.DataFrame(out)
out.columns = ['greens','yellows','reds','brains_array','shots_array']
out['mean_brains'] = out.brains_array.apply(np.mean)
out['mean_shots'] = out.shots_array.apply(np.mean)
out.set_index(['greens','yellows','reds'], inplace=True)
out['prob_0_shots'] = out.shots_array.apply(lambda x: 1.0*len(x[x == 0])/len(x))
out['prob_1plus_shots'] = out.shots_array.apply(lambda x: 1.0*len(x[x >= 1])/len(x))
out['prob_2plus_shots'] = out.shots_array.apply(lambda x: 1.0*len(x[x >= 2])/len(x))
out['prob_3_shots'] = out.shots_array.apply(lambda x: 1.0*len(x[x >= 3])/len(x))

out.to_csv('roll_probability_data_n{}.csv'.format(n))
