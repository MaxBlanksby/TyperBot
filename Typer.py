import pyautogui
import time
import random

def type_paragraph(paragraph, delay=0.1, accuracy=0.95):
    print("You have 5 seconds to focus on the Google Docs window.")
    time.sleep(5)

    for char in paragraph:
        if random.random() > accuracy:
           
            incorrect_char = paragraph[paragraph.index(char) + 1] if (paragraph.index(char) + 1 < len(paragraph)) else random.choice("abcdefghijklmnopqrstuvwxyz")
            pyautogui.write(incorrect_char)  
            time.sleep(delay) 
            pyautogui.press('backspace')  

        pyautogui.write(char)
        time.sleep(delay)  

if __name__ == "__main__":
    
    with open('Text.txt', 'r') as file:
        paragraph = file.read()

    type_paragraph(paragraph, delay=0.03, accuracy=0.8)
