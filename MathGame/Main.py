"""
Name: Math Project

February 6th, 2023, AP Assignment
ICS-3UN

Code Targets:
- Offer Questions Serially based upon operators. Store data, and create new questions based upon weighted 'learning values' (Weighed creation is uncreated, currently generation is handled by user settings and rng)
- Store all question answers in a dictionary to use for weighting purposes (Currently only used for user analytics)
- Offer datasaving (Finished)
- Offer blacklisting/whitelisting certain operators (Completed)

Authors Notes:

- I feel like I added far too many comments? The code looks more green than code at this point. So unappealing.

- The user interface is NOT designed to be user friendly. If I wanted that I would've used fluent design or smth. It's just meant to add a layer of functionality over cml input

Credit:
- All code that is not written by me is noted down within the line's comment.
"""

# Dependencies

# To whoever is testing this, make sure you have np installed, it's the only one not included. Simply run 'pip install numpy'.
# tk is also required, should come preinstalled with most version of python, but on the odd chance you're on linux, your package manager should have in a repository... Probably...

import numpy as np
import tkinter as tk

import operator
import math
import random
import time
from os import path
import threading
import decimal
import time
import sys

# Developer Tools
Debug_Mode = False # Determines whether output messages are rerouted to the GUI.
GUI_Enabled = True # Determines whether the GUI is Enabled
Answer_Debug = False # Determines whether to print the answer string expected.
clean_strings = True # Whether strings are cleaned up to form more legible numbers


# Constants
file_name = 'data.npy' # The name of .npy file saved!
operators_available = ["ADD","SUB","MUL","DIV"] # Operators available to the program.
Sleep_Time = 0.1 # Time to wait between questions

operator_functions = {
    "ADD": operator.add,
    "SUB": operator.sub,
    "MUL": operator.mul,
    "DIV": operator.truediv
}

# Translates my OP_CODE naming to something more readeable. 
translation_layer = {
    "ADD":"+",
    "SUB":"-",
    "MUL":"x",
    "DIV":"÷"
}

# Variables
questions_asked = 0 # Session specific

data = {
'settings':{
    'num_operands':2,       # Number of operands in an equation
    'operators_allowed':[True,True,True,False],         # true false according to the operators_available table above
    'log_10':1,             # Determines the random number generator range. 10^x.
    'negatives':False,      # Determines whether negative numbers are included within questions
    'decimal_places':0      # Divides the random int by 10^x to create decimals, 0 is zero decimal places max, 1 is one and so on.
},
'questions':[]               # Used to store the history of the users questions to better predict what the best problem is to ask the user.
} #Primary Data Table for ALL data

def DeepCopyArray(array): # Quick function to ensure that when an array is destructively operated upon, the original array is not the same memory address of operated array.
    new_arr = []
    for i in array:
        new_arr.append(i)
    return new_arr
original_copy = dict(data)



# Data Loading Block
if path.exists(file_name): #Attempting to load a non-existent file will throw an error
    #if input('Data Save Found, would you like to start a new save? Enter y if you would: ') != "y": # This allowed for easier testing, since past saves are not checked for consistency with systems. Metadata could be used to solve for this
        data = dict(enumerate(np.load(file_name,allow_pickle=True).flatten(),1))[1] # This method to convert a npy array to a dictionary was sourced online.
        print("Data Save Loaded!") 
        
else:
    print("No save dats found. New Profile Created")
    np.save(file_name, data)  # Save the data



settings = data['settings']
questions_data = data['questions']


def stopgame():  # Write back to file after game has ended
    data['settings'] = settings # I'm not certain on whether if when creating the settings variable its the same memory address, or a clone is created as a seperate address, so I just sync them here.
    data['questions'] = questions_data

    np.save(file_name, data)  # Save the data
    exit() # Exits all running threads. Closes GUI and all that as well...


# ||    ||  ||||||||  #
# ||    ||     ||     #
# ||    ||     ||     # 
# ||    ||     ||     #
# ||||||||  ||||||||  #

window = tk.Tk()

window.title("Math Game v1.01 - Python")


# Button Functions 

def resetSettings():
    global settings
    settings = dict(original_copy['settings'])


def resetQuestions():
    global questions_data
    questions_data = []


