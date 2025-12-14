import tkinter as tk
from tkinter import messagebox

# Function to calculate BMI and show positive message
def calculate_bmi():
    try:
        weight = float(weight_entry.get())
        height_cm = float(height_entry.get())

        if weight <= 0 or height_cm <= 0:
            messagebox.showwarning("Invalid Input", "Please enter numbers greater than zero.")
            return

        height_m = height_cm / 100
        bmi = weight / (height_m ** 2)

        # Decide BMI category and give positive message
        if bmi < 18.5:
            result = "Underweight"
            message = "You're lighter than average, but that doesn't define your strength. A balanced diet and mindful habits can help you feel your best!"
        elif bmi < 25:
            result = "Normal"
            message = "You're in a healthy range—great job! Keep up the good habits and stay active. Your body is doing amazing things every day."
        elif bmi < 30:
            result = "Overweight"
            message = "You're on a journey, and every step counts. Small changes can lead to big results. You're capable, strong, and worthy of feeling great!"
        else:
            result = "Obese"
            message = "Your body is unique, and your health journey is yours alone. Focus on progress, not perfection. You’ve got the power to make positive changes!"

        result_label.config(text=f"Your BMI is {bmi:.2f} — {result}\n\n{message}")
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers only.")

# Function to clear inputs
def clear_fields():
    weight_entry.delete(0, tk.END)
    height_entry.delete(0, tk.END)
    result_label.config(text="")
    weight_entry.focus()

# Create main window
window = tk.Tk()
window.title("Simple BMI Calculator")
window.geometry("400x300")
window.configure(bg="lightyellow")

# Weight input
tk.Label(window, text="Weight (kg):", bg="lightyellow", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5, sticky="w")
weight_entry = tk.Entry(window, font=("Arial", 12))
weight_entry.grid(row=0, column=1, padx=10, pady=5)
weight_entry.focus()
tk.Label(window, text="Enter your weight in kilograms", bg="lightyellow", font=("Arial", 8, "italic")).grid(row=1, column=1, sticky="w")

# Height input
tk.Label(window, text="Height (cm):", bg="lightyellow", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=5, sticky="w")
height_entry = tk.Entry(window, font=("Arial", 12))
height_entry.grid(row=2, column=1, padx=10, pady=5)
tk.Label(window, text="Enter your height in centimeters", bg="lightyellow", font=("Arial", 8, "italic")).grid(row=3, column=1, sticky="w")

# Buttons frame for better alignment
button_frame = tk.Frame(window, bg="lightyellow")
button_frame.grid(row=4, column=0, columnspan=2, pady=15)

tk.Button(button_frame, text="Calculate BMI", font=("Arial", 11), bg="green", fg="white", command=calculate_bmi).grid(row=0, column=0, padx=10)
tk.Button(button_frame, text="Clear", font=("Arial", 11), bg="red", fg="white", command=clear_fields).grid(row=0, column=1, padx=10)

# Result display
result_label = tk.Label(window, text="", bg="lightyellow", font=("Arial", 12), wraplength=350, justify="center")
result_label.grid(row=5, column=0, columnspan=2, pady=10)
window.mainloop()
