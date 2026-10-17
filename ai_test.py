import pygame
import random
import math
import numpy as np

from ai import ai
from Food import Food
pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
my_font = pygame.font.Font(None, 50)
screen.fill((0, 0, 0))
tick = 0
total_energy_used = 0
running = True
my_ai = ai("my_ai", 100,100, 0,0, 50,(70, 130, 180))
food = Food(100,20)
food_list = []
food_list.append(food)
food_eaten_count = 0
my_ai.link_nodes()
my_ai.run_nodes([0.5, 0.3, 0.2])
my_ai.x_dif = 0
my_ai.y_dif = 0
hunger = 0
last_total_loss = 1000000000
check = 0
change = 0
last_total_fitness = -100000
def find_food():
    x_dif = (food.x + (food.size//2)) - (my_ai.x + (my_ai.size//2))
    y_dif = (food.y + (food.size//2)) - (my_ai.y + (my_ai.size//2))
    my_ai.x_dif = x_dif
    my_ai.y_dif = y_dif
    pos_dif = [x_dif, y_dif]
    return pos_dif

def check_collision():
    cx = my_ai.x + (my_ai.size // 2)
    cy = my_ai.y + (my_ai.size // 2)
    for m in range(len(food_list) - 1, -1, -1):
            food = food_list[m]
    
            dx = (food.x + food.size // 2) - cx
            dy = (food.y + food.size // 2) - cy
            dist = math.sqrt(dx**2 + dy**2)
    
            if dist < (my_ai.size // 2):
                food_list.pop(m)
                my_ai.hunger -= 100
                my_ai.food_eaten_count +=1
                new_food_x = random.randint(10//2, width- 10//2)
                new_food_y = random.randint(10//2, height - 10//2)
                food = Food(new_food_x, new_food_y)
                food_list.append(food)


    
              
def run():
    global tick
    global total_energy_used
    global last_total_fitness
    global food_eaten_count
    global running
    
    while running:
            # Look for events (mouse clicks, key presses, closing window)
        for event in pygame.event.get():

            if event.type == pygame.QUIT:  # If user clicks the 'X' button
                running = False 
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Pressing the 'Esc' key
                    running = False           # Break the loop
        
        screen.fill((0, 0, 0))
        tick+=1
        hunger = 0.5
        my_ai.x_dif = 0
        my_ai.y_dif = 0
        find_food()
        x_dif_food = my_ai.x_dif
        y_dif_food = my_ai.y_dif

        inputs = [my_ai.x_dif, my_ai.y_dif, hunger]
        outputs = my_ai.run(inputs)
        my_ai.update_hunger()
        x_error = x_dif_food - my_ai.x_dif
        y_error = y_dif_food - my_ai.y_dif
        learning_rate = 1
        changeAB = learning_rate *  np.outer(inputs, [x_error, y_error, 0,0])
       

        #my_ai.W_AB += change
        # Move the character step-by-step using your newly fixed delta values
        my_ai.x += my_ai.delta_x
        my_ai.y += my_ai.delta_y
        delta_pos_sqrd = (my_ai.delta_x**2 + my_ai.delta_y**2)
    

        energy_used = 0.1*delta_pos_sqrd + 1
        my_ai.hunger += energy_used
        total_energy_used += energy_used

        survival_reward = tick * 1.0
        energy_penalty = total_energy_used * 0.001
        food_bonus = food_eaten_count * 500.0 
        #my_ai.total_fitness = survival_reward + food_bonus - energy_penalty
        #print("fitness   ", my_ai.total_fitness)
        check_collision()
        if my_ai.alive == 0:
            food_pen = 5*math.sqrt(find_food()[0]**2 + find_food()[1]**2)
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