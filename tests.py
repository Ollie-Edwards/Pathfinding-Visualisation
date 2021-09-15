
def completeTests():
    # not the best way of doing this
    
    AllFilesPresent = True
    
    try: import pygame
    except: 
        print("pygame is not installed")
        AllFilesPresent = False
    
    try: import math
    except:
        print("math library is not installed")
        AllFilesPresent = False
    
    try: import sys
    except:
        print("sys library is not installed")
        AllFilesPresent = False
    
    # IF ALL LIBRARIES ARE INSTALLED
    if AllFilesPresent == True:
        try: from Drawing import noSolutions
        except:
            print("Drawing.py does not exist")  
            AllFilesPresent = False  
        
        try: from NodeClass import Node
        except:
            print("NodeClass.py does not exist")
            AllFilesPresent = False
        
        try: from Colours import BLACK
        except:
            print("Colours.py does not exist")
            AllFilesPresent = False
        
    if AllFilesPresent == False:
        exit()
    else:
        print("Tests passed...")