def OperatorWindow():
    newWindow = tk.Toplevel(window)
    newWindow.title("Operations")

    newWindow.rowconfigure(0, minsize=50, weight=1)

    newWindow.columnconfigure(1, minsize=100, weight=1)

    def LocalizeFunction(i):
        def LocalFlip():
            settings['operators_allowed'][i] = not settings['operators_allowed'][i]
            if settings['operators_allowed'][i]:
                button.config(background='white')
            else:
                button.config(background='grey')
                
        button = tk.Button(newWindow,relief=tk.RAISED,text=" #   "+operators_available[i]+"   # ",command=LocalFlip,background='grey')  
        button.pack(anchor="w")

        if settings['operators_allowed'][i]:
            button.config(background='white')


    for i in range(len(operators_available)):
        LocalizeFunction(i)

            
        
        
    

def SettingsWindow():
    newWindow = tk.Toplevel(window)
    newWindow.title("Settings - Math Game v0.03")

    newWindow.rowconfigure(0, minsize=50, weight=1)

    newWindow.columnconfigure(1, minsize=100, weight=1)

    amount_frm = 1
    
    frame = tk.Text(newWindow, relief=tk.RAISED,background="white",height=1)
    frame.grid(row=0, column=0, sticky="ew", padx=5, pady=2)

    frame.insert("1.0","// SETTINGS SECTION")
    frame.config(state=tk.DISABLED)
    frame.grid(row=0, column=0, sticky="ew", padx=5, pady=2)

    button = tk.Button(frame,relief=tk.RAISED,command=resetSettings,text="[Reset Settings]")
    button.pack(anchor="e")
    for SettingName in settings:
        frame = False # Named Variable first.
        setting_Name = SettingName # Create a localized value for SettingName as the variable settingName is changed as the loop continues.

        if setting_Name == "operators_allowed":
            frame = tk.Button(newWindow, relief=tk.RAISED,background="white",height=1,text="//                                                  "+SettingName,command=OperatorWindow)
        else:
            frame = tk.Text(newWindow, relief=tk.RAISED,background="white",height=2)
            frame.insert("1.0","// "+SettingName)
            frame.config(state=tk.DISABLED)


        frame.grid(row=amount_frm, column=0, sticky="ew", padx=5, pady=2)

        SettingDT = str(type(settings[SettingName]))[8:-2] # The individiual settings data type
        
        amount_frm+=1
        def LocalizeTextCreator(setting_Name):
            text_local = False
            def Apply():
                if text_local.get().isnumeric():
                    settings[setting_Name] = int(text_local.get())
                else:
                    text_local.delete(0,50)
                    text_local.insert("0",str(settings[setting_Name]))
            text_local = tk.Entry(frame,relief=tk.RAISED)
            text_local.pack(anchor="e")
            text_local.insert(0,str(settings[setting_Name]))

            activate = tk.Button(frame,relief=tk.RAISED,command=Apply,text="Set")
            activate.pack(anchor="e") 



        if SettingDT=='bool':
            button_local = False # So that type safe passes this. I hate python sm sm

            def BooleanFlip(): # Bad practice since this function will only be used for this window, hopefully the garbage collector for python is efficient.
                # The reason I require this function though is because the variable setting_Name can't be carried outside, since I don't know how to add parameters in tkinter.
                settings[setting_Name] = not settings[setting_Name]
                button_local.config(text = "["+ str(settings[setting_Name])+"]")
            button_local = tk.Button(frame,relief=tk.RAISED,command=BooleanFlip,text="["+ str(settings[setting_Name])+"]")
            button_local.pack(anchor="e")
        elif SettingDT=="int":
            LocalizeTextCreator(SettingName)
            

def ThreadSettings():
    thread = threading.Thread(target=SettingsWindow, daemon=True)
    thread.start()

def ThreadAnalytics():
    thread = threading.Thread(target=AnalyticsWindow, daemon=True)
    thread.start()
    
