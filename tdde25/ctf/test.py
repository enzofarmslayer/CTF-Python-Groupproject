def decide(self):
        """ Main decision function that gets called on every tick of the game.
        """
        next(self.move_cycle_gen())

def move_cycle_gen(self):
        """ A generator that iteratively goes through all the required steps
            to move to our goal.
        """
        print('before first yield')
        yield
        print('after first yield')

while True