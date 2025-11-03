class Height(object):
    def __init__(self, feet, inches):
        self.feet = feet
        self.inches = inches
    
    def __lt__(self, other):
        height_inches_A = self.feet * 12 + self.inches
        height_inches_B = other.feet * 12 + other.inches
        return height_inches_A < height_inches_B

    def __le__(self, other):
        height_inches_A = self.feet * 12 + self.inches
        height_inches_B = other.feet * 12 + other.inches
        return height_inches_A <= height_inches_B

    def __eq__(self, other):
        height_inches_A = self.feet * 12 + self.inches
        height_inches_B = other.feet * 12 + other.inches
        return height_inches_A == height_inches_B

    def __gt__(self, other):
        height_inches_A = self.feet * 12 + self.inches
        height_inches_B = other.feet * 12 + other.inches
        return height_inches_A > height_inches_B

    def __ge__(self, other):
        height_inches_A = self.feet * 12 + self.inches
        height_inches_B = other.feet * 12 + other.inches
        return height_inches_A >= height_inches_B

    def __ne__(self, other):
        height_inches_A = self.feet * 12 + self.inches
        height_inches_B = other.feet * 12 + other.inches
        return height_inches_A != height_inches_B
    
    def __str__(self):
        return f"{self.feet} feet, {self.inches} inches"
    
    # Test cases
h1 = Height(4, 6)
h2 = Height(4, 5)
h3 = Height(4, 5)
h4 = Height(5, 9)
h5 = Height(5, 10)

heights = [h1, h2, h3, h4, h5]

heights = sorted(heights)
for height in heights:
    print(height)