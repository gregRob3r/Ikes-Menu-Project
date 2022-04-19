from selenium import webdriver as wd
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import PySimpleGUI as sg

layout = [[sg.Button("Restart")], [sg.Button("Quit")],[sg.Button("Yes")],[sg.Button("No")], [sg.Text("Input Here:"), sg.InputText(key = "input_box")], [sg.Submit(key = "sbmt")], [sg.Column([[sg.Text(key = "body",size = (100,100))]], scrollable = True, vertical_scroll_only = True)]]
window = sg.Window("Scroll up/down if you don't see anything in the text box!!", layout, finalize = True)

full_text = ""
user_input = ""

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
        global full_text
        full_text += "There are no sandwiches with these ingredients!\n"
        window["body"].update(full_text)
    return [final_list,final_desc] #in [0], there is the list of sandwiches; in [1], there is the list of descriptions for them.
                                   #name in [0][i] corresponds to the description in [1][i]

def check_event(event): #check the event passed through is quit or if the window was closed
    global window
    if(event == "Quit"):
        window.close()
    if(event == sg.WIN_CLOSED):
        window.close()

def print_menu(): #print the full menu of unique ingredients
    global full_text
    global window
    full_text = ""
    for i in all_ing:
        full_text += i+"\n"
    window["body"].update(full_text)
    
s = Service('./chromedriver')
driver = wd.Chrome(service = s)

#getting to the full menu page

driver.get("https://order.myguestaccount.com/menu/60902b7495b701063f8b4597?from_locations=1&appid=5ffe1d20adb0d57c1c96ada1")
driver.find_element(by = By.XPATH, value = "//*[@id='start-order-type']/div[1]/div[2]/button[1]").click()
if(int(current_time.split(':')[0]) >=9 and int(current_time.split(':')[0]) < 21): #This button only exists when they're open
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
    all_names_v1.append(i.text.title())
for i in descriptions:
    all_desc_v1.append(i.text.split('.')[0].title())

#process veg category
veg_btn.click()
names = driver.find_elements(by = By.TAG_NAME, value = 'h3')
descriptions = driver.find_elements(by = By.CLASS_NAME, value = "item-description")
for i in names:
    all_names_v1.append(i.text.title())
for i in descriptions:
    all_desc_v1.append(i.text.split('.')[0].title())
    
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
full_text += "Welcome to the Ike's Subway-ifier. These are all of the possible ingredients: \n\n"
for i in all_names_v1:#handle duplicate entries
    if i not in all_names:
        all_names.append(i)

for i in all_desc_v1:#handle duplicate entries
    if i not in all_desc:
        all_desc.append(i)
        
print_menu()

poss_iterations = [[]] #add iterations (print statement at the beginning of each iteration of ingredients
iterations = 0

full_text += "\nWhat would you like your first ingredient to be? Enter and hit 'Submit'\n"
window["body"].update(full_text)
event, value = window.read()
check_event(event)
    
while(event != "sbmt"):
    full_text += "Please enter an ingredient into the box and hit Submit"
    window["body"].update(full_text)
    event, value = window.read()
    check_event(event)

user_input = value["input_box"].title()
            
