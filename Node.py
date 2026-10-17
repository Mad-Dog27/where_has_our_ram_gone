import random


class Node:
    def __init__(self):
        self.value = round(random.random(),2)
        self.links = []
        self.calc = 0

    def link(self, to_link):
        self.links.append(to_link)