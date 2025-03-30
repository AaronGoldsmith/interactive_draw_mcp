# Interactive Drawing MCP

This project is an example of a Model Context Protocol (MCP) server with an interactive drawing interface. It demonstrates how to build an MCP extension that includes a separate UI window for drawing, using Tkinter as the graphical interface.

## Features

- **Drawing Grid Interface**: 
  - Offers a 16x16 grid where each cell can be toggled between two states (filled or empty).
  - Provides a clear grid button to reset all cells.

- **Server Capabilities**:
  - **Start Drawing Session**: Initializes a new session and launches the UI.
  - **Toggle Cell**: Toggle the color of individual cells via a command interface.
  - **Get Grid State**: Retrieve the current grid configuration as a text representation.

- **Persistence**: Grid state is saved to a JSON file (`board_state.json`) to maintain consistency across sessions.

- **UI and State Synchronization**:
  - **Real-Time UI Update**: A background thread continuously watches for updates to the grid state file and reflects changes visually.

## Installation

### Option 1: Install from Source

1. Clone this repository:
   ```
   git clone https://github.com/AaronGoldsmith/interactive_draw_mcp
   cd interactive_draw_mcp
   ```

2. Install the package:
   ```
   pip install -e .
   ```

## Usage

### As a Standalone MCP Server

Run the server to open the drawing window:

```
interactive-draw-mcp
```

### With Goose

#### Option 1: Using Goose CLI (recommended)

Start Goose with your extension enabled:

```bash
# Local Development
goose session --with-extension "python -m interactive-draw-mcp"
```

## Tools

- **Server Tools**:
  - `start_drawing_session()`: Initializes a drawing session and opens the UI.
  - `toggle_cell_color(row, col)`: Toggles the cell's color at specified `row` and `col`.
  - `get_grid_state()`: Provides a string representation of the grid's current state.

### Resources and References

- **Inspiration**: This MCP draws inspiration from [Kvadratni/tik-tak-toe-mcp](https://github.com/Kvadratni/tik-tak-toe-mcp).

## Architecture Overview

The architecture of this project demonstrates:

1. **MCP Server**: Manages communication between the Goose AI and the drawing interface via well-defined tools.
2. **Interactive UI**: Provides a visual interface for the grid.
3. **Integration with Goose AI**: Tool calls from Goose AI reflect directly onto the grid state and vice versa.

### Benefits

- **Separation of Responsibilities**: Maintains clear separation between server logic and UI presentation.
- **Improved User Experience**: Offers intuitive visual feedback alongside text-based command interface.
- **Adaptability**: Can be extended to more sophisticated applications involving AI and interactive UIs.

