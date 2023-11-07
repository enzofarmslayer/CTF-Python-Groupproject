class Enzo:
    def __init__(self, sprite):
        self.sprite = sprite
        self.sprite = "Sosh är en stor fet idiot"
    def updateName(self):
        self.sprite += 'cum'
    def updateNameName(self):
        self.updateName()
        self.updateName()
class Sosh(Enzo):
    def __init__(self, sprite):
        super().__init__(sprite)

tobias = Sosh('enzo')
print(tobias.sprite)

action_map = {
    test: {
        sosh: 'hej',
        enzo: 'hej'
    }
}


        