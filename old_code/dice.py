import numpy as np
import pandas as pd
import matplotlib.pylab as plt

score_to_win = 13 # number of brains you need to win a game
shots_that_end_turn = 3 # number of shots required to force end your turn
num_dice_roll = 3 # number of dice you roll each turn
# number of colored dice that you start with in the container
n_green_dice = 6
n_yellow_dice = 4
n_red_dice = 3
# the distibution of the sides on each colored die
green_dice = ['brain','brain','brain','feet','feet','shot']
yellow_dice = ['brain','brain','feet','feet','shot','shot']
red_dice = ['brain','feet','feet','shot','shot','shot']

class Dice(object):
    '''
    A zombie dice of a color with corresponding hard coded distribution of brains, feets, shots for the sides
    you can roll the dice
    '''
    def __init__(self,color):
        if color == 'green':
            self.sides = green_dice
        elif color == 'yellow':
            self.sides = yellow_dice
        elif color == 'red':
            self.sides = red_dice
        self.color = color

    def __repr__(self):
        ''' dice are represented by their color '''
        return self.color

    def roll(self):
        ''' returns a random single side of the die '''
        return np.random.choice(self.sides,1)[0]


class Container(object):
    '''
    The container holds the dice. dice are randomly pulled from the container
    you can check the number and colors of any remaining dice in the container
    you can shake the container to shuffel the dice
    '''

    def __init__(self,greens=n_green_dice, yellows=n_yellow_dice, reds=n_red_dice):
        self.dice = np.hstack([
        [Dice('green') for _ in range(greens)],
        [Dice('yellow') for _ in range(yellows)],
        [Dice('red') for _ in range(reds)]])

    def num_color(self,color):
        ''' returns the number of the given color in ('green','yellow','red')'''
        return len([d for d in self.dice if d.color == color])

    def __repr__(self):
        '''prints how many dice are left in the bag'''
        return '{} green | {} yellow | {} red'.format(
        self.num_color('green'),
        self.num_color('yellow'),
        self.num_color('red'))

    def shake(self):
        ''' shuffles the order of the dice'''
        self.dice = np.random.choice(self.dice,len(self.dice),replace = False)


class Player(object):
    '''
    The player manipulates the container and the dice while counting points
    the player can be named and can be a human or computer player
        - roll the dice
        - start a turn for themselves
    a non-human player has coded logic
    '''
    def __init__(self, name = None, human = True, com_logic = 1):
        if name is None and human:
            self.name = 'human player'
        elif name is None and not human:
            self.name = 'computer player'
        else:
            self.name = name
        self.human = human

        # set all the base player attributes
        self.brains = 0 # number of brains they have for the turn
        self.shots = 0 # number of shots
        self.dice = np.array([]) # dice they have in hand
        self.container = Container() # dice left in their container
        self.score = 0 # the players current score
        self.round = 0 # what round the player in on
        self.com_logic = com_logic

    def __repr__(self):
        ''' prints out the current score and dice roll for the player '''
        line1 = '{}: total score: {}, this round: {} brains, {} shots'.format(self.name, self.score, self.brains, self.shots)
        return line1

    def get_player_state(self):
        ''' returns all the relevent game information for the player in a dictionary'''
        return {'brains':self.brains,
                'shots':self.shots,
                'score':self.score,
                'dice':self.dice,
                'container':self.container,
                'round':self.round} #all the information of the player

    def roll_dice(self):
        '''
        the player rolling the dice in their hand plus new random dice (up to num_dice_roll)
            - any new dice is removed from the container
            -
        '''
        if self.human: print '\n-- you rolled --'
        for i in range(num_dice_roll-len(self.dice)):
            self.container.shake() # shuffel the container
            # add the first dice to the players hand
            self.dice = np.hstack([self.dice,self.container.dice[0]])
            # remove the first dice from the container
            self.container.dice = self.container.dice[1:]
        keep_dice = [] # the dice that roll feet and are kept for the next roll

        # loop over the dice in the players hand
        for i,dice in enumerate(self.dice):
            roll = dice.roll()

            # print the human's roll outcomes
            if self.human: print dice.color, roll

            # update the rounds values
            if roll == 'brain':
                self.brains += 1
            elif roll == 'shot':
                self.shots += 1
            elif roll == 'feet':
                keep_dice.append(i) #what dice to keep in the players hand
        if len(keep_dice)>0:
            self.dice = self.dice[keep_dice] #keep the dice in any exist
        else:
            self.dice = np.array([]) #if no feet were rolled, empty the players hand

        if self.human: # print the player state after the roll
            print '-- end roll --\n'

            print 'dice in hand:',self.dice
            print 'dice in container:'
            print self.container


    def set_com_logic(self, thresh=.5):
        '''
        the logic the computer players follow based on the actual probablilty at any given player state
        '''
        if thresh == 'logic':
            if self.shots == 0:#always go for it when you have no shots
                return 'y'
            elif self.shots == 1 and self.brains < 5:
                return 'y'
            elif self.shots == 2 and self.brains < 3:
                return 'y'
            else:
                return 'n'
        else:
            player_state = self.get_player_state()
            p = turn_prob(player_state)
            if p > thresh: # if the probabilty of striking out is greater than 50% don't risk it
                return 'n'
            else:
                return 'y'

    def start_turn(self, playbyplay=True):
        '''
        calls self.roll_dice until the player strikes out with too many shots or choses to end their turn and keep their points
        playbyplay prints to the terminal what is happening in the game and requires actions to continue the game to help slow it down
        '''
        # everyone is still playing to start their turn
        still_playing = 'y'

        # while you have selected to keep playing
        # and you <3 shots
        # and you have enough dice to roll a full 3 dice
        # and you don't have the win
        # if any of these are false then your turn ends
        while still_playing == 'y' and self.shots < shots_that_end_turn and len(self.container.dice)>=3-len(self.dice) and self.score+self.brains < score_to_win:

            self.roll_dice() # roll the dice
            if self.shots < shots_that_end_turn: # if you dont strike out
                if self.human: # ask the human if they want to continue
                    print self
                    still_playing = raw_input('--> Continue to roll? (y/n): ')
                    if still_playing == '': still_playing = 'y' # accept enter as a shortcut for yes
                else: # otherwise the computer logic tells the game if the com player continues
                    if playbyplay: print self
                    still_playing = self.set_com_logic(thresh=self.com_logic)

        if self.shots < shots_that_end_turn:
            self.score += self.brains # if the player didn't strike out update their score
        else: # othersize tell the game that this player's turn was ended with no points awarded
            if playbyplay or self.human: print '--> Turn Over: {} got shot {}+ times\n'.format(self.name, shots_that_end_turn)

        # reset the players turn information
        self.shots = 0
        self.brains = 0
        self.dice = np.array([]) # remove all dice in hand
        self.container = Container() # reset to a full container
        self.round +=1 # update the completed round count