# This function indexes through all past questions, applies a filter to make sure they apply to the requested filter, then collects and combines the data to create analytics.
def analyticsFind(operators=[],negatives=0,decimals=0,magnitude=0):
    question_times = []
    correct = 0
    incorrect = 0
    for question in questions_data:
        fits = True

        # Filtering
        for i in question['operators']:
            for a in operators:
                if a == i:
                    break
                fits = False
        for i in question['operands']: 
            if negatives == True:
                if i<0:
                    fits = False
            if int(math.log10(i)) != magnitude-1 and magnitude != 0:
                fits = False
            if abs(decimal.Decimal( str(i).rstrip('0')).as_tuple().exponent) == decimals and decimals != 0:
                fits = False
        
        # Append to dataset
        if fits:
            if question['correct']:
                correct += 1
                question_times.append(question['time_spent'])
            else:
                incorrect += 1
    
    # Return a filtered dataset.
    return math.floor(np.average(question_times)*100)/100, correct,incorrect,correct+incorrect,str(np.floor((correct/(correct+incorrect))*1000)/10)+"%"


# This is a high level control function that creates the user interface for the analytics window.    

viewing = "all" # Utilized within the Analytics Window for checking Current or not Current

def OperatorCompatabilityLayer():
    newTab = []
    for i in range(len(settings['operators_allowed'])):
        if settings['operators_allowed'][i]:
            newTab.append(operators_available[i])

    return newTab


def AnalyticsWindow():
    newWindow = tk.Toplevel(window)
    newWindow.title("Analytics - Math Game v0.03")

    newWindow.rowconfigure(0, minsize=50, weight=1)

    newWindow.columnconfigure(1, minsize=100, weight=1)

    

    newWindow.rowconfigure(0, minsize=50, weight=1)

    newWindow.columnconfigure(1, minsize=100, weight=1)

    # Sort all analytics into defining properties. View correct questions, incorrect questions, total questions, average time for question.
    average_time,correct,incorrect,total,percentage = analyticsFind()
    average_time_1,correct_1,incorrect_1,total_1,percentage_1 = analyticsFind(OperatorCompatabilityLayer(),settings['negatives'],settings['decimal_places'],settings['log_10']) # Analytics of currently applied settings.
    
    # User interface generation
    frame = tk.Text(newWindow, relief=tk.RAISED,background="white",height=1)
    frame.grid(row=0, column=0, sticky="ew", padx=5, pady=2)

    frame.insert("1.0","// ANALYTICS")
    frame.config(state=tk.DISABLED)
    frame.grid(row=0, column=0, sticky="ew", padx=5, pady=2)

    button = tk.Button(frame,relief=tk.RAISED,command=resetQuestions,text="[Wipe Data]")
    button.pack(anchor="e")

    
    frame1 = tk.Text(newWindow, relief=tk.RAISED,background="white",height=2)
    frame1.insert("1.0","Average Time: "+str(average_time))
    frame1.config(state=tk.DISABLED)
    frame1.grid(row=2, column=0, sticky="ew", padx=5, pady=2)


    frame2 = tk.Text(newWindow, relief=tk.RAISED,background="white",height=2)
    frame2.insert("1.0","Accuracy: "+str(percentage))
    frame2.config(state=tk.DISABLED)
    frame2.grid(row=3, column=0, sticky="ew", padx=5, pady=2)

    frame3 = tk.Text(newWindow, relief=tk.RAISED,background="white",height=2)
    frame3.insert("1.0","Total Questions: "+str(total))
    frame3.config(state=tk.DISABLED)
    frame3.grid(row=4, column=0, sticky="ew", padx=5, pady=2)
    def Redraw():
        global viewing

        if viewing == "all":
            viewing = "notall"

            frame1.config(state=tk.NORMAL)
            frame2.config(state=tk.NORMAL)
            frame3.config(state=tk.NORMAL)

            frame1.delete("1.0","50.0")
            frame2.delete("1.0","50.0")
            frame3.delete("1.0","50.0")
            frame1.insert("1.0","Average Time: "+str(average_time_1))
            frame2.insert("1.0","Accuracy: "+str(percentage_1))
            frame3.insert("1.0","Total Questions: "+str(total_1))

            
            frame1.config(state=tk.DISABLED)
            frame2.config(state=tk.DISABLED)
            frame3.config(state=tk.DISABLED)
        else:
            viewing = "all"
            
            
            frame1.config(state=tk.NORMAL)
            frame2.config(state=tk.NORMAL)
            frame3.config(state=tk.NORMAL)

            frame1.delete("1.0","50.0")
            frame2.delete("1.0","50.0")
            frame3.delete("1.0","50.0")
            frame1.insert("1.0","Average Time: "+str(average_time))
            frame2.insert("1.0","Accuracy: "+str(percentage))
            frame3.insert("1.0","Total Questions: "+str(total))
            
            frame1.config(state=tk.DISABLED)
            frame2.config(state=tk.DISABLED)
            frame3.config(state=tk.DISABLED)
    
    button_local = tk.Button(frame,relief=tk.RAISED,command=Redraw,text="[View Current Setting/All Questions]")
    button_local.pack(anchor="e")


