
import pygame
import random
import math
import numpy as np

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


my_ai = ai("my_ai", 100, 100, 50, (70, 130, 180)) # (name, x =100, y =100, size, colour)
food = Food(100,20) # (x, y)
food_list = []
food_list.append(food) # list to add other food
#--------------- Object creation ^^^^^

tick = 0
running = True

#----------------------------------------------------------------------------------endsetup
# Main Code
# Function Setup vvvvvvvv   (skip to run for context)
def find_food():
    x_dif = (food.x + (food.size//2)) - (my_ai.x + (my_ai.size//2))
    y_dif = (food.y + (food.size//2)) - (my_ai.y + (my_ai.size//2))
    my_ai.x_dif = x_dif
    my_ai.y_dif = y_dif
    pos_dif = [x_dif, y_dif]
    return pos_dif

def check_collision():
    cx = my_ai.x + (my_ai.size // 2) # ai centre calc
    cy = my_ai.y + (my_ai.size // 2)
    for m in range(len(food_list) - 1, -1, -1):   # This is helpful: for loop but USUALLY 'm' is not an index it is the actual object, in this case it is the index as length (len) was used
            food = food_list[m]
    
            dx = (food.x + food.size // 2) - cx # food centre calc
            dy = (food.y + food.size // 2) - cy
            dist = math.sqrt(dx**2 + dy**2)
    
            if dist < (my_ai.size // 2):
                food_list.pop(m) # remove from list
                my_ai.hunger -= 100
                my_ai.food_eaten_count +=1
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
   
        x_error, y_error = find_food()
        inputs = [my_ai.x_dif, my_ai.y_dif, 0]
        outputs = my_ai.run(inputs)
        my_ai.update_hunger()

        # this is for future
        learning_rate = 1
        changeAB = learning_rate *  np.outer(inputs, [x_error, y_error, 0,0])
       

        #my_ai.W_AB += change
        # Move the character step-by-step using your newly fixed delta values
        my_ai.x += my_ai.delta_x
        my_ai.y += my_ai.delta_y
        delta_pos_sqrd = (my_ai.delta_x**2 + my_ai.delta_y**2)
    

        energy_used = 0.1*delta_pos_sqrd + 1
        my_ai.hunger += energy_used
        my_ai.total_energy_used += energy_used

        survival_reward = tick * 1.0//10
        energy_penalty = 0#my_aitotal_energy_used * 0.001
        food_bonus = my_ai.food_eaten_count * 500.0 
        #my_ai.total_fitness = survival_reward + food_bonus - energy_penalty
        #print("fitness   ", my_ai.total_fitness)
        check_collision()
        if my_ai.alive == 0:
            food_pen = 10*math.sqrt(find_food()[0]**2 + find_food()[1]**2)
            my_ai.total_fitness = survival_reward + food_bonus - energy_penalty - food_pen
            
            print("Fitness on death:  ", my_ai.total_fitness)
            print("prev fitness on reset:  ", my_ai.last_total_fitness)

            print("Food on death:  ", food_pen)

            if ((my_ai.total_fitness >= my_ai.last_total_fitness)):
                my_ai.last_total_fitness = my_ai.total_fitness
                
                my_ai.random_evo()
                my_ai.reset(100,100, 50)
                
                tick =0
                print("YAY")



                print("  ")
                my_ai.has_undone =1
            elif my_ai.has_undone == 1:
                my_ai.has_undone = 0
                my_ai.reverse_prev_evo(0)
                my_ai.reset(100, 100, 50)

                tick = 0
                print("BAD")
                print("  ")
            elif my_ai.has_undone == 0:
                my_ai.reverse_prev_evo(1)
                my_ai.reset(100, 100, 50)
                my_ai.has_undone = 1
            else:
                    my_ai.reset(100,100,50)     
                    tick = 0
                    
                    print("  ")


            

        pygame.draw.rect(screen, (my_ai.colour), (my_ai.x, my_ai.y, my_ai.size, my_ai.size))
        for this_food in food_list:

            pygame.draw.rect(screen, (0, 255,0), (this_food.x, this_food.y, this_food.size, this_food.size))

        # Clear the screen with a background color (e.g., Black)

        # (Your game logic and rendering go here)

        # Refresh the display to show changes
        pygame.display.flip()
run()
# 4. Clean exit when loop ends
pygame.quit()