class Game(object):
    '''
    games are started with a number of players
    the game asks the players names, unnamed players are computers

    once the game is started players go through rounds
    the game checks if there is a winner at the end of each round
    the game ends when a winner is found
    '''
    def __init__(self, n_players, playbyplay = True):
        self.playbyplay = playbyplay
        if type(n_players) == type([]) or type(n_players) == type(np.array([])):
            self.players = n_players
        elif type(n_players) == type(5): # ask for players
            self.players = []
            for n in range(n_players):
                name = raw_input("player name? (enter, '', or 'com' to create computer player): ")
                if name == '' or name == 'com':
                    name = 'computer{}'.format(n)
                    p = Player(name,human =False)
                else:
                    p = Player(name)
                self.players.append(p)

    def round(self):
        for player in self.players:
            if self.playbyplay: _ = raw_input('--> Get ready {} (hit enter to continue)'.format(player.name))
            player.start_turn(playbyplay=self.playbyplay)
        if self.playbyplay:
            print ''
            for player in self.players: print '{}: total score = {}'.format(player.name,player.score)


    def check_winner(self):
        return [True for player in self.players if player.score >= score_to_win]

    def start_game(self):
        self.round_num = 0
        while not self.check_winner():
            self.round_num +=1
            self.round()
            if not self.check_winner() and self.playbyplay:
                _ = raw_input('--> End of round {} (hit enter to continue)\n----------------------\n'.format(self.round_num))
        self.winners = [player.name for player in self.players if player.score >= score_to_win]
        if self.playbyplay: print 'Congrats to {} for winning the game!'.format(' & '.join(self.winners))


    def get_game_state(self):
        dict([(player.name,player.player_state) for player in self.players])
        return self.game_state


def make_player_from_state(player_state):
    p = Player('fake_player', human = False)
    p.brains = player_state['brains']
    p.shots = player_state['shots']
    p.score = player_state['score']

    # make a new instance so it doesnt change player_state
    p.container = Container(greens = player_state['container'].num_color('green'),
    reds = player_state['container'].num_color('red'),
    yellows = player_state['container'].num_color('yellow'))
    p.dice = player_state['dice']
    p.round = player_state['round']
    p.player_state = p.get_player_state()
    return p


def turn_prob(player_state, n=100):
    out = []
    for i in range(n):
        player = make_player_from_state(player_state)
        # print player.player_state
        player.roll_dice()
        out.append(1) if player.shots >= shots_that_end_turn else out.append(0)
    return 1.0*sum(out)/n







if __name__ == '__main__':
    c = Container()
    d = Dice('green')
    out = []
    for i in range(500):
        try:
            even = Player(name = 'even', human=False, com_logic = .5)

            conservative = Player(name = 'conservative', human=False, com_logic = .4)

            risky = Player(name = 'risky',human=False,com_logic = .6)

            normal1 = Player(name = 'norm1',human=False,com_logic = 'logic')
            normal2 = Player(name = 'norm2',human=False,com_logic = 'logic')
            # g = Game([even, even2, conservative, conservative2, risky, risky2],playbyplay=False)
            g = Game([even, conservative, risky, normal1, normal2], playbyplay=False)

            g.start_game()
            out.append('_'.join(g.winners))
        except:
            pass
    out = pd.Series(out)
    print out.value_counts()/len(out)
    # p.start_turn()


    # p = Player(name = 'jan')
    # p.roll_dice()
    # player_state = p.get_player_state()
    # print player_state
    # print turn_prob(player_state, n=100)
    # print player_state
# i should make a flag that prints and asks nothing if all players are computers


#     n = 1000
#     out = []
#     for i in range(n):
#         com = player(human = False)
#         while com.score < 13: #13 points to win
#             com.start_turn()
#         out.append([com.score,com.round])
# out = pd.DataFrame(out)
# out.columns = ['score','round']
# pdf = out['round'].value_counts()/len(out['round'])
# pdf.sort_index(inplace = True)
# pdf.cumsum().plot()

    # bout = np.array(bout)
    # sout = np.array(sout)
    #
    # print 'brains'
    # for i in range(4):
    #     print i, 1.0*np.sum(bout==i)/n
    #
    # print 'shots'
    # for i in range(4):
    #     print i, 1.0*np.sum(sout==i)/n

    # p.roll_dice()
    # p.roll_dice()
