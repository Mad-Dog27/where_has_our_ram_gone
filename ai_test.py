
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
for i in range(50):
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
            this_food = food_list[m]
    
            dx = (this_food.x + this_food.size / 2) - cx # food centre calc
            dy = (this_food.y + this_food.size / 2) - cy
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
    
              
def run(Current_AI_List):
    global tick
    global check
    global running
    global alive_sum
    running = True
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
        for this_ai in Current_AI_List:
            alive_sum += this_ai.alive
            x_error, y_error = find_food(this_ai)
            this_ai.run()
            this_ai.update_hunger()


            check_collision(this_ai)
        
            # this is for future
            learning_rate = 1
            #changeAB = learning_rate *  np.outer(inputs, [x_error, y_error, 0,0])
        
            # score
            this_ai.delta_pos_sqrd = math.sqrt(this_ai.x_dif**2 + this_ai.y_dif**2)
        
            

            pygame.draw.rect(screen, (this_ai.colour), (this_ai.x, this_ai.y, this_ai.size, this_ai.size))
            for this_food in food_list:

                pygame.draw.rect(screen, (0, 255,0), (this_food.x, this_food.y, this_food.size, this_food.size))
        if alive_sum <1:
            running = False
                

        # Clear the screen with a background color (e.g., Black)

        # (Your game logic and rendering go here)

        # Refresh the display to show changes
        pygame.display.flip()

# ------------------------------- SCORING ---------------------------------
def score(Current_AI_List):
    i = 0
    sum = 0
    score = []
    ratio = []
    To_Have_Children = []
    Children_list = []
    global running
    # getting raw distance and storing in list (maybe redundant, could do in run loop)
    for this_ai in Current_AI_List: 
        score.append(this_ai.delta_pos_sqrd)
        sum += score[i]    
        print("ai_num  ", this_ai.name)
        print("Score : ", score[i])
        i+=1
    i = 0
    sum =0
    max_score = max(score)
    # after finding max distance from all AI (the furthest distance) then subtract all AI distances off of the max
    for this_ai in Current_AI_List: 
        score[i] = max_score - score[i]
        sum += score[i]    
        i+=1
    i = 0

    #(max_distance - this_ai.distance) / (maxdis - ALL_ai_dist_summed) - this means the ai with the best score is weighted maissivly, and the ai with max distance gets 0
    for this_ai in Current_AI_List:
        this_ai.current_ratio = score[i]/(sum+.00001)
        ratio.append(this_ai.current_ratio)
        i +=1

    print(" ---------------------------------------------------------------- ")

    for j in range(len(ratio)):
        i=0
        total_sum = 0
        random_stat = random.uniform(0, 1)
        for i in range(len(ratio)):
            
            this_ai= Current_AI_List[i]
            if random_stat < ratio[i] + total_sum:
                if random_stat > total_sum:
                    this_ai.next_amnt_children +=1
                    To_Have_Children.append(copy.deepcopy(this_ai))
                    break
            else:
                total_sum += ratio[i]
            i+=1

    for this_ai in Current_AI_List:
                print("for: ", this_ai.name)
                print("ai children: ", this_ai.next_amnt_children)
    
    for this_ai in To_Have_Children:
        W_AB = copy.deepcopy(this_ai.W_AB)
        W_BC = copy.deepcopy(this_ai.W_BC)
        # Create a brand new instance so its functions are perfectly intact
        new_ai = ai(f"ai_{i}", 100, 100, 50, (70, 130, 180), W_AB, W_BC)
        ai.gaus_random(new_ai)
        # 3. Safely copy ONLY the numerical neural network weights/matrices
        # Change 'W_AB' to whatever the exact name of your weight matrix is inside your ai class!
        
        Children_list.append(new_ai)
    return Children_list

current_generation = AI_list
for generation in range(100):  # or while true with proper control
  run(current_generation)
  # After run() finishes, handle scoring and next generation creation:
  new_generation = score(current_generation)
  current_generation = new_generation


# 4. Clean exit when loop ends
pygame.quit()