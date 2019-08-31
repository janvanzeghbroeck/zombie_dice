import numpy as np

## constants
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
    def __init__(self, color):
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


class Jar(object):
    '''
    The jar holds the dice. dice are randomly pulled from the jar
    you can check the number and colors of any remaining dice in the jar
    you can shake the jar to shuffel the dice
    '''

    def __init__(self, greens=n_green_dice, yellows=n_yellow_dice, reds=n_red_dice):
        self.dice = np.hstack([
        [Dice('green') for _ in range(greens)],
        [Dice('yellow') for _ in range(yellows)],
        [Dice('red') for _ in range(reds)]])

    def num_color(self, color):
        ''' returns the number of the given color in ('green', 'yellow', 'red')'''
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

    def get_dice(self, n=3):
        ''' removes and returns n dice from the jar at random '''
        self.shake()
        gotten_dice = []
        for i in range(n):
            if len(self.dice)>0:
                gotten_dice.append(self.dice[0])
                self.dice = self.dice[1:]
        return gotten_dice

    def add_dice(self, dice_list):
        ''' adds a list of dice to the jar '''
        self.dice = np.hstack([self.dice, dice_list])

if __name__ == '__main__':

    jar = Jar()
