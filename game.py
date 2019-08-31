import game_bits as gb
import numpy as np

shots_needed_to_die = 3
brains_needed_to_win = 13

class Zombie():
    ''' Zombie Dice zombie aka the player'''
    def __init__(self, name='name', start_brains=0, start_shots=0, start_points=0):
        self.name = name  # zombie name
        self.brains = start_brains  # brains the zombie already has
        self.points = start_points
        self.shots = start_shots  # shots the zombie already has
        self.hand = np.array([])  # human hand that holds dice
        self.is_human = True
        self.logic_function = None

    def __repr__(self):
        return '{}\npoints: {}'.format(self.name, self.points)

    def add_dice_to_hand(self, dice_list):
        ''' adds dice to the zombies hand '''
        self.hand = np.hstack([self.hand, dice_list])

    def roll_dice_in_hand(self):
       ''' rolls the dice in the zombies hand '''
       rolls = [dice.roll() for dice in self.hand]
       return np.array(rolls)

    def add_computer_player_logic(self, logic_function):
        '''
            allows you to add a function to create a computer zombie

            Game().start_game() will call self.zombie.logic_function(game_state) and expect 'y' or 'n' as a return

            >>> Return Rules
                Function must return 'y' to keep rolling
            any other return stops rolling 'n' is prefered
            >>> Input Rules
                input to the function is the game_state a list in the following order
                [points, brains, shots, n_green, n_yellow, n_red]
        '''
        self.logic_function = logic_function
        self.is_human = False



def copy_jar(jar):
    ''' copies the info from one jar into a new object '''
    return gb.Jar(greens=jar.num_color('green'),
    yellows=jar.num_color('yellow'),
    reds=jar.num_color('red'))


def copy_zombie(zombie):
    ''' copies the info from one zombie into a new object '''
    zom = Zombie(name=zombie.name, start_brains=zombie.brains, start_shots=zombie.shots)
    zom.is_human = zombie.is_human
    zom.logic_function = zombie.logic_function
    return zom


class Turn():
    ''' controls the time information of a single turn
        copies the information of the jar / zombie
    '''
    def __init__(self, zombie, jar):
        self.zombie = copy_zombie(zombie)
        self.jar = copy_jar(jar)

    def roll_dice(self):
        '''
            moves and rolls the dice between the jar and zombie
            show_game_log prints the actions and results
        '''
        # move dice from jar to zombie's hand
        self.zombie.add_dice_to_hand(self.jar.get_dice())
        # print self.zombie.hand

        # roll the dice
        outcome = self.zombie.roll_dice_in_hand()

        # count points and return any feet dice to the jar
        for roll in outcome:
            if roll == 'shot':
                self.zombie.shots = self.zombie.shots + 1

        # count brains only if zombie has not died
        if self.zombie.shots < shots_needed_to_die:
            for i, roll in enumerate(outcome):
                if roll == 'brain':
                    self.zombie.brains = self.zombie.brains + 1
                elif roll == 'feet':
                    self.jar.add_dice(self.zombie.hand[i])

        # empty the zombie's hand
        self.zombie.hand = np.array([])
        return self.jar, self.zombie

    def start_turn(self):
        ''' '''

        ans='y' # default while loop to continue rolling

        # while the zombie doesnt die or win, keep rolling
        while self.zombie.shots < shots_needed_to_die and self.zombie.brains < brains_needed_to_win and ans == 'y' and len(self.jar.dice) > 0:
            self.roll_dice()

            # points, brains, shots, n_green, n_yellow, n_red
            game_state = [self.zombie.points, self.zombie.brains, self.zombie.shots, self.jar.num_color('green'), self.jar.num_color('yellow'), self.jar.num_color('red')] # can add other players later

            # ask the zombie if they would like to keep rolling
            # only if they aren't dead, a winner, or the jar is empty
            if self.zombie.shots < shots_needed_to_die and self.zombie.brains < brains_needed_to_win and len(self.jar.dice) > 0:

                if self.zombie.is_human == True: # aks the humans
                    print '\n', self.zombie.name, '\nBrains:', self.zombie.brains, '\nShots:', self.zombie.shots
                    print 'Dice:', self.jar
                    ans = raw_input('Do you want to keep chasing them humans? (aka keep roling?) (y/n) ')

                else:
                    ans = self.zombie.logic_function(game_state)
                    # print 'computer player said',  ans


        return self.zombie


class Game():

    def __init__(self, zombie_list):
        self.zombie_list = zombie_list

    def start_game(self, print_log=True, jar=None):
        if jar is None: jar = gb.Jar() # start with normal jar
        have_a_winner = None

        while have_a_winner is None: # while we do not have a winner
            # for each zombie
            for i, zombie in enumerate(self.zombie_list):
                if not have_a_winner:
                    turn = Turn(zombie,jar)
                    zombie_ = turn.start_turn() # play their turn

                    # if they didn't die
                    if zombie_.shots < shots_needed_to_die:
                        # add brains to the zombie's points
                        zombie.points = zombie.points + zombie_.brains
                        if print_log:
                            print '\n*NOM* You made it out with {} tasty brains.'.format(zombie_.brains)
                            print 'You have munched on {} brains thus far.'.format(zombie.points)
                    else: # tell them they died
                        if print_log: print '\n*BANG* The humans got you good. No brains for you.'

                    # do they win?
                    if zombie.points >= brains_needed_to_win:
                        have_a_winner = i

            # print scores
            if print_log: print '\nThe standings thus far:'
            for p in self.zombie_list:
                if print_log: print p.name, ':', p.points, '/', brains_needed_to_win, 'human brains'

        # print the winner
        if print_log: print '\n\n{} is the winner. Good zombie.'.format(self.zombie_list[have_a_winner].name)

        return self.zombie_list[have_a_winner] # return winner

if __name__ == '__main__':



    p1 = Zombie('Undead4ever')
    p2 = Zombie('I<3Brainz')
    game = Game([p1,p2])
    game.start_game()
