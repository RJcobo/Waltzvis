import tkinter as tk
import subprocess
import sys
import settings
from PIL import Image, ImageTk

def choose_color():
    color_window = tk.Toplevel(root)
    color_window.title("Choose Color")
    color_window.configure(bg="black")

    chosen_color = tk.StringVar(value=settings.LINE_COLOR)
    # Only one color option: green
    colors = ["green"]

    for c in colors:
        tk.Radiobutton(
            color_window, 
            text=c.capitalize(), 
            variable=chosen_color, 
            value=c,
            font=("Consolas", 14, "bold"), 
            fg="white", 
            bg="black", 
            selectcolor="black",
            activebackground="gray"
        ).pack(anchor=tk.W, pady=5)

    def apply_color():
        settings.LINE_COLOR = chosen_color.get()
        color_window.destroy()

    tk.Button(
        color_window, 
        text="OK", 
        command=apply_color,
        font=("Consolas", 14, "bold"), 
        fg="white", 
        bg="black", 
        activebackground="gray"
    ).pack(pady=10)

def visualize():
    # Run the main script
    subprocess.Popen([sys.executable, "main.py"])

def config():
    config_window = tk.Toplevel(root)
    config_window.title("Configure Frequency Preset")
    config_window.configure(bg="black")

    # Define some preset ranges for low and high frequencies
    presets = [
        ("Low Band Emphasis", (200, 1500)),
        ("Default Range", (300, 2000)),
        ("High Band Emphasis", (400, 3000)),
        ("Ultra High Range", (500, 4000))
    ]

    chosen_preset = tk.IntVar(value=0)  # Default to the first preset
    for i, (label, (low_val, high_val)) in enumerate(presets):
        tk.Radiobutton(
            config_window, 
            text=label, 
            variable=chosen_preset, 
            value=i,
            font=("Consolas", 14, "bold"), 
            fg="white", 
            bg="black", 
            selectcolor="black",
            activebackground="gray"
        ).pack(anchor=tk.W, pady=5)

    def apply_config():
        index = chosen_preset.get()
        low_val, high_val = presets[index][1]
        settings.LOW_FREQ_MAX = low_val
        settings.HIGH_FREQ_MIN = high_val
        config_window.destroy()

    tk.Button(
        config_window, 
        text="OK", 
        command=apply_config,
        font=("Consolas", 14, "bold"), 
        fg="white", 
        bg="black", 
        activebackground="gray"
    ).pack(pady=10)

def exit_program():
    root.destroy()

root = tk.Tk()
root.title("Main Menu")
root.geometry("800x600")
root.configure(bg="black")

# If you have a background image, load and set it here
try:
    bg_img = Image.open("background.png")
    bg_img = bg_img.resize((800, 600), Image.ANTIALIAS)
    bg_photo = ImageTk.PhotoImage(bg_img)

    bg_label = tk.Label(root, image=bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
except:
    pass

button_font = ("Consolas", 14, "bold")

btn_color = tk.Button(root, text="Color", command=choose_color, font=button_font, fg="white", bg="black", activebackground="gray")
btn_color.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

btn_visualize = tk.Button(root, text="Visualize", command=visualize, font=button_font, fg="white", bg="black", activebackground="gray")
btn_visualize.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

btn_config = tk.Button(root, text="Config", command=config, font=button_font, fg="white", bg="black", activebackground="gray")
btn_config.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

btn_exit = tk.Button(root, text="Exit", command=exit_program, font=button_font, fg="white", bg="black", activebackground="gray")
btn_exit.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

root.mainloop()
