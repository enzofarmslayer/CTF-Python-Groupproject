class Enzo:
    def __init__(self, sprite):
        self.sprite = sprite + 'cum'
    def updateNameName(self):
        self.updateName()
        self.updateName()

class Sosh(Enzo):
    karl = 'rickard'
    def __init__(self, sprite, tobias):
        self.tobias = tobias + self.karl
        super().__init__(sprite)

enzo = Sosh('penis', 'görren')
print(enzo.sprite, enzo.tobias)