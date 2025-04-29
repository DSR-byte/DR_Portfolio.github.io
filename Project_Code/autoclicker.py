"""#!/usr/bin/env python3
# -*- coding: utf-8 -*-


Created on Tue Dec 24 22:54:47 2024

@author: davidrock
"""
from pynput.mouse import Button, Controller
import time
from threading import Thread
from Quartz import CGEventSourceButtonState, kCGMouseButtonLeft, kCGEventSourceStateHIDSystemState

# ///////////////////////////////////////////////////////////////

mouse = Controller() # declares mouse as a class of controller 

running = True # is a gllobal variabel to tell the clicking while loop weather to be on or not

programed_click = False # a flag to know if the clicks are vitual

clicking = False  # serves two puposes one to stop the while loop form seasing up and to only start clicking if the mous is down

press_time = 0




# ///////////////////////////////////////////////////////////////  

# ///////////////////////////////////////////////////////////////   
def is_left_button_pressed():
    #print("ispressed")
    # Check the state of the left mouse button
    return CGEventSourceButtonState(kCGEventSourceStateHIDSystemState, kCGMouseButtonLeft)

# ///////////////////////////////////////////////////////////////

# ///////////////////////////////////////////////////////////////  
def click():
    #print("click")
    global clicking, programed_click,press_time
    
    if programed_click:
        return
    if is_left_button_pressed():
        if not clicking:  # Detect the start of a new press
            press_time = time.time()  # Set press time only once
        clicking = True  # Set flag to True when the button is pressed
    else:
        clicking = False  # Set flag to False when the button is released
        press_time = 0

# ///////////////////////////////////////////////////////////////

# ///////////////////////////////////////////////////////////////

# Simulate `while clicked` functionality
def click_while_pressed():
    global clicking, programed_click, press_time
    
    while running:
        click()
        if clicking:
            elapsed_time = time.time() - press_time
            if elapsed_time >= 0.4:  
                print(elapsed_time)
                programed_click = True
                print("programable click")
                mouse.release(Button.left)
                mouse.press(Button.left)
                time.sleep(0.4)        
                programed_click = False
                print("programable click false")    
                
                
# ///////////////////////////////////////////////////////////////


# ///////////////////////////////////////////////////////////////

try:   
   click_while_pressed()
   



     
except KeyboardInterrupt:
    # Handle manual interruption (Ctrl+C) gracefully
    print("Exiting...")

finally:

    
    # Signal threads to stop
    running = False
    print("Program terminated.")

    