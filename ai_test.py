
import pygame
import random
import math
import numpy as np
import copy

from ai import ai    # my class, (importing class name from class file name)
from Food import Food # my class again

pygame.init() #this is for display
#  ^^^^^^^Importing in built functions and my classes for python^^^^^

#-----------------------------------------------------------------------------------setup vvv
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
my_font = pygame.font.Font(None, 50)
screen.fill((0, 0, 0))
#--------------- Screen display^^^^^

AI_list= []
my_ai = ai("my_ai", 100, 100, 50, (70, 130, 180)) # (name, x =100, y =100, size, colour)
for i in range(5):
    # Create a brand new instance so its functions are perfectly intact
    new_ai = ai(f"ai_{i}", 100, 100, 50, (70, 130, 180))
    
    # 3. Safely copy ONLY the numerical neural network weights/matrices
    # Change 'W_AB' to whatever the exact name of your weight matrix is inside your ai class!
    new_ai.W_AB = copy.deepcopy(my_ai.W_AB) 
    
    AI_list.append(new_ai)
food = Food(100,20) # (x, y)
food_list = []
food_list.append(food) # list to add other food
#--------------- Object creation ^^^^^

tick = 0
running = True

#----------------------------------------------------------------------------------endsetup
# Main Code
# Function Setup vvvvvvvv   (skip to run for context)

def find_food(this_ai):
    print(this_ai)
    x_dif = (food.x + (food.size//2)) - (this_ai.x + (this_ai.size//2))
    y_dif = (food.y + (food.size//2)) - (this_ai.y + (this_ai.size//2))
    this_ai.x_dif = x_dif
    this_ai.y_dif = y_dif
    pos_dif = [x_dif, y_dif]
    return pos_dif

def check_collision(this_ai):
    cx = this_ai.x + (this_ai.size // 2) # ai centre calc
    cy = this_ai.y + (this_ai.size // 2)
    for m in range(len(food_list) - 1, -1, -1):   # This is helpful: for loop but USUALLY 'm' is not an index it is the actual object, in this case it is the index as length (len) was used
            food = food_list[m]
    
            dx = (food.x + food.size // 2) - cx # food centre calc
            dy = (food.y + food.size // 2) - cy
            dist = math.sqrt(dx**2 + dy**2)
    
            if dist < (this_ai.size // 2):
                food_list.pop(m) # remove from list
                this_ai.hunger -= 100
                this_ai.food_eaten_count +=1
                # creating new food vvvv
                new_food_x = random.randint(10//2, width - 10//2)
                new_food_y = random.randint(10//2, height - 10//2)
                food = Food(new_food_x, new_food_y)
                food_list.append(food)

#End function setup
    
              
def run():
    global tick
    global running
    
    while running:
        for event in pygame.event.get(): # This line checks if user interacted by pressing a button or clicking etc (can be used to control smth too)

            if event.type == pygame.QUIT:  # If user clicks the 'X'/close button
                running = False 
            elif event.type == pygame.KEYDOWN: # this line is if a key has been pressed
                if event.key == pygame.K_ESCAPE:  # Pressing the 'Esc' key   --- Note: esc closes tab entirely
                    running = False           # Break the loop/quits game
        
        screen.fill((0, 0, 0)) # wipe screen
        tick+=1 # time measure
        hunger = 0.5
        for this_ai in AI_list:
            print(this_ai.x)
            x_error, y_error = find_food(this_ai)
            inputs = [this_ai.x_dif, this_ai.y_dif, 0]
            outputs = this_ai.run(inputs)
            this_ai.update_hunger()

        # this is for future
            learning_rate = 1
            changeAB = learning_rate *  np.outer(inputs, [x_error, y_error, 0,0])
        

            #my_ai.W_AB += change
            this_ai.x += this_ai.delta_x
            this_ai.y +=this_ai.delta_y
            delta_pos_sqrd = (this_ai.delta_x**2 + this_ai.delta_y**2)
        

            energy_used = 0.1*delta_pos_sqrd + 1
            this_ai.hunger += energy_used
            this_ai.total_energy_used += energy_used

            survival_reward = tick * 1.0//10
            energy_penalty = 0 #my_aitotal_energy_used * 0.001
            food_bonus = this_ai.food_eaten_count * 500.0 
            #my_ai.total_fitness = survival_reward + food_bonus - energy_penalty
            #print("fitness   ", my_ai.total_fitness)
            check_collision(this_ai)
            if this_ai.alive == 0:
                food_pen = 10*math.sqrt(find_food(this_ai)[0]**2 + find_food(this_ai)[1]**2)
                this_ai.total_fitness = survival_reward + food_bonus - energy_penalty - food_pen
                
                print("Fitness on death:  ", this_ai.total_fitness)
                print("prev fitness on reset:  ", this_ai.last_total_fitness)

                print("Food on death:  ", food_pen)

                if ((this_ai.total_fitness >= this_ai.last_total_fitness)):
                    this_ai.last_total_fitness = this_ai.total_fitness
                    
                    this_ai.random_evo()
                    this_ai.reset(100,100, 50)
                    
                    tick =0
                    print("YAY")



                    print("  ")
                    this_ai.has_undone =1
                elif this_ai.has_undone == 1:
                    this_ai.has_undone = 0
                    this_ai.reverse_prev_evo(0)
                    this_ai.reset(100, 100, 50)

                    tick = 0
                    print("BAD")
                    print("  ")
                elif this_ai.has_undone == 0:
                    this_ai.reverse_prev_evo(1)
                    this_ai.reset(100, 100, 50)
                    this_ai.has_undone = 1
                else:
                        this_ai.reset(100,100,50)     
                        tick = 0
                        
                        print("  ")


            

            pygame.draw.rect(screen, (this_ai.colour), (this_ai.x, this_ai.y, this_ai.size, this_ai.size))
            for this_food in food_list:

                pygame.draw.rect(screen, (0, 255,0), (this_food.x, this_food.y, this_food.size, this_food.size))

        # Clear the screen with a background color (e.g., Black)

        # (Your game logic and rendering go here)

        # Refresh the display to show changes
        pygame.display.flip()
run()
# 4. Clean exit when loop ends
pygame.quit()