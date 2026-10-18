
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
check =0
alive_sum = 5
#--------------- Screen display^^^^^
num_ai=5
AI_list= []
matrix_size = [3, 4, 3]


#my_ai = ai("my_ai", 100, 100, 50, (70, 130, 180), W_AB, W_BC) # (name, x =100, y =100, size, colour)
for i in range(5):
    W_AB = np.random.randn(matrix_size[0], matrix_size[1]) # Random weight number
    W_BC = np.random.randn(matrix_size[1], matrix_size[2])
    # Create a brand new instance so its functions are perfectly intact
    new_ai = ai(f"ai_{i}", 100, 100, 50, (70, 130, 180), W_AB, W_BC)
    
    # 3. Safely copy ONLY the numerical neural network weights/matrices
    # Change 'W_AB' to whatever the exact name of your weight matrix is inside your ai class!
    
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
    x_dif = (food.x + (food.size/2)) - (this_ai.x + (this_ai.size/2))
    y_dif = (food.y + (food.size/2)) - (this_ai.y + (this_ai.size/2))
    this_ai.x_dif = x_dif
    this_ai.y_dif = y_dif
    pos_dif = [x_dif, y_dif]
    return pos_dif

def check_collision(this_ai):
    cx = this_ai.x + (this_ai.size / 2) # ai centre calc
    cy = this_ai.y + (this_ai.size / 2)
    for m in range(len(food_list) - 1, -1, -1):   # This is helpful: for loop but USUALLY 'm' is not an index it is the actual object, in this case it is the index as length (len) was used
            food = food_list[m]
    
            dx = (food.x + food.size / 2) - cx # food centre calc
            dy = (food.y + food.size / 2) - cy
            dist = math.sqrt(dx**2 + dy**2)
    
            if dist < (this_ai.size / 2):
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
    global check
    global alive_sum
    while running:
        #print("running first: ", running)

        alive_sum = 0
        for event in pygame.event.get(): # This line checks if user interacted by pressing a button or clicking etc (can be used to control smth too)

            if event.type == pygame.QUIT:  # If user clicks the 'X'/close button
                running = False 
            elif event.type == pygame.KEYDOWN: # this line is if a key has been pressed
                if event.key == pygame.K_ESCAPE:  # Pressing the 'Esc' key   --- Note: esc closes tab entirely
                    running = False           # Break the loop/quits game
        if check > 100:
            check += 1
            running = False
        screen.fill((0, 0, 0)) # wipe screen
        tick+=1 # time measure
        hunger = 0.5
        for this_ai in AI_list:
            alive_sum += this_ai.alive
            x_error, y_error = find_food(this_ai)
            this_ai.run()
            this_ai.update_hunger()
      

            check_collision(this_ai)
        
            # this is for future
            learning_rate = 1
            #changeAB = learning_rate *  np.outer(inputs, [x_error, y_error, 0,0])
        

            this_ai.delta_pos_sqrd = (this_ai.x_dif**2 + this_ai.y_dif**2)
            print(this_ai.x_dif**2 + this_ai.y_dif**2)
          
            #my_ai.total_fitness = survival_reward + food_bonus - energy_penalty
            #print("fitness   ", my_ai.total_fitness)
            

        

            

            pygame.draw.rect(screen, (this_ai.colour), (this_ai.x, this_ai.y, this_ai.size, this_ai.size))
            for this_food in food_list:

                pygame.draw.rect(screen, (0, 255,0), (this_food.x, this_food.y, this_food.size, this_food.size))
        print("sum: ", alive_sum)
        if alive_sum <1:
             running = False
        print("running: ", running)

        # Clear the screen with a background color (e.g., Black)

        # (Your game logic and rendering go here)

        # Refresh the display to show changes
        pygame.display.flip()


if check == 0:    
    run()
    check +=1


i = 0
sum = 0
score = []
ratio = []

for this_ai in AI_list:
    
    score.append(this_ai.delta_pos_sqrd)
    sum += score[i]
    print("ai_num  ", this_ai.name)
    print("score: ", this_ai.delta_pos_sqrd)
    i+=1
i = 0
for this_ai in AI_list:
    
    this_ai.current_ratio = (1-score[i]/sum)
    ratio.append(this_ai.current_ratio)
    print("ai_num  ", this_ai.name)
    print("score: ", this_ai.delta_pos_sqrd)

    print("ratio: ", this_ai.current_ratio)
    i +=1
total_sum =0
for j in range(len(ratio)):
    i=0
    for i in range(len(ratio)):
        random_stat = np.random.rand()
        this_ai= AI_list[i]
        print("ai_num  ", this_ai.name)
        print("RANDOMSTAT: ", random_stat)
        print("this ratio : ", this_ai.current_ratio)
        print("this Sum : ", total_sum)
        print("  ")

        if random_stat < ratio[i] + total_sum:
            if random_stat > total_sum:
                this_ai.next_amnt_children +=1
                print("YES")
                print("  ")
                break
        i+=1

for this_ai in AI_list:
            print("for: ", this_ai.name)
            print("ai children: ", this_ai.next_amnt_children)
# 4. Clean exit when loop ends
pygame.quit()