# Similar to threading settings, this ensures that the main thread does not halt if the analytics Window has a bug.
# TK also just seems to halt the proccess, its not simultaneous by default?


# Main Window Creation

window.rowconfigure(0, minsize=300, weight=1)

window.columnconfigure(1, minsize=200, weight=1)

txt_edit = tk.Frame(window)

frm_buttons = tk.Frame(window, relief=tk.RAISED, bd=2)

btn_set = tk.Button(frm_buttons, text="Settings",command=ThreadSettings)

btn_ana = tk.Button(frm_buttons, text="Analytics",command=ThreadAnalytics)

btn_exi = tk.Button(frm_buttons, text="Exit",command=stopgame)


btn_set.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

btn_ana.grid(row=1, column=0, sticky="ew", padx=5,pady=5)

btn_exi.grid(row=2, column=0, sticky="ew", padx=5,pady=5)


frm_buttons.grid(row=0, column=0, sticky="ns")

txt_edit.grid(row=0, column=1, sticky="nsew")

text_lab = tk.Text(txt_edit,width=150,height=15, bg="white",fg="black",relief=tk.SUNKEN)
text_lab.grid(row=0,column=0,sticky="ew",padx=5)
text_lab.config(state=tk.DISABLED)

enter = tk.Entry(txt_edit,width=150,bg="white",fg="black",relief=tk.RIDGE)
enter.grid(row=1,column=0,sticky="ew",padx=5,pady=5)


#   ||      ||||||  ||||||  ||||||  ||||||  #
#   ||      ||  ||  ||        ||    ||  ||  #
#   ||      ||  ||  || |||    ||    ||      #
#   ||      ||  ||  ||  ||    ||    ||  ||  #
#   ||||||  ||||||  ||||||  ||||||  ||||||  #



# Detects Enter Key Press
enter_key = False

def enter_bind(event):
    global enter_key
    enter_key = True
window.bind('<Return>', enter_bind)



# 
character_space = 0
def redirector(inputStr):
    text_lab.config(state=tk.NORMAL)
    global character_space
    character_space += 1
    text_lab.insert(str(character_space)+".0",inputStr)
    text_lab.config(state=tk.DISABLED)


sys_write = sys.stdout.write # in case I want to use terminal prints for debugging while keeping the application.
if not Debug_Mode:
    sys.stdout.write = redirector

# RNG for the values that will be operated upon. Input of the settings table. The settings table is an input because it is a user controlled table.
def OperandGen():
    log_val = settings['log_10']         # Digits
    dec_val = settings['decimal_places'] # Decimal Values
    neg     = settings['negatives']      # Is Negative

    max_val = 10**(log_val+dec_val)
    integer = 0
    while integer == 0:
        if neg:
            integer = random.randint(-max_val,max_val)/(10**dec_val) # Random Number between negative max and positive max

        else:
            integer = random.randint(0,max_val)/(10**dec_val)         # Random number between 0 and positive max
    return integer


def correct_decimals(num_string:str): # Python generally prints numbers with a digit (e.g 5.0 instead of 5)
    if not clean_strings:
        return num_string
    while num_string.endswith("0") and len(num_string)!=1 and num_string.find(".")!=-1: 
        num_string = num_string[0:len(num_string)-2]
    if num_string.endswith("."):
        num_string = num_string[0:len(num_string)-2]
    if num_string == "-0":
        num_string = "0"
    return num_string


