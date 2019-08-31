

### code that i didn't end up using


    zombie = Zombie()
    jar = gb.Jar()
    # zombie_ = turn.start_turn(human_zombie=True)

    j=gb.Jar(1,2,3)
    t=Turn(zombie, j)





    turn = Turn(zombie,jar)
    # turn.roll_dice()
    zombie_ = turn.start_turn(human_zombie=True)

    # first roll prob to die
    shots = []
    brains = []
    for i in range(1000):
        turn = Turn(zombie,jar)
        turn.roll_dice()
        brains.append(turn.zombie.brains)
        shots.append(turn.zombie.shots)
    shots = np.array(shots)
    brains = np.array(brains)

    print 'prob to die', 1.0*len(shots[shots>=shots_needed_to_die]) / len(shots)
    print 'mean brains', np.mean(brains)

    # first turn prob to win

    shots = []
    brains = []
    for i in range(1000):
        turn = Turn(zombie,jar)
        p = turn.start_turn()

        brains.append(p.brains)
        shots.append(p.shots)
    shots = np.array(shots)
    brains = np.array(brains)

    print 'prob to die', 1.0*len(shots[shots>=shots_needed_to_die]) / len(shots)
    print 'prob to win', 1.0*len(brains[brains>=brains_needed_to_win]) / len(brains)
    print 'mean brains', np.mean(brains)





    def dice_roll(zombie, jar):
        my_dice = jar.get_dice()
        my_roll = roll_dice(my_dice)

        for i, roll in enumerate(my_roll):
            if roll == 'brain':
                zombie.brains = zombie.brains + 1
            elif roll == 'shot':
                zombie.shots = zombie.shots + 1
            elif roll == 'feet':
                jar.add_dice(my_dice[i])



    def iter_roll(zombie, jar, n=10000):
        brains = []
        shots = []
        for i in range(n):
            p1 = copy_zombie(zombie)
            j1 = copy_jar(jar)
            dice_roll(p1, j1)
            brains.append(p1.brains)
            shots.append(p1.shots)
        brains = np.array(brains)
        shots = np.array(shots)
        return brains, shots

    def get_roll_prob(brains, shots):
        mean_brains = brains.mean()
        prob_winning = 1.0*len(brains[brains>=brains_needed_to_win])/len(brains)
        prob_die = 1.0*len(shots[shots>=shots_needed_to_die])/len(shots)
        return mean_brains, prob_winning, prob_die

    def iter_turn(zombie, jar, n=10):
        # i don't get the points right before the zombie dies
        brains = []
        shots = []
        for i in range(n):
            brains_ = []
            p1 = copy_zombie(zombie)
            j1 = copy_jar(jar)
            while p1.brains < brains_needed_to_win and p1.shots < shots_needed_to_die and len(j1.dice) > 0:
                dice_roll(p1, j1)
                # brains_.append(p1.brains)
            # brains.append(brains_[-2])
            shots.append(p1.shots)
        return np.array(brains), np.array(shots)


    zombie = zombie()
    jar = gb.Jar()

    brains, shots = iter_roll(zombie, jar, n=1000)

    print get_roll_prob(brains, shots)

    brains, shots = iter_turn(zombie,jar,n=100)
    print get_roll_prob(brains, shots)


    # zombie = zombie(start_brains=10)
    # jar = gb.Jar()
    #
    # brains, shots = iter_roll(zombie, jar, n=10000)
    #
    # print get_roll_prob(brains, shots)







    ## chance of getting out on the first roll
