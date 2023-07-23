from enum import Enum

class PrimaryColors(Enum):
    PURPLE = "#492a42"
    GREEN = "#1C4C38"
    BLUE = "#005288"
    ORANGE = "#DD663C"

class SecondaryColors(Enum):
    PURPLE = "#A899A5"
    GREEN = "#d8eded"
    BLUE = "#bdd7e5"
    LAVENDER = "#e6e6fa"
    PANTONE = "#d6dbe0"

class ColorList(Enum):
    ONE = ["#A899A5"]
    TWO = ["#A899A5", "#99a89c"]
    THREE = ["#a899a5", "#a5a899", "#99a5a8"]
    FOUR = ["#a899a5", "#99a89c", "#999ea8", "#a8a399"]
    FIVE = ["#a899a5", "#99a89c", "#999ea8", "#a8a399", "#d4ccd2"]

if __name__ == "__main__":
    print(ColorList.TWO)
    print(ColorList.TWO.value)