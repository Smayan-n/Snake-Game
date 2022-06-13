class ColorGradient():
    def __init__(self, base_color = (0, 255, 0)):

        self.base_color = 255
        self.step = 10

    def getNextColor(self, i):
        
        red = 0
        green = 0
        blue = self.base_color - (i * self.step)

        return "rgb" + str((red, green, blue))