# Calculates a solution based upon the values and operators given.
def CalculateAnswer(values_memadd,ops_memadd):
    values = DeepCopyArray(values_memadd) # Since this function is destructive on the parameters, I want to make sure that it's not operating on the arrays mem values within the class, so I made a unique mem_add cloned array
    ops = DeepCopyArray(ops_memadd)
    if len(values)-len(ops) != 1: # There must always be exactly one more operand than operator as each operator must go between 2 operands.
        print('Invalid Data to Calculate Answer')
        exit()

    # The specific order of solving is set up to follow order of operations
    # It essentially works be operating on the two values besides a matching operator, then
    # Replacing all 3 values with 1 value
    
    # Multiplication/Division Loop
    end = False
    while not end:
        counter = 0 # I hate this, why can you not unpack 2 values in the for loop, why is there no counter value built into python?
        broken = False
        for i in ops:
            if i == "MUL" or i == "DIV":
                a = values[counter]
                b = values[counter+1]
                ops.pop(counter)
                values[counter] = operator_functions[i](a,b) # Operator function because it's easier than converting the string to a operator using 4 if/else statements.
                values.pop(counter+1) # Should shift up the list.
                broken = True
                break #Must break the for loop, because the list has been restructured.
            # if it reached here that means that none of the operators are of the specified type anymore, therefore the while can end.
            counter += 1
        if not broken:
            end = True

    
    # Addition/Subtraction Loop
    end = False
    while not end:
        counter = 0
        broken = False
        for i in ops:
            if i == "ADD" or i == "SUB":
                a = values[counter]
                b = values[counter+1]
                ops.pop(counter)
                values[counter] = operator_functions[i](a,b) # Operator function because it's easier than converting the string to a operator using 4 if/else statements.
                values.pop(counter+1) # Should shift up the list.
                broken = True
                break #Must break the for loop, because the list has been restructured.
             # if it reached here that means that none of the operators are of the specified type anymore, therefore the while can end.
            counter += 1
        if not broken:
            end = True

    solution = values[0]

    # Sometimes the solution has a FP error.
    solution = math.floor(solution* (10**settings['decimal_places']))/(10**settings['decimal_places']) # This makes it precisely the amount of deceimals in the decimal place specified value.


    return solution


# Class that will be used in the datasaving.
class Question:
    def __init__(self, values, ops):
        self.operators = ops
        self.operands = values


        self.answer = correct_decimals(str(CalculateAnswer(values,ops)))
        self.time_spent = 0
        self.correct = False
        formed_equation = ""
        for i in range(len(ops)):
            formed_equation = formed_equation+correct_decimals(str(values[i]))+" "
            formed_equation = formed_equation+translation_layer[ops[i]]+ " "
        formed_equation = formed_equation+ correct_decimals(str(values[len(values)-1]))
        self.Equation = formed_equation


def GenerateQuestion ():
    operands = []
    operators = []

    for i in range(settings['num_operands']-1): # -1 because it adds a operand after loop
        # Generate Operator
        allowed = OperatorCompatabilityLayer()
        operators.append( allowed[random.randint(0,len(allowed)-1)] )

        # Generate Operand
        operands.append(OperandGen())
    
    operands.append(OperandGen()) # One more operand than operator

    return Question(operands,operators)
    

def InputFunction(Question):
    if Debug_Mode:
        return input(Question)
    else:
        enter.focus_set()
        global enter_key
        while not enter_key:
            time.sleep(0.1)
        string  = enter.get()
        enter.delete(0,100)
        enter_key = False
        return correct_decimals(string)

def QuestionWindowThread():
    while True:
        global questions_asked

        # Take care of GUI Print stuff
        if GUI_Enabled:
            character_space = 0 
            text_lab.config(state=tk.NORMAL)
            text_lab.delete("1.0","10.0")                
            text_lab.config(state=tk.DISABLED)

        questions_asked += 1
        print("[ QUESTION "+str(questions_asked)+"]")
        print("Generating Question....."," ")
        question = GenerateQuestion()
        
        timestamp = time.time()

        print(question.Equation)
        if Answer_Debug:
            print(question.answer)
        plr_ans = InputFunction("What is the answer?")
        if plr_ans == question.answer:
            print("Correct")
            question.correct = True
            question.time_spent = math.floor((time.time()-timestamp)*100)/100
        else:
            print("Incorrect")
            question.correct = False
        
        questions_data.append(question.__dict__) # Converts the Class into an array. NESSECARY due to JSON and saving complexities
        time.sleep(Sleep_Time)

# Start the question thread
question_thread = threading.Thread(target=QuestionWindowThread, daemon=True)
question_thread.start()

if Debug_Mode:
    print("Passed Question Threading Start! :D")

if GUI_Enabled:
    if Debug_Mode:
        print("GUI Being Drawn")
    window.mainloop()
else:
    while 1: # Prevents threads from ending when main thread reaches end in the case that there is no window loop running.
        time.sleep(1)

