import subprocess
import sys
import os
import json
from typing import Dict, List, Optional

from mcp.server.fastmcp import FastMCP
from mcp.shared.exceptions import McpError
from mcp.types import ErrorData, INTERNAL_ERROR, INVALID_PARAMS

mcp = FastMCP("interactive-draw")

# Path to save grid state
STATE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "board_state.json")

# Grid size
GRID_SIZE = 16

# Default grid state
DEFAULT_GRID_STATE = {
    "grid": [[" " for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)],
    "ui_process": None
}

# Load grid state from file or use default
def load_grid_state():
    try:
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, 'r') as f:
                state = json.load(f)
                # UI process can't be serialized, so we set it to None
                state["ui_process"] = None
                return state
        else:
            return DEFAULT_GRID_STATE.copy()
    except Exception as e:
        print(f"Error loading grid state: {e}")
        return DEFAULT_GRID_STATE.copy()

# Save grid state to file
def save_grid_state(state):
    try:
        # Create a copy of the state without the UI process
        state_copy = state.copy()
        state_copy.pop("ui_process", None)
        
        with open(STATE_FILE, 'w') as f:
            json.dump(state_copy, f)
    except Exception as e:
        print(f"Error saving grid state: {e}")

# Initialize grid state
grid_state = load_grid_state()

@mcp.tool()
def start_drawing_session() -> str:
    """
    Start a new Drawing Session and launch the UI.
    
    This will open a separate window with the drawing grid UI.
    """
    global grid_state
    
    # Reset the grid state
    grid_state = DEFAULT_GRID_STATE.copy()
    
    # Save the grid state
    save_grid_state(grid_state)
    
    # Launch the UI in a separate process
    try:
        # Kill any existing UI process
        if grid_state["ui_process"] is not None:
            try:
                grid_state["ui_process"].terminate()
            except:
                pass
        
        # Start a new UI process
        python_executable = sys.executable
        script_path = os.path.join(os.path.dirname(__file__), "ui", "__init__.py")
        grid_state["ui_process"] = subprocess.Popen([python_executable, script_path])
        
        return "New Drawing session started! The UI should open in a separate window."
    except Exception as e:
        raise McpError(
            ErrorData(
                INTERNAL_ERROR,
                f"Failed to start the UI: {str(e)}"
            )
        )

@mcp.tool()
def toggle_cell_color(row: int, col: int) -> str:
    """
    Toggle the color of a cell in the drawing grid.
    
    Args:
        row: Row index (0-{GRID_SIZE - 1})
        col: Column index (0-{GRID_SIZE - 1})
    
    Returns:
        Confirmation message indicating the cell toggle
    """
    global grid_state
    
    # Reload grid state to ensure we have the latest
    grid_state = load_grid_state()
    
    # Validate input
    if not (0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE):
        raise McpError(
            ErrorData(
                INVALID_PARAMS,
                f"Invalid position. Row and column must be between 0 and {GRID_SIZE - 1}."
            )
        )
    
    # Toggle the cell's color
    current_value = grid_state["grid"][row][col]
    new_value = "X" if current_value == " " else " "
    grid_state["grid"][row][col] = new_value
    
    # Save the updated grid state
    save_grid_state(grid_state)
    
    return f"Cell at ({row}, {col}) toggled. Current state: {new_value}"

@mcp.tool()
def get_grid_state() -> str:
    """
    Get the current state of the drawing grid.
    
    Returns:
        A string representation of the current grid state
    """
    global grid_state
    
    # Reload grid state to ensure we have the latest
    grid_state = load_grid_state()
    
    grid_str = "\n"
    for row in grid_state["grid"]:
        grid_str += " ".join(row) + "\n"
    
    return grid_str
