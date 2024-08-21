import tkinter as tk
from tkinter import PhotoImage
from pygame import mixer
import speech_recognition as sr
import re

# Initialize mixer
mixer.init()

# Create window
root = tk.Tk()
root.title("SciFi Calculator")
root.configure(bg="#003366")
root.geometry("1050x550")

# Load the images
logo = PhotoImage(file=r"C:\Users\DELL\OneDrive\Desktop\Self Study\Personal Projects\1.Calculator(Done)\images\logo.png")
microphone_image = PhotoImage(file=r"C:\Users\DELL\OneDrive\Desktop\Self Study\Personal Projects\1.Calculator(Done)\images\microphone.png")

# Display the logo in a Label
logoLabel = tk.Label(root, image=logo, bg="#003366")
logoLabel.grid(row=0, column=0, sticky="w", padx=10)

# Entry field
entryField = tk.Entry(root, font=('Roboto', 24, 'bold'), bg='#003366', fg='white', bd=5, relief=tk.RAISED, width=40)
entryField.grid(row=0, column=1, columnspan=6, padx=10, pady=10)

# Function to handle button click
def click(button):
    current_text = entryField.get()
    entryField.delete(0, tk.END)
    entryField.insert(tk.END, current_text + button)

# Function to clear the entry field
def clear_entry():
    entryField.delete(0, tk.END)

# Function to clear the last character of the entry field
def clear_last_entry():
    current_text = entryField.get()
    if current_text:
        entryField.delete(len(current_text)-1, tk.END)

# Function to evaluate the expression
def evaluate():
    try:
        result = str(eval(entryField.get()))
        entryField.delete(0, tk.END)
        entryField.insert(tk.END, result)
    except Exception as e:
        entryField.delete(0, tk.END)
        entryField.insert(tk.END, "Error")
        root.after(2000, clear_entry)  # Clear entry after 2 seconds

# Function to process voice commands
def clickMic():
    mixer.music.load(r"C:\Users\DELL\OneDrive\Desktop\Self Study\Personal Projects\Calculator\audio\beep.mp3")
    mixer.music.play()
    
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            # Adjust for ambient noise and listen
            recognizer.adjust_for_ambient_noise(source, duration=0.2)
            print("Listening...")
            audio = recognizer.listen(source)
            query = recognizer.recognize_google(audio)
            print("You said:", query)
            
            # Map spoken words to mathematical operations
            expression = query.lower()
            expression = re.sub(r'\badd\b', '+', expression)
            expression = re.sub(r'\bsubtract\b', '-', expression)
            expression = re.sub(r'\bmultiply\b', '*', expression)
            expression = re.sub(r'\bdivide\b', '/', expression)
            expression = re.sub(r'\b(\d+)\s+and\s+(\d+)\b', r'\1 \2', expression)  # Replace "number and number" with "number number"
            expression = re.sub(r'\bminus\b', '-', expression)
            expression = re.sub(r'\binto\b', '*', expression)
            expression = re.sub(r'\btimes\b', '*', expression)
            expression = re.sub(r'\bcalculate sum of\b', '(', expression)
            expression = re.sub(r'\bplus\b', '+', expression)
            
            # Update entry field with parsed expression
            entryField.delete(0, tk.END)
            entryField.insert(tk.END, expression)
            
            # Evaluate the expression
            try:
                result = str(eval(expression))
                entryField.delete(0, tk.END)
                entryField.insert(tk.END, result)
            except Exception as e:
                entryField.delete(0, tk.END)
                entryField.insert(tk.END, "Error")
                root.after(2000, clear_entry)  # Clear entry after 2 seconds
            
            mixer.music.load(r"C:\Users\DELL\OneDrive\Desktop\Self Study\Personal Projects\Calculator\audio\music2.mp3")
            mixer.music.play()
        except sr.UnknownValueError:
            print("Could not understand audio")
            entryField.delete(0, tk.END)
            entryField.insert(tk.END, "Could not understand audio")
            root.after(2000, clear_entry)  # Clear entry after 2 seconds
        except sr.RequestError as e:
            print("Service error:", e)
            entryField.delete(0, tk.END)
            entryField.insert(tk.END, "Service error")
            root.after(2000, clear_entry)  # Clear entry after 2 seconds

# Microphone button for voice input
microphoneButton = tk.Button(root, image=microphone_image, bg="#003366", cursor="hand2", borderwidth=0, command=clickMic)
microphoneButton.grid(row=0, column=7, padx=10)

# Button layout
buttonTextList = ["C", "CE", "√", "+", "π", "cosθ", "tanθ", "sinθ", 
                  "1", "2", "3", "-", "2π", "cosh", "tanh", "sinh",
                  "4", "5", "6", "*", chr(8731), "x\u02b8", "x\u00B3", "x\u00B2",
                  "7", "8", "9", chr(247), "ln", "deg", "rad", "e",
                  "0", "%", "log₁₀", "(", ")", "x!", "="]

rowVal = 1
colVal = 0
for t in buttonTextList:
    if t == "C":
        button = tk.Button(root, text=t, width=8, height=3, bd=2, relief=tk.RAISED, bg='#66ccff', fg='white', font=('Roboto', 16, 'bold'), activebackground='#003366', command=clear_entry)
    elif t == "CE":
        button = tk.Button(root, text=t, width=8, height=3, bd=2, relief=tk.RAISED, bg='#66ccff', fg='white', font=('Roboto', 16, 'bold'), activebackground='#003366', command=clear_last_entry)
    elif t == "=":
        button = tk.Button(root, text=t, width=16, height=3, bd=2, relief=tk.RAISED, bg='#FFD700', fg='black', font=('Roboto', 16, 'bold'), activebackground='#003366', command=evaluate)
    else:
        button = tk.Button(root, text=t, width=8, height=3, bd=2, relief=tk.RAISED, bg='#66ccff', fg='white', font=('Roboto', 16, 'bold'), activebackground='#003366', command=lambda b=t: click(b))
    button.grid(row=rowVal, column=colVal, padx=1, pady=1)
    colVal += 1
    if colVal > 7:
        colVal = 0
        rowVal += 1

root.mainloop()
