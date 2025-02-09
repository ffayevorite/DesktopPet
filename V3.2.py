import tkinter as tk
import os
import random
from platform import system

def resource_path(relative_path):
    """Get the absolute path to the resource."""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class Pet:

    def __init__(self):
        self.root = tk.Tk()  # create window
        self.delay = 200  # delay in ms
        self.pixels_from_right = 500  # change to move the pet's starting position
        self.pixels_from_bottom = 130  # change to move the pet's starting position
        self.normal_speed = 6  # normal movement speed
        self.follow_speed = 50  # faster speed when following the mouse
        self.move_speed = self.normal_speed  # current movement speed
        self.follow_mouse = False  # Initialize follow_mouse flag
        self.current_direction = random.choice(['left', 'right'])  # Initial direction (only left or right)
        self.follow_mouse_chance = 0.01  # 1% chance to follow the mouse
        self.idle_chance = 0.1  # 10% chance to go idle
        self.sleep_chance = 0.05  # 5% chance to sleep
        self.idle_duration = 3000  # 3 seconds in idle state
        self.sleep_duration = 5000  # 5 seconds in sleep state
        self.current_state = 'idle'  # Initial state

        # initialize frame arrays
        self.animation = {
            'idle': [tk.PhotoImage(file=r"D:\my_project\desktop_pet\Stay.gif", format='gif -index %i' % i) for i in range(4)],
            'sleep': [tk.PhotoImage(file=r"D:\my_project\desktop_pet\Nap.gif", format='gif -index %i' % i) for i in range(4)] * 3,
            'walk_left': [tk.PhotoImage(file=r"D:\my_project\desktop_pet\WalkGifR.gif", format='gif -index %i' % i) for i in range(2)],
            'walk_right': [tk.PhotoImage(file=r"D:\my_project\desktop_pet\WalkGifL.gif", format='gif -index %i' % i) for i in range(2)]
        }

        # Debug: Check if GIFs are loaded
        print("Loaded animations:", self.animation.keys())

        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)
        self.root.wm_attributes('-transparentcolor', 'black')

        self.label = tk.Label(self.root, bd=30, bg='black')
        self.label.pack()

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.min_width = 100
        self.max_width = screen_width - 110
        self.min_height = 100
        self.max_height = screen_height - 110

        self.curr_width = screen_width - self.pixels_from_right
        self.curr_height = screen_height - self.pixels_from_bottom
        self.root.geometry(f'100x100+{self.curr_width}+{self.curr_height}')

        self.root.bind("<Button-1>", self.on_left_click)
        self.root.bind("<Button-2>", self.on_right_click)
        self.root.bind("<Button-3>", self.on_right_click)

    def update(self, i, curr_animation):
        self.root.attributes('-topmost', True)
        animation_arr = self.animation[curr_animation]
        frame = animation_arr[i % len(animation_arr)]  # Use modulo to loop through frames
        self.label.configure(image=frame)

        # Randomly decide whether to follow the mouse
        if random.random() < self.follow_mouse_chance:  # 1% chance to follow the mouse
            self.follow_mouse = True
            self.move_speed = self.follow_speed  # Increase speed when following the mouse

        if self.follow_mouse:
            reached_mouse = self.follow_mouse_cursor()  # Move the pet towards the mouse cursor
            if reached_mouse:
                self.follow_mouse = False  # Stop following the mouse
                self.move_speed = self.normal_speed  # Reset speed to normal
                curr_animation = 'idle'  # Change to idle animation
        else:
            if self.current_state == 'idle':
                # Stay idle for a while
                self.root.after(self.idle_duration, self.change_state, 'walk')
            elif self.current_state == 'sleep':
                # Stay asleep for a while
                self.root.after(self.sleep_duration, self.change_state, 'walk')
            else:
                self.move_around_screen()  # Move the pet around the screen

        # Update animation based on current state and direction
        if self.current_state == 'walk':
            if self.current_direction == 'left':
                curr_animation = 'walk_left'
            elif self.current_direction == 'right':
                curr_animation = 'walk_right'
        elif self.current_state == 'idle':
            curr_animation = 'idle'
        elif self.current_state == 'sleep':
            curr_animation = 'sleep'

        i += 1
        self.root.after(self.delay, self.update, i, curr_animation)

    def change_state(self, new_state):
        """Change the current state of the pet."""
        self.current_state = new_state
        if new_state == 'idle':
            self.idle_chance = 0.1  # Reset idle chance
        elif new_state == 'sleep':
            self.sleep_chance = 0.05  # Reset sleep chance

    def on_left_click(self, event):
        print("Detected left click")

    def on_right_click(self, event):
        self.quit()

    def move_around_screen(self):
        if self.current_state == 'walk':
            if self.current_direction == 'left':
                if self.curr_width > self.min_width:
                    self.curr_width -= self.move_speed
                else:
                    self.current_direction = 'right'  # Change direction to right
            elif self.current_direction == 'right':
                if self.curr_width < self.max_width:
                    self.curr_width += self.move_speed
                else:
                    self.current_direction = 'left'  # Change direction to left

            # Keep the y position fixed at 130
            self.curr_height = 950

            # Randomly decide to go idle or sleep
            if random.random() < self.idle_chance:
                self.current_state = 'idle'
            elif random.random() < self.sleep_chance:
                self.current_state = 'sleep'

            # Update the pet's position
            self.root.geometry(f'100x100+{self.curr_width}+{self.curr_height}')

    def follow_mouse_cursor(self):
        # Get the current mouse position
        mouse_x = self.root.winfo_pointerx()
        mouse_y = self.root.winfo_pointery()

        # Calculate the difference between the pet's position and the mouse position
        delta_x = mouse_x - self.curr_width

        # Check if the pet has reached the mouse in the x-axis
        if abs(delta_x) <= self.move_speed:
            return True  # Pet has reached the mouse in the x-axis

        # Move the pet towards the mouse in the x-axis only
        if abs(delta_x) > self.move_speed:
            if delta_x > 0:
                self.curr_width += self.move_speed
                self.current_direction = 'right'  # Set direction to right
            else:
                self.curr_width -= self.move_speed
                self.current_direction = 'left'  # Set direction to left

        # Keep the y position fixed at 130
        self.curr_height = 950

        # Update the pet's position
        self.root.geometry(f'100x100+{self.curr_width}+{self.curr_height}')
        return False  # Pet has not reached the mouse yet

    def get_next_animation(self, curr_animation):
        if curr_animation == 'idle':
            return random.choice(['idle', 'walk_left', 'walk_right'])
        elif curr_animation == 'sleep':
            return random.choice(['idle', 'sleep'])
        elif curr_animation == 'walk_left':
            return 'walk_left' if self.current_direction == 'left' else 'walk_right'
        elif curr_animation == 'walk_right':
            return 'walk_right' if self.current_direction == 'right' else 'walk_left'

    def run(self):
        self.root.after(self.delay, self.update, 0, 'idle')
        self.root.mainloop()

    def quit(self):
        self.root.destroy()

if __name__ == '__main__':
    print('Initializing your desktop pet...')
    print('To quit, right click on the pet')
    print('Pet has a 1% chance to follow the mouse at any time')
    pet = Pet()
    pet.run()