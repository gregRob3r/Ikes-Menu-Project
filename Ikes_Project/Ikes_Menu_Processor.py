from selenium import webdriver as wd
from datetime import datetime
from selenium.webdriver.common.by import By
import time

now = datetime.now()
current_time = str(now.strftime("%H:%M:%S"))

def find_sandwiches(sammy_list, desc_list, ing_list, iterations):#we know that all ingredients in ing_list are possible ingredients
    final_list = []
    final_desc = []
    for j in desc_list:
        if ing_list[iterations] in j:
            if j not in final_desc:
                final_list.append(sammy_list[desc_list.index(j)])
                final_desc.append(j)
                
    if (len(final_list) == 0):
        print("There are no sandwiches with these ingredients!")
    return [final_list,final_desc]

driver = wd.Chrome('./chromedriver')

#getting to the full menu page

driver.get("https://order.myguestaccount.com/menu/60902b7495b701063f8b4597?from_locations=1&appid=5ffe1d20adb0d57c1c96ada1")
driver.find_element(by = By.XPATH, value = "//*[@id='start-order-type']/div[1]/div[2]/button[1]").click()
if(int(current_time.split(':')[0]) >= 10 and int(current_time.split(':')[0]) < 21): #This button only exists when they're open
    driver.find_element(by = By.XPATH, value = "//*[@id='start-order-time-info']/div[2]/button[1]").click()
driver.find_element(by = By.XPATH, value = "//*[@id='start-order']").click()

#items for the three main category buttons we want to search through sandwiches for
meat_btn = driver.find_element(by = By.XPATH, value = "//*[@id='category_list']/li[1]/ul/li[1]/a")
veg_btn = driver.find_element(by = By.XPATH, value = "//*[@id='category_list']/li[1]/ul/li[2]/a")
kid_btn = driver.find_element(by = By.XPATH, value = "//*[@id='category_list']/li[1]/ul/li[3]/a")

#variables to contain all of the names and descriptions of all menu items (indeces correlate with each other)
all_names_v1 = []
all_names = []
all_desc_v1 = []
all_desc = []

#process meat category
meat_btn.click() #click into meat category
names = driver.find_elements(by = By.TAG_NAME, value = 'h3')
descriptions = driver.find_elements(by = By.CLASS_NAME, value = "item-description")
for i in names:
    all_names_v1.append(i.text)
for i in descriptions:
    all_desc_v1.append(i.text.split('.')[0])

#process veg category
veg_btn.click()
names = driver.find_elements(by = By.TAG_NAME, value = 'h3')
descriptions = driver.find_elements(by = By.CLASS_NAME, value = "item-description")
for i in names:
    all_names_v1.append(i.text)
for i in descriptions:
    all_desc_v1.append(i.text.split('.')[0])
    
driver.quit() #done taking in data

#remove white spaces
all_names_v1 = [x for x in all_names_v1 if x]
all_desc_v1 = [x for x in all_desc_v1 if x]

#process all descriptions into a list of ingredients, pretty nuch just removing duplicates, formatting, etc.
all_ing = []
count = 0
for i in all_desc_v1:
    ingredients = i.split(',')
    for j in ingredients:
        if j.strip() not in all_ing:
            all_ing.append(j.strip())

#at this point, I think we're good. We have a list of all ingredients, and all items and their descriptions are
#mapped to the same indeces ***in separate arrays***
print("Welcome to the Ike's Subway-ifier. These are all of the possible ingredients: \n")
for i in all_names_v1:#handle duplicate entries
    if i not in all_names:
        all_names.append(i)

for i in all_desc_v1:#handle duplicate entries
    if i not in all_desc:
        all_desc.append(i)
        
for i in all_ing:
    print(i)

poss_iterations = [[]] #add iterations (print statement at the beginning of each iteration of ingredients
iterations = 0
user_input = input("What would you like your first ingredient to be? (-1 to exit)\n").title()
            
#all_ing        has all ingredients
#all_names      has all names of sandwiches, indeces linked with all_desc
#all_desc       had all descriptions of sandwiches, indeces linked with all_names
#ingredients loop
while(user_input != "-1"):
    if(user_input == "r"):#giving the user a chance to restart
        iterations = 0
        poss_iterations = [[]]
        user_input = input("What would you like your first ingredient to be?\n").title()
        
    if(iterations != 0): #user input at the top of each loop all but the first time when asking for next ingredient
        print("--------------------------------------------------------------------------------")
        iterations += 1
        poss_iterations.append(poss_iterations[iterations-1].copy())
        print("Current ingredients:",poss_iterations[iterations])
        print("Current iteration:",iterations)
        user_input = input("What would you like your next ingredient to be?\n").title()
    else:
        iterations += 1
        poss_iterations.append(poss_iterations[iterations-1].copy())
        
    #Checking if the input is a valid ingredient
    while(user_input not in all_ing):
        user_input = input("Please input a valid ingredient. Enter 'm' to see the menu of ingredients again\n").title()
        print("Current ingredients:",poss_iterations[iterations])
        print("Current iteration:",iterations)
        if(user_input == "m" or user_input == "M"):
            for i in all_ing:
                print(i)

    #Checking if input is already in the list        
    if(user_input in poss_iterations[iterations]):
        print("You've already entered that ingredient.")
        continue
    else:
        poss_iterations[iterations].append(user_input)
        print("Excellent choice")

    #After adding the new ingredient, asking if the user would like to see all the sandwiches possible?
    user_input = input("Would you like to see your ingredient list/possible sandwiches? (y/n)\n")
    while(user_input != "Y" and user_input != "y" and user_input != "N" and user_input != "n"):#if invalid input
        user_input = input("Please enter either a 'y' or a 'n'")

    #The user would like to see the sandwiches    
    if(user_input == "Y" or user_input == "y"):
        stay = True
        while(stay):
            print("Your current ingredient list, iteration",iterations,"is:")#print relevant information
            print(poss_iterations[iterations])
            print("The sandwiches you can make with these ingredients are:")
            if(iterations == 1):
                current_sandwiches = find_sandwiches(all_names, all_desc, poss_iterations[iterations], iterations-1)
                old_sand = current_sandwiches.copy()
            else:
                current_sandwiches = find_sandwiches(old_sand[0], old_sand[1], poss_iterations[iterations], iterations-1)
                old_sand = current_sandwiches.copy()
                
            for i in range(len(current_sandwiches[0])):
                print("(",i,")",current_sandwiches[0][i])

            #Check if user wants more specific information on these sandwiches
            user_input = input("If you want a closer look at sandwich, please enter a #, where (#) are next to the sandwich names.\nIf not, please enter 'n'.\n")
            while(user_input != 'n' and user_input != 'N' and (not user_input.isnumeric())):#if invalid input
                user_input = input("Try again. Enter a #, where (#) are next to the sandwich names.\nIf not, please enter 'n'.\n")
                
            #User wants more specific information
            if(user_input.isnumeric()):
                print("--------------------------------------------------------------------------------")
                print(current_sandwiches[0][int(user_input)],":",current_sandwiches[1][int(user_input)])
                print("--------------------------------------------------------------------------------")
                continue
            else:#customer wants out of the while loop
                stay = False
    #What are we doing next
    user_input = input("\nPossible Commands:\n'-1' will end the program\n'r' if you'd like to restart\nEnter anything else if you want to add your next ingredient.\n")

print("ENDING")#Final print statement before the program ends
