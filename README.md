# PyQt6 SSH Terminal Widget: UglierPTY

## Overview

UglierPTY is a proof-of-concept (POC) application created to explore the possibility of constructing a fully functional SSH Terminal Widget using PyQt6. This POC is inspired by its sister project, UglyPTY, a full-featured SSH client that utilizes xterm.js. The aim is to offer a similar, if not superior, feature set without relying on browser technologies or JavaScript, resulting in a more streamlined and resource-efficient solution.

## Features

- Fully functional SSH terminal built with PyQt6
- Communication class to manage SSH communication in real-time
- Resizable terminal window
- Terminal history and screen ratio control via pyte
- Modular design for easy embedding into other PyQt6 projects
- Free of Web technology (no xterm.js)

## Prerequisites

- Python 3.x
- PyQt6
- Paramiko
- pyte

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/scottpeterman/UglierPTY
    ```

2. Navigate into the project directory:

    ```bash
    cd UglierPTY
    ```

3. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

The primary entry point for this POC is the `uglierpty.py` script. To launch the application:

```bash
python uglierpty.py
```

Upon execution, you'll be presented with a dialog box asking for SSH credentials (host, username, and password). After successful authentication, the SSH Terminal interface will appear.

## Packet Flow

1. **Keyboard Input**: The user interacts with the PyQt6 terminal widget by providing keyboard input.
   
2. **Terminal Frontend**: The input is captured by the PyQt6 terminal frontend and passed to the Listener object.

3. **SSHLib and Communication**: The `SSHLib` class serves as the backend for SSH communication, managed by a Communication object running on a separate thread. The Communication class uses the Paramiko library to handle SSH communication with the host.

4. **Host Interaction**: Communication class sends the user input to the remote SSH host.

5. **Data Retrieval**: Communication class listens for incoming data from the remote host using `select.select()` and updates the terminal screen with the received data.

6. **Display**: The PyQt6 terminal widget displays the data, effectively showing the SSH session output.

Absolutely. Let's dive deeper into the mechanics of screen rendering and cursor handling, focusing on the calculations and data structures involved.

---

### Screen Management - Detailed Explanation

#### Screen Rendering

##### Data Structure: The Buffer Grid
- A 2D array of cells, where each cell contains:
  - `char`: The character to display.
  - `fg_color`: Foreground color.
  - `bg_color`: Background color.
  - `attributes`: Additional attributes like bold, underline, etc.

```python
buffer_grid = [
    [{"char": "H", "fg_color": "#FFFFFF", "bg_color": "#000000", "attributes": None},
     {"char": "e", "fg_color": "#FFFFFF", "bg_color": "#000000", "attributes": None},
     ...],
    [...],
    ...
]
```

##### PaintEvent: The Rendering Engine
- Qt's `paintEvent(QPaintEvent *event)` is overridden.
- A `QPainter` object is used for all graphical rendering.

```python
def paintEvent(self, event):
    painter = QPainter(self)
    # Logic to paint each cell of buffer_grid
```

##### Calculating Cell Position
- Cell width and height are calculated based on widget dimensions and grid size.
  
```python
cell_width = self.width() // num_columns
cell_height = self.height() // num_rows
```

- To draw a cell at `(row, col)`:

```python
x_position = col * cell_width
y_position = row * cell_height
```

##### Text and Attributes
- To draw text:

```python
painter.setPen(QColor(fg_color))
painter.drawText(x_position, y_position, char)
```

- To apply attributes like bold or underline:

```python
font = painter.font()
font.setBold(True if "bold" in attributes else False)
painter.setFont(font)
```

#### Cursor Handling

##### Cursor Position
- Stored as `(cursor_x, cursor_y)` in the 2D buffer_grid.

##### Rendering the Cursor
- Change the background color of the cell `(cursor_x, cursor_y)` during `paintEvent`.

```python
if (row, col) == (cursor_x, cursor_y):
    painter.fillRect(x_position, y_position, cell_width, cell_height, QColor(cursor_bg_color))
```

##### Cursor Movement Calculations
- Moving the cursor involves changing `(cursor_x, cursor_y)` and constraining it within the grid dimensions.

```python
# Move cursor down
cursor_x = min(cursor_x + 1, num_rows - 1)

# Move cursor up
cursor_x = max(cursor_x - 1, 0)
```

##### Cursor Blinking
- A `QTimer` toggles a boolean flag, which is then checked during each `paintEvent`.

```python
self.cursor_visible = not self.cursor_visible
self.update()  # Trigger a repaint
```

---

This should offer a detailed explanation of how screen rendering and cursor handling work in the SSHTerminal. Feel free to add code snippets or expand on these points to suit your implementation.
