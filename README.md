
# Terminapy

**Terminapy** is a lightweight Python library for creating a simple
ASCII/Unicode-based terminal "screen" with sub-screens. It allows you to
divide the terminal into multiple panels, each managed independently,
and safely share screens between threads.

## What Is It For?

Terminapy provides a `Screen` class that help you create and manage a display of the terminal:

    ╭───────────────────────┬───────────────────────╮
    │                       │                       │
    │                       │                       │
    │      Sub-Screen 1     │     Sub-Screen 2      │
    │   (displaying text)   │  (displaying text 2)  │
    │                       │                       │
    │                       │                       │
    ╰───────────────────────┴───────────────────────╯

>the lib provide function to print directly the screen on the terminal but you can get the screen as a str and display it on you own there will be some example 

### External Lib use:
> In this lib i will try to use as little as possible external lib
-   os
-   math
-   time
-   threading


## Installation

    pip install terminapy

## Usage Examples

### Simple loop

``` python
import terminapy as tp

screen = tp.screen()
while True:
    screen.draw_terminal_screen()
```

### Split vertically

``` python
import terminapy as tp

screen = tp.screen()
screen.split_vertical(0.5)
while True:
    screen.draw_terminal_screen()
```

### Updating content

``` python
import terminapy as tp
import time

screen = tp.screen()
screen.split_vertical(0.5)
left = screen.get_screen(0)
right = screen.get_screen(1)

left.append("Left panel: Hello!")
right.append("Right panel: Counter")

counter = 0
while True:
    counter += 1
    right.rewrite_last_line(f"Right panel: {counter}")
    screen.draw_terminal_screen()
    time.sleep(1)
```

### Threading Example

``` python
import terminapy as tp
import threading
import time

def worker(sub):
    for i in range(20):
        sub.append(f"Thread says {i}")
        time.sleep(0.5)

screen = tp.screen()
screen.split_vertical(0.5)
left = screen.get_screen(0)
right = screen.get_screen(1)

t = threading.Thread(target=worker, args=(right,))
t.start()

for _ in range(40):
    screen.draw_terminal_screen()
    time.sleep(0.25)
t.join()
```

## API Reference

|  Method | Description |
| :------ | :---------- |
|`screen(name: str)`                 | Create a new main screen  |
|`split_horizontally(ratio: float)`  | Split top/bottom          |
|`split_vertically(ratio: float)`    | Split left/right          |
|`change_line(lines:list[str],copy:bool = True)`| Replace all the previous lines by the new line|
|`append(message: str)`              | Append text to sub-screen |
|`clear()`                           | Clear a screen            |
|`rewrite_last_line(message: str)`   | Replace last line         |
|`get_screen(index: int)`            | Get a sub-screen          |
|`get_terminal_screen()`             | Get the str of the screen (what is use in **draw_terminal_screen**)|
|`draw_terminal_screen()`            | Render terminal screen    |
|`full_autonome(refresh_rate : float)`| Start a thread and refresh the terminal on it's own you do not need to have a loop do draw the screen on the terminal |
