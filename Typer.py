import sys
import tkinter as tk
from tkinter import scrolledtext, messagebox
import pyautogui
import time
import random
import threading
from pynput.keyboard import GlobalHotKeys

class TypingGUI:
    def __init__(self, master):
        self.master = master
        master.title("Auto Typer")
        master.attributes("-topmost", True)
        if sys.platform == 'darwin':
            hotkeys = {'<cmd>+<ctrl>+t': self.show_window}
            print("Press ⌘+Ctrl+T to show the Auto Typer")
        else:
            hotkeys = {'<ctrl>+<alt>+t': self.show_window}
            print("Press Ctrl+Alt+T to show the Auto Typer")

        self.hotkey_listener = GlobalHotKeys(hotkeys)
        self.hotkey_listener.start()
        # Text area for the paragraph
        self.text_area = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=60, height=20)
        self.text_area.pack(padx=10, pady=10)
        try:
            with open('Text.txt', 'r') as f:
                self.text_area.insert(tk.END, f.read())
        except FileNotFoundError:
            pass

        controls_frame = tk.Frame(master)
        controls_frame.pack(padx=10, pady=5)
        tk.Label(controls_frame, text="Delay (seconds)").grid(row=0, column=0, padx=5)
        self.delay_entry = tk.Entry(controls_frame, width=10)
        self.delay_entry.insert(0, "0.1")
        self.delay_entry.grid(row=0, column=1, padx=5)
        tk.Label(controls_frame, text="Accuracy (0–1)").grid(row=0, column=2, padx=5)
        self.acc_entry = tk.Entry(controls_frame, width=10)
        self.acc_entry.insert(0, "0.95")
        self.acc_entry.grid(row=0, column=3, padx=5)

        buttons_frame = tk.Frame(master)
        buttons_frame.pack(padx=10, pady=5)
        self.start_button = tk.Button(buttons_frame, text="Start", command=self.start_typing)
        self.start_button.grid(row=0, column=0, padx=5)
        self.stop_button = tk.Button(buttons_frame, text="Stop", command=self.stop_typing, state=tk.DISABLED)
        self.stop_button.grid(row=0, column=1, padx=5)

        self.stop_event = threading.Event()

    def bring_to_front(self):
        self.master.attributes("-topmost", True)
        self.master.lift()
        self.master.focus_force()

    def show_window(self):
        self.master.deiconify()
        self.bring_to_front()
        self.text_area.focus_set()

    def type_paragraph(self, paragraph, delay, accuracy):
        print("You have 5 seconds to focus the target window...")
        time.sleep(5)
        length = len(paragraph)
        for i, char in enumerate(paragraph):
            if self.stop_event.is_set():
                break
            if random.random() > accuracy:
                offset = random.randint(1, 3)
                future_idx = i + offset
                if future_idx < length:
                    typo_char = paragraph[future_idx]
                elif i + 1 < length:
                    typo_char = paragraph[i + 1]
                else:
                    typo_char = char
                pyautogui.write(typo_char)
                time.sleep(delay)
                pyautogui.press('backspace')
            pyautogui.write(char)
            time.sleep(delay)
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def start_typing(self):
        self.show_window()
        paragraph = self.text_area.get("1.0", tk.END)
        try:
            delay = float(self.delay_entry.get())
            accuracy = float(self.acc_entry.get())
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter numeric values for delay and accuracy.")
            return
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.stop_event.clear()
        threading.Thread(
            target=self.type_paragraph,
            args=(paragraph, delay, accuracy),
            daemon=True
        ).start()

    def stop_typing(self):
        self.stop_event.set()
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = TypingGUI(root)
    root.mainloop()
