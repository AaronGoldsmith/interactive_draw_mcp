import tkinter as tk
import os
import json
import time
import threading
import logging

GRID_SIZE = 80  # Define the grid size
STATE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "board_state.json")
LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "interactive_draw_mcp.log")

# Set up logging
logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class DrawingGridUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Drawing Grid")
        # Define base window size
        window_size = 800  
        tile_size = window_size // GRID_SIZE
        
        self.root.geometry(f"{window_size}x{window_size + 50}")
        
        # Create the grid UI using tiles
        self.tiles = []
        self.grid = [[" " for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        
        for i in range(GRID_SIZE):
            row = []
            for j in range(GRID_SIZE):
                canvas = tk.Canvas(root, width=tile_size, height=tile_size, bg="white", highlightthickness=1, highlightbackground="black")
                canvas.grid(row=i, column=j, padx=1, pady=1)
                canvas.bind("<Button-1>", lambda event, row=i, col=j: self.toggle_cell(row, col))
                row.append(canvas)
            self.tiles.append(row)
        
        # Reset button
        self.reset_button = tk.Button(
            root,
            text="Clear",
            font=('Arial', 12),
            command=self.clear_grid
        )
        self.reset_button.grid(row=GRID_SIZE, column=0, columnspan=GRID_SIZE, pady=5)
        
        # Start a thread to periodically check for updates
        self.should_update = True
        self.update_thread = threading.Thread(target=self.check_for_updates)
        self.update_thread.daemon = True
        self.update_thread.start()
        
        # Handle window close event
        root.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def update_ui_from_state(self):
        """Update the UI to reflect the current grid state"""
        try:
            if os.path.exists(STATE_FILE):
                with open(STATE_FILE, 'r') as f:
                    state = json.load(f)
                    logging.debug(f"Loaded state: {state['grid']}")
                    for i in range(GRID_SIZE):
                        for j in range(GRID_SIZE):
                            color = "black" if state["grid"][i][j] == "X" else "white"
                            logging.debug(f"Updating tile at ({i}, {j}) to color {color}")
                            self.tiles[i][j].config(bg=color)
        except Exception as e:
            logging.error(f"Error updating UI from state: {e}")

    def toggle_cell(self, row, col):
        """Toggle the state of a cell in the state file"""
        try:
            with open(STATE_FILE, 'r') as f:
                state = json.load(f)
            
            current_value = state["grid"][row][col]
            new_value = "X" if current_value == " " else " "
            state["grid"][row][col] = new_value
            logging.debug(f"Toggled cell ({row}, {col}) from {current_value} to {new_value}")
            
            with open(STATE_FILE, 'w') as f:
                json.dump(state, f)
                logging.debug(f"Saved new state: {state['grid']}")
        except Exception as e:
            logging.error(f"Error toggling cell: {e}")

    def clear_grid(self):
        """Clear the grid, resetting all cells to empty state"""
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                self.tiles[row][col].config(bg="white")
    
    def check_for_updates(self):
        """Periodically check for updates to the grid state file"""
        last_modified = 0
        if os.path.exists(STATE_FILE):
            last_modified = os.path.getmtime(STATE_FILE)
        
        while self.should_update:
            try:
                if os.path.exists(STATE_FILE):
                    current_modified = os.path.getmtime(STATE_FILE)
                    if current_modified > last_modified:
                        last_modified = current_modified
                        logging.debug("Detected state file update")
                        self.root.after(0, self.update_ui_from_state)
            except Exception as e:
                logging.error(f"Error checking for updates: {e}")
            
            time.sleep(0.5)  # Check every half second
    
    def on_close(self):
        """Handle window close event"""
        self.should_update = False
        self.root.destroy()

def main():
    root = tk.Tk()
    app = DrawingGridUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()