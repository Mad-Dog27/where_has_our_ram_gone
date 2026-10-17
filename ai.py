from Node import Node
from Food import Food
import numpy as np
import random

# Create a 3x4 array filled with the value 7
val = 7
arr = np.full((3, 4), val)

class ai:
    def __init__(self, name, x, y, desired_x, desired_y, size, colour):
        self.firstNum = 3
        self.secondNum = 4
        self.thridNum = 3
        self.name = name
        self.hunger = 0
        self.x = x - size/2
        self.y = y - size /2
        self.delta_x = 0
        self.delta_y = 0
        self.matrix_size = [3, 4, 3]
        self.B_bias = np.full(self.matrix_size[1], 0)
        self.C_bias = np.full(self.matrix_size[2], 0)
        self.alive = 1
    
        self.W_AB = np.random.randn(self.matrix_size[0], self.matrix_size[1]) # Random weight numbers
        self.W_BC = np.random.randn(self.matrix_size[1], self.matrix_size[2])

        self.updateamnt = 0
        self.last_total_fitness = -10000

        self.current_outputs = self.C_bias
        self.x_dif  = 0
        self.y_dif = 0
        
        self.last_total_loss = 10000
        self.lastABRowChange = 0
        self.lastABColChange = 0
        self.size = size
        self.colour = colour
        self.food_eaten_count = 0
        self.has_undone = 0

        self.firstNodeList = [Node(), Node(), Node(), Node()]
        self.secondNodeList = [Node(), Node(), Node(), Node()]
        self.thirdNodeList = [Node(), Node(), Node(), Node()]
        self.link_nodes()

    def run(self,inputs):
        inputs = np.array(inputs)
        #print("DEBUG INPUTS:", inputs)
        B = self.relu(inputs @ self.W_AB + self.B_bias)
        #print("DEBUG BBBBBB:", B)

        C = B @ self.W_BC + self.C_bias
        #print("DEBUG CCCCCCC:", C)

        C_squashed = np.tanh(C)
        self.current_outputs = C_squashed
        speed_cap = .5
        self.delta_x = self.current_outputs[0] * speed_cap
        self.delta_y = self.current_outputs[1] * speed_cap

        return C_squashed
    
    def relu(self, x):
        y = []
        for i in x:
            y.append(max(0,i))
        return np.array(y)
    
    def link_nodes(self):
        for i in self.firstNodeList:
            for j in self.secondNodeList:
                i.link(j)

        for m in self.secondNodeList:
            for n in self.thirdNodeList:
                m.link(n)

    def run_nodes(self, input):
        for i in range(len(input)):
            self.firstNodeList[i].calc = input[i]
            for next_link in self.firstNodeList[i].links:
                print(next_link.calc) 

                next_link.calc = next_link.value * self.firstNodeList[i].value
                print(next_link.calc) 

            

    def random_evo(self):

        ABorBC = np.random.randint(0,2)

        rows, cols = self.W_AB.shape

        rand_row = np.random.randint(0,rows)
        rand_col = np.random.randint(0,cols)
        change_amnt = 1
        self.updateamnt = change_amnt
        self.W_AB[rand_row, rand_col] += change_amnt
        self.lastABRowChange = rand_row
        self.lastABColChange = rand_col
        column = np.random.randint(0,3)
        #print(self.W_AB[rand_row, rand_col])

    def reverse_prev_evo(self, reset):
        if reset == 0:
            self.W_AB[self.lastABRowChange, self.lastABColChange] -= self.updateamnt*2
        else:
            self.W_AB[self.lastABRowChange, self.lastABColChange] += self.updateamnt

    def reset(self, x, y, size):
        
        self.hunger = 0
        self.x = x - size/2
        self.y = y - size /2
        self.delta_x = 0
        self.delta_y = 0

        self.alive = 1

        self.total_fitness = 0



        self.x_dif  = 0
        self.y_dif = 0
        self.last_total_loss = 0
        self.lastABRowChange = 0
        self.lastABColChange = 0

    def update_hunger(self):
        self.hunger +=1
        if self.hunger > 1000:
            self.alive = 0 