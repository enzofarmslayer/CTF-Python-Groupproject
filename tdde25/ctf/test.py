class Enzo:
    def __init__(self, sprite):
        self.sprite = sprite
        self.sprite = "sosh"
    def updateName(self):
        self.sprite += 'cum'
    def updateNameName(self):
        self.updateName()
        self.updateName()

class Tobias(Enzo):
    def __init__(self, x, y, v, sprite):
        self.sprite = sprite

        self.sprite += 'cumerow'

test = Tobias(1, 'sosh', 'enzo', 'tobias')
test.updateNameName()
print(test.sprite)