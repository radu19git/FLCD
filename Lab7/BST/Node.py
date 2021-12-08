
class Node:
    def __init__(self, value, index):
        self.left = None
        self.right = None
        self.index = index
        self.value = value

    def __repr__(self):
        return f"{self.index} ---> {self.value}"