#all_ing        has all ingredients
#all_names      has all names of sandwiches, indeces linked with all_desc
#all_desc       had all descriptions of sandwiches, indeces linked with all_names
#ingredients loop
while(True):

    #get the user input for the next igredient
    if(iterations != 0): #all iterations after the first
        iterations += 1
        poss_iterations.append(poss_iterations[iterations-1].copy())
        full_text += "Current ingredients: "+str(poss_iterations[iterations])+"\n"
        full_text += "Current iteration: "+ str(iterations)+"\n"
        full_text += "\nWhat would you like your next ingredient to be? Click 'Yes' for a full list of ingredient\n"
        window["body"].update(full_text)
        #print stuff to user (above) and then read user input for ingredient (below)
        event, value = window.read()
        check_event(event)
        user_input = value["input_box"].title()
        if(event == "Yes"):
            print_menu()
    else:               #just the first iteration
        iterations += 1
        poss_iterations.append(poss_iterations[iterations-1].copy())
        
    #if the user doesn't input a valid ingredient
    while(user_input not in all_ing):
        full_text += "Please input a valid ingredient and hit 'Submit'. Hit 'Yes' to see the ingredients again\n"
        full_text += "Current ingredients: "+str(poss_iterations[iterations])+"\n"
        full_text += "Current iteration: "+str(iterations)+"\n"
        window["body"].update(full_text)
        event, value = window.read()
        check_event(event)
        user_input = value["input_box"].title()
        if(event == "Yes"):
            print_menu()
            
    #Checking if input is already in the list        
    if(user_input in poss_iterations[iterations]):
        full_text += "You've already entered that ingredient.\n"
        iterations -= 1
        window["body"].update(full_text)
        continue
    else:
        poss_iterations[iterations].append(user_input)
        full_text += "Excellent choice\n"
        window["body"].update(full_text)
    #After adding the new ingredient, asking if the user would like to see all the sandwiches possible?
    full_text += "Would you like to see your ingredient list/possible sandwiches? Hit 'Yes' or 'No'\n"
    window["body"].update(full_text)
    event, value = window.read()
    check_event(event)
    user_input = value["input_box"].title()
    while(event != "Yes" and event != "No"):#if invalid input
        full_text += "Please hit either 'Yes' or 'No'\n"
        window["body"].update(full_text)
        event, value = window.read()
        check_event(event)

    #The user would like to see the sandwiches, keep looking at them until the user doesn't want to (they hit "No") 
    if(event == "Yes"):
        while(True):
            full_text += "Your current ingredient list, iteration "+str(iterations)+" is:\n"#print relevant information
            full_text += str(poss_iterations[iterations])+"\n"
            full_text += "The sandwiches you can make with these ingredients are:\n"
            #finding the sandwiches with specified ingredients
            if(iterations == 1):#for the first ever iteration
                current_sandwiches = find_sandwiches(all_names, all_desc, poss_iterations[iterations], iterations-1)
                old_sand = current_sandwiches.copy()
            else:               #for all other iterations
                current_sandwiches = find_sandwiches(old_sand[0], old_sand[1], poss_iterations[iterations], iterations-1)
                old_sand = current_sandwiches.copy()

            #print all the sandwiches with the specified ingredients
            for i in range(len(current_sandwiches[0])):
                full_text += "( "+str(i)+" )"+str(current_sandwiches[0][i])+"\n"
            window["body"].update(full_text)
            
            #check if user wants more specific information on these sandwiches
            full_text += "For full sandwich stats, please enter a (#) and hit Submit.\nTo move on, hit 'No'.\n"
            window["body"].update(full_text)
            event, value = window.read()
            check_event(event)
            user_input = value["input_box"]
            #(user didn't give a valid input
            while(event != "No" and event != "sbmt" and (not user_input.isnumeric())):#if invalid input
                full_text += "TRY AGAIN. For full sandwich stats, please enter a (#) and hit Submit.\nIf not, hit 'No'.\n"
                event, value = window.read()
                check_event(event)
                user_input = value["input_box"]

            #if the user doesn't want to see sandwichs, get out of the while loop
            if(event == "No"):
                break
                
            #User wants more specific information, print it out
            if(event == "sbmt" and user_input.isnumeric()):
                full_text += "--------------------------------------------------------------------------------\n"
                full_text += str(current_sandwiches[0][int(user_input)])+" : "+str(current_sandwiches[1][int(user_input)])
                full_text += "\n--------------------------------------------------------------------------------\n"
                window["body"].update(full_text)
                continue

    else:
        if(iterations == 1):#for the first ever iteration
            current_sandwiches = find_sandwiches(all_names, all_desc, poss_iterations[iterations], iterations-1)
            old_sand = current_sandwiches.copy()
        else:               #for all other iterations
            current_sandwiches = find_sandwiches(old_sand[0], old_sand[1], poss_iterations[iterations], iterations-1)
            old_sand = current_sandwiches.copy()

    #after viewing sandwiches, see what the user wants to do next
    full_text = "\nQuit will end the program\nRestart if you'd like to restart\nYes to move on to the next ingredient.\n"
    window["body"].update(full_text)
    event, value = window.read()
    check_event(event)

    #user wants to restart (all other inputs handled at the top of the big while loop
    if(event == "Restart"):
        iterations = 0
        poss_iterations = [[]]
        full_text += "Restarting. What would you like your first ingredient to be? Hit 'Yes' to see a full list of ingredients.\n"
        window["body"].update(full_text)
        event, value = window.read()
        if(event == "Yes"): #user wants to see full menu
            print_menu()
        window["body"].update(full_text)
        while(event != "sbmt"):#user didn't input a valid input
            full_text += "Please enter an ingredient into the box and hit Submit. Hit 'Yes' to see a full list of ingredients.\n"
            window["body"].update(full_text)
            event, value = window.read()
            if(event == "Yes"):
                print_menu()

        user_input = value["input_box"].title()

window.close()
